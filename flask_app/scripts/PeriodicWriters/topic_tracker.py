from flask import render_template, redirect, url_for, send_file, session
from flask_login import login_required
from flask_app.scripts.create_flask_app import db, app
# from flask_app.scripts.PeriodicWriters.emailWeeklyRep import report
from flask_app.scripts.EmailValidator.emailReport import report

from flask_app.scripts.config import Config
from flask import request

from itsdangerous import URLSafeSerializer, BadData
import traceback, os
import pandas as pd
from datetime import datetime

JOURNALIST_ROUTE = '/topic_tracker'

csvname = {
                "AI": "top50AI.pdf",
                "Crypto": "top50Crypto.pdf",
                "Economics": "top50Economics.pdf",
                "Marketing": "top50Marketing.pdf",
                "NFT": "top50NFT.pdf",
                "Philosophy": "top50Philosophy.pdf",
            }


class UserAlreadySubscribed(Exception):
    pass


def timeframe2freq(timeframe):
    if timeframe == '_day':
        return 'Daily'
    elif timeframe == '_week':
        return 'Weekly'

def freq2timeframe(frequency):
    if frequency == 'Daily':
        return '_day'
    elif frequency == 'Weekly':
        return '_week'


def create_rules_topic(user_name,user_category,timeframe,url):
    return {
        '{username}': user_name,
        '{topic}': user_category,
        '{chosen_frequency}': timeframe.replace('_', ''),
        'URL_TO_UNSUBSCRIBE': url
    }

@login_required
def receive_category():
    """
    Gets csv(s) with Journalists from the form, extracts data.
    @param:    None
    @return:   Upload Journalists Page
    """
    if request.method == 'POST':

        user_name = session['name']# current_user.username
        user_email = session['email'] # request.form.get('email')
        user_category = request.form.get('category')
        timeframe = request.form.get('frequency')


        if timeframe == '_once':
            try:
                return send_file(os.path.join(Config.REPORTS_DIR,csvname[user_category]),
                                 mimetype='application/pdf',
                                 attachment_filename=csvname[user_category],
                                 as_attachment=True)

            except Exception:
                traceback.print_exc()


        # only executed if there is no 'journalists' table
        elif not db.inspect(db.engine.connect()).has_table(f'cat_writers{timeframe}'):
            data = [user_name, user_email, user_category]
            df = pd.DataFrame([data], columns=['ClientName', 'ClientEmail', 'Category'])
            df.to_sql(name=f'cat_writers{timeframe}', con=db.engine, index=False)

        else:
            try:

                # There are entries with current client, we remove the entries
                # TODO: with POSTGRES pandas can be removed
                users_df = pd.read_sql_table(f'cat_writers{timeframe}', db.engine)
                if not users_df[(users_df['ClientEmail'] == user_email) & (users_df['Category'] == user_category)].empty:
                    raise UserAlreadySubscribed

                # Add new entries
                # TODO: can be done just by using SQL or SQLAlchemy
                print("Adding new rows")
                data = [user_name, user_email, user_category]
                df = pd.DataFrame([data], columns=['ClientName', 'ClientEmail', 'Category'])
                journalists_df = pd.concat([users_df,df], ignore_index=True)
                journalists_df.to_sql(name=f'cat_writers{timeframe}', con=db.engine, index=False, if_exists='replace')

                return render_template('OnSuccess/Subscribed.html')

            except UserAlreadySubscribed:
                return render_template('topic_tracker.html',
                                       FLASH='<div class="flashed-message">You are already subscribed to this topic!</div>')

            except Exception:
                traceback.print_exc()

        try:
            unsub = URLSafeSerializer(app.secret_key, salt='unsubscribe_topic')
            # TODO: check if time frame is the same as in

            frequency = timeframe2freq(timeframe)

            token_string = f'{user_email} {frequency} {user_category}'
            token = unsub.dumps(token_string)

            app.config['SERVER_NAME'] = Config.SERVER_NAME
            with app.app_context(), app.test_request_context():
                url = url_for('unsubscribe_topic', token=token, _external=True)

            # open .html file in assets folder
            with open(os.path.join(Config.EMAIL_ASSETS_DIR, 'topic_sub.html'), 'r') as f:
                html = f.read()

            # TOPIC SUB PLACEHOLDERS
            rules = create_rules_topic(user_name, user_category, timeframe, url)

            gmail = report('"George Lightyear" <george@lightyearstrategies.com>',
                           user_email,
                           f"You Successfully Subscribed to {user_category} Updates!",
                           html,
                           user_id="me",
                           rules=rules)

            gmail.sendMessage()

        except Exception:
            traceback.print_exc()

        return redirect(JOURNALIST_ROUTE)

    return render_template('topic_tracker.html')

@app.route('/unsubscribe_topic/<token>') # must have
def unsubscribe_topic(token):
    unsub = URLSafeSerializer(app.secret_key, salt='unsubscribe_topic')

    try:
        email_sub_string = unsub.loads(token)
        #print(email_sub_string)
    except BadData:
        print('unsubscribe failed')
        return render_template('ErrorPages/500.html')

    email, frequency, category = email_sub_string.split()[0], email_sub_string.split()[1], email_sub_string.split()[2]
    if frequency == 'Daily':
        timeframe = '_day'
    elif frequency == 'Weekly':
        timeframe = '_week'
    else:
        print('Error occured with subject')
        return render_template('ErrorPages/500.html')

    # TODO: redo replacing of table
    jour_df_tf = pd.read_sql_table(f'cat_writers{timeframe}', con=db.engine)
    index_names = jour_df_tf[(jour_df_tf['ClientEmail'] == email) & (jour_df_tf['Category'] == category)].index
    jour_df_tf.drop(index_names, inplace=True)
    jour_df_tf.reset_index(inplace=True, drop=True)
    jour_df_tf.to_sql(f'cat_writers{timeframe}', con=db.engine, index=False, if_exists='replace')

    return render_template('OnSuccess/Unsubscribed.html')


def send_pdf_report(user_name, user_email, frequency, user_category):
    """
    sends the weekly pdf report
    note: needs to be in flaskMain to access flask specific stuff
    """
    try:
        unsub = URLSafeSerializer(app.secret_key, salt='unsubscribe_topic')
        token_string = f'{user_email} {frequency} {user_category}'
        token = unsub.dumps(token_string)

        app.config['SERVER_NAME'] = Config.SERVER_NAME
        with app.app_context(), app.test_request_context():
            url = url_for('unsubscribe_topic', token=token, _external=True)
            #print(url)

        # str_date = str(datetime.now().date())

        # to_send = report(
        #     sender='"George Lightyear" <george@lightyearstrategies.com>',
        #     to=user_email,
        #     subject=f'{user_category} Journalist Report {str_date}',
        #     text=f'Hi {user_name.capitalize()},\n\nHere is your {user_category} report.\n\nClick on the url to unsubscribe: {url}\n\n',
        #     file=f'flask_app/scripts/PeriodicWriters/reports/' + csvname[user_category]
        # )
        # to_send.sendMessage()




        # open .html file in assets folder
        with open(os.path.join(Config.EMAIL_ASSETS_DIR, 'topic_report.html'), 'r') as f:
            html = f.read()

        timeframe = freq2timeframe(frequency)

        # TOPIC REPORT PLACEHOLDERS
        rules = create_rules_topic(user_name, user_category, timeframe, url)

        gmail = report('"George Lightyear" <george@lightyearstrategies.com>',
                        user_email,
                        f"Your {frequency} {user_category} Report is Here!",
                        html,
                        file='flask_app/scripts/PeriodicWriters/reports/' + csvname[user_category],
                        user_id="me",
                        rules=rules)
        gmail.sendMessage()

    except Exception as e:
        print('Frequency: ', frequency)
        # TODO: Could create exception handling based on frequency
        traceback.print_exc()
        return render_template('ErrorPages/500.html')
