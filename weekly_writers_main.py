from flask_app.scripts.create_flask_app import db
from weeklyWriters.muckRack import google_muckrack as gm, Muckrack as mr
from weeklyWriters.toPDF import pdfReport
from weeklyWriters.emailWeeklyRep import report
import sys, datetime
import pandas as pd


if __name__ == "__main__":
    
    journalists_db = journalists = pd.read_sql_table('journalists', db.engine)

    if sys.argv[1] == "links":
        links_needed = journalists_db[journalists_db['Muckrack'].isnull()]
        gm_ob = gm.google_muckrack(links_needed, 'Journalist')
        new_df = gm_ob.get_dataframe()
        journalists_db[journalists_db['Muckrack'].isnull()] = new_df
        journalists_db.to_sql('journalists', db.engine, index=False, if_exists='replace')

    if sys.argv[1] == "parse":
        unique_links = list(journalists_db['Muckrack'].unique())
        parser = mr.Muckrack(unique_links)
        parser.parse_HTML()
        try:
            grouped_by_name = parser.df.groupby('Name')
        except KeyError:
            # no articles for anything
            print('no articles this week')
        grouped_by_clientemail = journalists_db.groupby('ClientEmail')

        # this is the for loop that will make all the pdfs and send all the emails
        for email, df in grouped_by_clientemail:
            df_list_to_concat = list()
            for jour_name in df.Journalist:
                try:
                    df_list_to_concat.append(grouped_by_name.get_group(jour_name))
                except KeyError:
                    # no info for this journalist in particular
                    # TODO: add way to tell the user that no updates for this journalist are out for this week
                    continue
            try:
                df_for_email = pd.concat(df_list_to_concat)
            except ValueError:
                # No info for any of the journalists for email
                # TODO: find way to send an email letting the user know that none of their journalists had updates this week
                continue
            
            pdf_maker_for_email = pdfReport(df_for_email)
            filepath = f'weeklyWriters/reports/{email}_journalist_report.pdf'
            pdf_for_email = pdf_maker_for_email.create_PDF(filename=filepath)

            clientname = df.ClientName.iloc[0]
            str_date = str(datetime.datetime.now().date())

            email = report(
                sender='george@lightyearstrategies.com',
                to=email,
                subject=f'Weekly Journalist Report {str_date}',
                text=f'Hi {clientname},\n\nHere is your weekly report.',
                file=filepath
            )
            email.sendMessage()