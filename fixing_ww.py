from flask_app.scripts.create_flask_app import db, app
import pandas as pd
from flask_app.scripts.PeriodicWriters.muckRack import google_muckrack as gm, Muckrack as mr
from flask_app.scripts.PeriodicWriters.journalist_upload_functions import send_pdf_report


timeframe = '_day'
days_back = 3
subject = 'Daily'

with app.app_context():
    journalists_db = pd.read_sql_table(f'journalists{timeframe}', db.engine)

    grouped_by_clientemail = journalists_db.groupby('ClientEmail')

    # this is the for loop that will make all the pdfs and send all the emails
    for email, df in grouped_by_clientemail:
        data={'Name':['Karan','Rohit','Sahil','Aryan'],'Age':[23,22,21,24]}

        df_for_email = pd.DataFrame(data)
        clientname = df.ClientName.iloc[0]
        send_pdf_report(df_for_email, email, subject, clientname)