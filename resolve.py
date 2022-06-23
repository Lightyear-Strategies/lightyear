import flaskMain as fm
import pandas as pd
from weeklyWriters.muckRack import google_muckrack as gm, Muckrack as mr


timeframe = '_day'
days_back = 3
subject = 'Daily'

journalists_db = pd.read_sql_table(f'journalists{timeframe}', fm.db.engine)

grouped_by_clientemail = journalists_db.groupby('ClientEmail')

# this is the for loop that will make all the pdfs and send all the emails
for email, df in grouped_by_clientemail:
    data={'Name':['Karan','Rohit','Sahil','Aryan'],'Age':[23,22,21,24]}

    df_for_email = pd.DataFrame(data)
    clientname = df.ClientName.iloc[0]
    fm.send_pdf_report(df_for_email, email, subject, clientname)
