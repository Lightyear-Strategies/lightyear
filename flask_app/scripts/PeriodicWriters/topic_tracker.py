from flask import render_template, redirect, url_for
from flask_login import login_required
from flask_app.scripts.forms import TopicTracker
from flask_app.scripts.create_flask_app import db, app
from flask_app.scripts.PeriodicWriters.emailWeeklyRep import report
from flask_app.scripts.config import Config
from flask_app.scripts.googleAuth import authCheck, localServiceBuilder

from itsdangerous import URLSafeSerializer, BadData
import traceback
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

def gauth():
    if Config.ENVIRONMENT == 'server':
        if not authCheck():
            return redirect('/authorizeCheck')
    elif Config.ENVIRONMENT == 'local':
        localServiceBuilder()


@login_required
def receive_category():
    """
    Gets csv(s) with Journalists from the form, extracts data.
    @param:    None
    @return:   Upload Journalists Page
    """
    user_name, email = None, None
    user_category, timeframe = None, None

    form = TopicTracker()
    if form.validate_on_submit():

        # TODO: lower()
        user_name = form.username.data
        user_email = form.email.data
        user_category = form.category.data
        timeframe = form.frequency.data
        #print(timeframe, user_category)

        if timeframe == '_now':
            gauth()
            str_date = str(datetime.now().date())

            to_send = report(
                sender='george@lightyearstrategies.com',
                to=user_email,
                subject=f'{user_category} Journalist Report {str_date}',
                text=f'Hi {user_name},\n\nHere is your {user_category} report.\n\n\n',
                file= f'flask_app/scripts/PeriodicWriters/reports/' + csvname[user_category]
            )
            to_send.sendMessage()


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
                print(f'{user_name} already subscribed on {user_category} category')

            except Exception:
                traceback.print_exc()

        return redirect(JOURNALIST_ROUTE)

    return render_template('topic_tracker.html', form=form, user_name=user_name, email=email,
                           user_category=user_category, timeframe=timeframe)

@app.route('/unsubscribe_topic/<token>')
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
        return render_template('ErrorPages/500.html')
        print('Error occured with subject')

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
        # TODO: fix this :)
        app.config['SERVER_NAME'] = '192.168.0.174:8000'
        with app.app_context():
            url = url_for('unsubscribe_topic', token=token, _external=True)
            #print(url)

        str_date = str(datetime.now().date())

        gauth()

        to_send = report(
            sender='george@lightyearstrategies.com',
            to=user_email,
            subject=f'{user_category} Journalist Report {str_date}',
            text=f'Hi {user_name},\n\nHere is your {user_category} report.\n\nClick on the url to unsubscribe: {url}\n\n',
            file=f'flask_app/scripts/PeriodicWriters/reports/' + csvname[user_category]
        )
        to_send.sendMessage()

    except Exception as e:
        print(e)
        return render_template('ErrorPages/500.html')
