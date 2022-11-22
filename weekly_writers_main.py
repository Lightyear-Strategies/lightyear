from flask_app.scripts.create_flask_app import db, app
from flask_app.scripts.PeriodicWriters.muckRack import google_muckrack as gm
from flask_app.scripts.PeriodicWriters.muckRack import Muckrack as mr
from flask_app.scripts.PeriodicWriters.journalist_tracker import send_pdf_report

import sys, traceback
import pandas as pd


def links(journalists_db : pd.DataFrame, timeframe : str):
    links_needed = journalists_db[journalists_db['Muckrack'].isnull()]
    gm_ob = gm.google_muckrack(links_needed, 'Journalist')
    new_df = gm_ob.get_dataframe()
    journalists_db[journalists_db['Muckrack'].isnull()] = new_df
    with app.app_context():
        journalists_db.to_sql(f'journalists{timeframe}', db.engine, index=False, if_exists='replace')


if __name__ == "__main__":

    if sys.argv[2] == 'day':
        timeframe = '_day'
        days_back = 3
        subject = 'Daily'
    elif sys.argv[2] == 'month':
        timeframe = '_month'
        days_back = 30
        subject = 'Monthly'
    else:
        timeframe = '_week'
        days_back = 7
        subject = 'Weekly'

    with app.app_context():
        journalists_db = pd.read_sql_table(f'journalists{timeframe}', db.engine)

    if sys.argv[1] == "links":
        links(journalists_db, timeframe)


    if sys.argv[1] == "parse":
        unique_links = list(journalists_db['Muckrack'].unique())
        parser = mr.Muckrack(url_list=unique_links, timeframe=days_back)
        parser.parse_HTML()
        try:
            grouped_by_name = parser.df.groupby('Name')
        except KeyError:
            # no articles for anything
            grouped_by_name = None
            print(f'no articles this {timeframe[1:]}')
        grouped_by_clientemail = journalists_db.groupby('ClientEmail')

        # this is the for loop that will make all the pdfs and send all the emails
        for email, df in grouped_by_clientemail:
            df_list_to_concat = list()
            for jour_name in df.Journalist:
                try:
                    if grouped_by_name == None:
                        print('sss')
                        raise KeyError
                    df_list_to_concat.append(grouped_by_name.get_group(jour_name))
                except KeyError:
                    # no info for this journalist in particular
                    # TODO: add way to tell the user that no updates for this journalist are out for this week
                    traceback.print_exc()
                    print('Zhopa')
                    continue
            try:
                df_for_email = pd.concat(df_list_to_concat)
            except ValueError:
                # No info for any of the journalists for email
                # TODO: find way to send an email letting the user know that none of their journalists had updates this week
                continue

            clientname = df.ClientName.iloc[0]
            print('client')
            send_pdf_report(df_for_email, email, subject, clientname)
            print('hui')