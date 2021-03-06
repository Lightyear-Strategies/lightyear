from flask_login import login_required
from flask_app.scripts.create_flask_app import db
from flask import render_template, request
from datetime import datetime, timedelta
import pandas as pd


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


def addDBData(df: pd.DataFrame): #(file):
    """
    Adds data to SQLite DB and checks for duplicates
    @param:    csv file with parsed haros
    @return:   None
    """
    # checking for duplicates
    try:
        whole_db = pd.read_sql_table('haros', db.engine, index_col='index')
        print(len(whole_db))
        print(whole_db.columns)
        res = pd.concat([df, whole_db])
    except Exception as e:
        res = df
        print(e)
    print(len(res))
    res.drop_duplicates(subset=['Summary'], inplace=True)
    print(len(res))
    res.reset_index(drop=True, inplace=True)

    # Load data to database
    print(res.columns)
    res.to_sql(name='haros', con=db.engine, index=True, if_exists='replace')


@login_required
def show_haro_table():
    """
    Shows Haro Table
    @param:    None
    @return:   Haros table
    """
    return render_template('HaroTable/haroTableView.html', title='LyS Haros Database')


def adding_used_unused(option: str = None, id: str = None):
    """
    Changes value in "Used" column of certain haro by using id
    Values can be "Used" or "None"
    @param:    option and id in the table
    @return:   string
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


def serve_data(option=None):
    """
    Sorts the table, returns searched data
    @param:    None/option
    @return:   table entries
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

        desired_col = getattr(Haros.columns,col_name)

        #decending
        if descending:
            desired_col = desired_col.desc()
        order.append(desired_col)

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