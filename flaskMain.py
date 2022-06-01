###################### Imports ######################
from flask import render_template, request, redirect, flash

import pandas as pd
import os, sys, time, traceback
from datetime import datetime, timedelta

from flask_app.scripts.forms import uploadJournalistCSV
from flask_app.scripts.create_flask_app import app, bootstrap, db
from flask_app.scripts import ev_flask_functions as ev_f_f


###################### Functions ######################

#@param:    None
#@return:   Upload Journalists Page
@app.route('/journalists', methods=['GET','POST'])
def uploadJournalist():
    """
    Gets csv(s) with Journalists from the form, extracts data.
    """
    personname, email, files = None, None, None

    form = uploadJournalistCSV()
    if form.validate_on_submit():
        personname = form.personname.data
        personemail = form.email.data
        files = request.files.getlist(form.files.name)
        form.email.data = ''
        # filename

        journalists = []
        if files:
            for file in files:
                df = None
                try:
                    df = pd.read_csv(file)

                except Exception:
                    flash("Upload file in CSV Format")
                    print("Not CSV")
                    return redirect("/journalists")


                finally:
                    """For Future: should use re to check for 'ournalist' string """

                    pos_names = ["Journalists","Journalist","Journalist(s)","journalists", "journalist", "journalist(s)"]
                    i = 0
                    len_pos_names = len(pos_names)
                    while True:
                        if i == len_pos_names:
                            flash("You do not have neither \"Journalist(s)\" nor \"journalist(s)\"")
                            return redirect("/journalists")
                        if pos_names[i] in df.columns:
                            journalists.extend(df[pos_names[i]].tolist())
                            break
                        i+=1

            # only executed if there is no 'journalists' table
            if not db.inspect(db.engine.connect()).has_table('journalists'):
                data = [[personname,personemail,journalist, None] for journalist in journalists]
                df = pd.DataFrame(data, columns = ['ClientName', 'ClientEmail', 'Journalist','Muckrack'])
                df.to_sql(name='journalists', con=db.engine, index=False)

            else:
                try:
                    """For Future: No so efficient to drop all old entries and then append the new ones"""
                    journalists_df = pd.read_sql_table('journalists', db.engine)

                    # There are entries with current client, we remove the entries
                    if len(journalists_df[journalists_df['ClientName'] == personname]) > 0:
                        print("Deleting old entries")
                        journalists_df = journalists_df[journalists_df['ClientName'] != personname]

                    # Add new entries
                    print("Adding new rows")
                    data = [[personname, personemail, journalist, None] for journalist in journalists]
                    new_df = pd.DataFrame(data, columns=['ClientName', 'ClientEmail', 'Journalist','Muckrack'])
                    journalists_df = pd.concat([journalists_df,new_df], ignore_index=True)
                    journalists_df.to_sql(name='journalists', con=db.engine, index=False, if_exists='replace')

                    flash('Successfully Subscribed')
                except Exception:
                    traceback.print_exc()

                    # script to drop table, run with sudo privilege
                    #jour_table = db.Table('journalists', db.metadata, autoload=True, autoload_with=db.engine)
                    #print("Dropping the Journalists Table")
                    #jour_table.drop(db.engine)

            return redirect("/journalists")
        else:
            print('No files')

    return render_template('uploadJournalistCSV.html', form=form, email=email, files=files)

def removeDBdups():
    """
    removes duplicates from SQLite DB, does not need to be run often, as the addDBData function now checks for duplicates
    """
    whole_db = pd.read_sql_table('haros', db.engine)
    print(whole_db)
    whole_db.drop_duplicates(subset=['Summary'], inplace=True)
    print(whole_db)
    whole_db.to_sql('haros', con=db.engine, index=False, if_exists='replace')
    new_db = pd.read_sql_table('haros', db.engine)
    print(new_db)

# @param:    csv file with parsed haros
# @return:   None
def addDBData(df: pd.DataFrame): #(file):
    """
    Adds data to SQLite DB and checks for duplicates
    """
    # checking for duplicates
    whole_db = pd.read_sql_table('haros', db.engine, index_col='index')
    print(len(whole_db))
    print(whole_db.columns)
    res = pd.concat([df,whole_db])
    print(len(res))
    res.drop_duplicates(subset=['Summary'], inplace=True)
    print(len(res))
    res.reset_index(drop=True, inplace=True)

    # Load data to database
    print(res.columns)
    res.to_sql(name='haros', con=db.engine, index=True, if_exists='replace')



#@param:    None
#@return:   Haros table
@app.route('/haros')
def serveTable():
    """
    Brings to the table with Haros
    """
    return render_template('haroTableView.html', title='LyS Haros Database')

#@param:    option and id in the table
#@return:   string
@app.route('/api/used/<option>/<id>')
def used_unused(option : str = None, id : str = None):
    """
    Changes value in "Used" column of certain haro by using id
    Values can be "Used" or "None"
    """

    Haros = db.Table('haros', db.metadata, autoload=True, autoload_with=db.engine)
    query = db.session.query(Haros).filter(Haros.columns.index == int(id))
    #print(query.all())

    if option == "add":
        query.update({Haros.columns.Used : "Used" })
        db.session.commit()

    elif option == "remove":
        query.update({Haros.columns.Used: "None"})
        db.session.commit()

   # print(query.all())

    return "Ok"


#@param:    None/option
#@return:   table entries
@app.route('/api/serveHaros/<option>')
@app.route('/api/serveHaros')
def data(option=None):
    """
    Sorts the table, returns searched data
    """

    Haros = db.Table('haros', db.metadata, autoload=True, autoload_with=db.engine)
    #print(Haros.columns.DateReceived.all_())
    query = db.session.query(Haros) #.all()

    if option == "used":
        query = query.filter(Haros.columns.Used == "Used")

    # fresh queries
    if option == "fresh":
        freshmark = datetime.today().date() - timedelta(days=3)
        query = query.filter(Haros.columns.DateReceived >= freshmark)

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            Haros.columns.Category.like(f'%{search}%'),
            Haros.columns.DateReceived.like(f'%{search}%'),
            Haros.columns.Summary.like(f'%{search}%'),
            Haros.columns.Email.like(f'%{search}%'),
            Haros.columns.MediaOutlet.like(f'%{search}%'),
            Haros.columns.Name.like(f'%{search}%'),
            Haros.columns.Requirements.like(f'%{search}%')
        ))

    total_filtered = query.count()

    # sorting
    order = []
    i = 0
    while True:

        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['Category','MediaOutlet','DateReceived']:
            col_name = 'TimeStamp'
        if col_name == 'DateReceived':
            col_name = 'TimeStamp'

        # gets descending sorting
        descending = request.args.get(f'order[{i}][dir]') == 'desc'

        desiredCol = getattr(Haros.columns,col_name)

        #decending
        if descending:
            desiredCol = desiredCol.desc()
        order.append(desiredCol)

        i += 1

    # ordering
    if order:
        query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    # response to be shown on HTML side
    return {
        'data': [dict(haro) for haro in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': query.count(),
        'draw': request.args.get('draw', type=int),
    }


app.add_url_rule('/email_verification', view_func=ev_f_f.email_verification,methods=['GET','POST'])


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80,debug=False,threaded=True)


