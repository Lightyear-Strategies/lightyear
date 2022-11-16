from flask import render_template, request, redirect, url_for, session
from flask_login import login_required
from flask_app.scripts.create_flask_app import db, app
from flask_app.scripts.PeriodicWriters.toPDF import pdfReport
from flask_app.scripts.PeriodicWriters.emailWeeklyRep import report
from flask_app.scripts.config import Config

from itsdangerous import URLSafeSerializer, BadData
import traceback
import pandas as pd
from datetime import datetime

JOURNALIST_ROUTE = '/journalist_tracker'


@login_required
def receive_journalists():
    """
    Gets csv(s) with Journalists from the form, extracts data.
    @param:    None
    @return:   Upload Journalists Page
    """

    if request.method == 'POST':
        files = request.files
        user_email = session['email'] #request.form.get('email')
        timeframe = request.form.get('frequency')
        user_name = session['name'] # current_user.username

        if files:

            journalists = []
            for filename in files:
                uploaded_file = files.get(filename)

                df = None
                try:
                    df = pd.read_csv(uploaded_file)
                    print(df.columns)

                except Exception:
                    print("Not CSV")
                    return redirect(JOURNALIST_ROUTE)


                finally:
                    """For Future: should use re to check for 'ournalist' string """
                    pos_names = ["Journalists","Journalist","Journalist(s)","journalists", "journalist", "journalist(s)"]

                    for i in range(0,len(pos_names)):
                        if pos_names[i] in df.columns:
                            journalists.extend(df[pos_names[i]].tolist())
                            break

                        if i+1 == len(pos_names):
                            print('No "Journalists" column')


            if not db.inspect(db.engine.connect()).has_table(f'journalists{timeframe}'):
                print('Creating new table')
                data = [[user_name, user_email, journalist, None] for journalist in journalists]
                print(data)
                df = pd.DataFrame(data, columns=['ClientName', 'ClientEmail', 'Journalist', 'Muckrack'])
                df.to_sql(name=f'journalists{timeframe}', con=db.engine, index=False)
                print("Added data to the new table")

            else:
                try:
                    # TODO: For Future: Not so efficient to drop all old entries and then append the new ones
                    journalists_df = pd.read_sql_table(f'journalists{timeframe}', db.engine)

                    # There are entries with current client, we remove the entries
                    if len(journalists_df[journalists_df['ClientEmail'] == user_email]) > 0:
                        print("Deleting old entries")
                        journalists_df = journalists_df[journalists_df['ClientEmail'] != user_email]

                    # Add new entries
                    print("Adding new rows")
                    data = [[user_name, user_email, journalist, None] for journalist in journalists]
                    new_df = pd.DataFrame(data, columns=['ClientName', 'ClientEmail', 'Journalist','Muckrack'])
                    journalists_df = pd.concat([journalists_df,new_df], ignore_index=True)
                    journalists_df.to_sql(name=f'journalists{timeframe}', con=db.engine, index=False, if_exists='replace')

                    return render_template('OnSuccess/Subscribed.html')
                except Exception:
                    traceback.print_exc()

                    # script to drop table, run with sudo privilege
                    #jour_table = db.Table('journalists', db.metadata, autoload=True, autoload_with=db.engine)
                    #print("Dropping the Journalists Table")
                    #jour_table.drop(db.engine)

            return redirect(JOURNALIST_ROUTE)
        else:
            print('No files')

    return render_template('journalistTracker.html')

@app.route('/unsubscribe_journalist/<token>')
def unsubscribe_journalist(token):
    unsub = URLSafeSerializer(app.secret_key, salt='unsubscribe_journalist')

    try:
        email_sub_string = unsub.loads(token)
        #print(email_sub_string)
    except BadData:
        print('unsubscribe failed')
        return render_template('ErrorPages/500.html')

    email, subject = email_sub_string.split()[0], email_sub_string.split()[1]
    if subject == 'Daily':
        timeframe = '_day'
    elif subject == 'Monthly':
        timeframe = '_month'
    elif subject == 'Weekly':
        timeframe = '_week'
    else:
        return render_template('ErrorPages/500.html')
        print('Error occured with subject')

    # TODO: redo replacing of table
    jour_df_tf = pd.read_sql_table(f'journalists{timeframe}', con=db.engine)
    index_names = jour_df_tf[jour_df_tf['ClientEmail'] == email].index
    jour_df_tf.drop(index_names, inplace=True)
    jour_df_tf.reset_index(inplace=True, drop=True)
    jour_df_tf.to_sql(f'journalists{timeframe}', con=db.engine, index=False, if_exists='replace')

    return render_template('OnSuccess/Unsubscribed.html')


def send_pdf_report(df_for_email, email, subject, clientname):
    """
    sends the weekly pdf report
    note: needs to be in flaskMain to access flask specific stuff
    """
    try:
        unsub = URLSafeSerializer(app.secret_key, salt='unsubscribe_journalist')
        token_string = f'{email} {subject}'
        token = unsub.dumps(token_string)

        app.config['SERVER_NAME'] = Config.SERVER_NAME
        with app.app_context(), app.test_request_context():
            url = url_for('unsubscribe_journalist', token=token, _external=True)
            #print(url)
        pdf_maker_for_email = pdfReport(df_for_email, unsub_link=url)
        filepath = f'weeklyWriters/reports/{email}_journalist_report.pdf'
        pdf_maker_for_email.create_PDF(filename=filepath)

        str_date = str(datetime.now().date())

        to_send = report(
            sender='"George Lightyear" <george@lightyearstrategies.com>',
            to=email,
            subject=f'{subject} Journalist Report {str_date}',
            text=f'Hi {clientname.capitalize()},\n\nHere is your {subject.lower()} report.\n\n\n',
            file=filepath
        )
        to_send.sendMessage()

    except Exception:
        traceback.print_exc()
        return render_template('ErrorPages/500.html')