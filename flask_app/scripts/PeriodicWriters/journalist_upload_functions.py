from flask import render_template, request, redirect, flash, url_for
from flask_login import login_required
from flask_app.scripts.forms import uploadJournalistCSV
from flask_app.scripts.create_flask_app import db, app
from flask_app.scripts.PeriodicWriters.toPDF import pdfReport
from flask_app.scripts.PeriodicWriters.emailWeeklyRep import report

from itsdangerous import URLSafeSerializer, BadData
import traceback
import pandas as pd
from datetime import datetime

JOURNALIST_ROUTE = '/writers'

@login_required
def load_journalist_file():
    """
    Gets csv(s) with Journalists from the form, extracts data.
    @param:    None
    @return:   Upload Journalists Page
    """
    user_name, email, files = None, None, None

    form = uploadJournalistCSV()
    if form.validate_on_submit():
        user_name = form.username.data
        user_email = form.email.data
        files = request.files.getlist(form.files.name)
        timeframe = form.frequency.data
        #print(timeframe)

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
                        i += 1

            # only executed if there is no 'journalists' table
            # if not db.inspect(db.engine.connect()).has_table('journalists'):
            #     data = [[user_name, user_email, journalist, None] for journalist in journalists]
            #     df = pd.DataFrame(data, columns = ['ClientName', 'ClientEmail', 'Journalist','Muckrack'])
            #     df.to_sql(name='journalists', con=db.engine, index=False)

            if not db.inspect(db.engine.connect()).has_table(f'journalists{timeframe}'):
                data = [[user_name, user_email, journalist, None] for journalist in journalists]
                df = pd.DataFrame(data, columns=['ClientName', 'ClientEmail', 'Journalist', 'Muckrack'])
                df.to_sql(name=f'journalists{timeframe}', con=db.engine, index=False)

            else:
                try:
                    # TODO: For Future: Not so efficient to drop all old entries and then append the new ones
                    journalists_df = pd.read_sql_table(f'journalists{timeframe}', db.engine)

                    # There are entries with current client, we remove the entries
                    if len(journalists_df[journalists_df['ClientName'] == user_name]) > 0:
                        print("Deleting old entries")
                        journalists_df = journalists_df[journalists_df['ClientName'] != user_name]

                    # Add new entries
                    print("Adding new rows")
                    data = [[user_name, user_email, journalist, None] for journalist in journalists]
                    new_df = pd.DataFrame(data, columns=['ClientName', 'ClientEmail', 'Journalist','Muckrack'])
                    journalists_df = pd.concat([journalists_df,new_df], ignore_index=True)
                    journalists_df.to_sql(name=f'journalists{timeframe}', con=db.engine, index=False, if_exists='replace')

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

@app.route('/unsubscribe/<token>')
def unsubscribe(token):
    unsub = URLSafeSerializer(app.secret_key, salt='unsubscribe')

    try:
        email_sub_string = unsub.loads(token)
        print(email_sub_string)
    except BadData:
        print('unsubscribe failed')
        return render_template('error_pages/500.html')

    email, subject = email_sub_string.split()[0], email_sub_string.split()[1]
    if subject == 'Daily':
        timeframe = '_day'
    elif subject == 'Monthly':
        timeframe = '_month'
    elif subject == 'Weekly':
        timeframe = '_week'
    else:
        return render_template('error_pages/500.html')
        print('Error occured with subject')

    # TODO: redo replacing of table
    jour_df_tf = pd.read_sql_table(f'journalists{timeframe}', con=db.engine)
    index_names = jour_df_tf[jour_df_tf['ClientEmail'] == email].index
    jour_df_tf.drop(index_names, inplace=True)
    jour_df_tf.reset_index(inplace=True, drop=True)
    jour_df_tf.to_sql(f'journalists{timeframe}', con=db.engine, index=False, if_exists='replace')

    return render_template('successUnsubscribe.html')


def send_pdf_report(df_for_email, email, subject, clientname):
    """
    sends the weekly pdf report
    note: needs to be in flaskMain to access flask specific stuff
    """
    unsub = URLSafeSerializer(app.secret_key, salt='unsubscribe')
    token_string = f'{email} {subject}'
    token = unsub.dumps(token_string)
    # TODO: fix this :)
    app.config['SERVER_NAME'] = '192.168.0.173:8000'
    with app.app_context():
        url = url_for('unsubscribe', token=token, _external=True)
        print(url)
    pdf_maker_for_email = pdfReport(df_for_email, unsub_link=url)
    # TODO: fix this :)
    #filepath = 'flask_app/scripts/PeriodicWriters/reports/george@lightyearstrategies.com_journalist_report.pdf'
    filepath = f'weeklyWriters/reports/{email}_journalist_report.pdf'
    pdf_maker_for_email.create_PDF(filename=filepath)

    str_date = str(datetime.now().date())

    to_send = report(
        sender='george@lightyearstrategies.com',
        to=email,
        subject=f'{subject} Journalist Report {str_date}',
        text=f'Hi {clientname},\n\nHere is your {subject.lower()} report.\n\n\n',
        file=filepath
    )
    to_send.sendMessage()