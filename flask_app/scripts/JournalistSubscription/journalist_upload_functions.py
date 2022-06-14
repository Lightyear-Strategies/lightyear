from flask import render_template, request, redirect, flash
from flask_login import login_required
from flask_app.scripts.forms import uploadJournalistCSV
from flask_app.scripts.create_flask_app import db
import traceback
import pandas as pd

JOURNALIST_ROUTE = '/journalists'

@login_required
def load_journalist_file():
    """
    Gets csv(s) with Journalists from the form, extracts data.
    @param:    None
    @return:   Upload Journalists Page
    """
    username, email, files = None, None, None

    form = uploadJournalistCSV()
    if form.validate_on_submit():
        username = form.username.data
        user_email = form.email.data
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
                    return redirect(JOURNALIST_ROUTE)


                finally:
                    """For Future: should use re to check for 'ournalist' string """

                    pos_names = ["Journalists","Journalist","Journalist(s)","journalists", "journalist", "journalist(s)"]
                    i = 0
                    len_pos_names = len(pos_names)
                    while True:
                        if i == len_pos_names:
                            flash("You do not have neither \"Journalist(s)\" nor \"journalist(s)\"")
                            return redirect(JOURNALIST_ROUTE)
                        if pos_names[i] in df.columns:
                            journalists.extend(df[pos_names[i]].tolist())
                            break
                        i+=1

            # only executed if there is no 'journalists' table
            if not db.inspect(db.engine.connect()).has_table('journalists'):
                data = [[username, user_email, journalist, None] for journalist in journalists]
                df = pd.DataFrame(data, columns = ['ClientName', 'ClientEmail', 'Journalist','Muckrack'])
                df.to_sql(name='journalists', con=db.engine, index=False)

            else:
                try:
                    """For Future: Noе so efficient to drop all old entries and then append the new ones"""
                    journalists_df = pd.read_sql_table('journalists', db.engine)

                    # There are entries with current client, we remove the entries
                    if len(journalists_df[journalists_df['ClientName'] == username]) > 0:
                        print("Deleting old entries")
                        journalists_df = journalists_df[journalists_df['ClientName'] != username]

                    # Add new entries
                    print("Adding new rows")
                    data = [[username, user_email, journalist, None] for journalist in journalists]
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

            return redirect(JOURNALIST_ROUTE)
        else:
            print('No files')

    return render_template('uploadJournalistCSV.html', form=form, email=email, files=files)