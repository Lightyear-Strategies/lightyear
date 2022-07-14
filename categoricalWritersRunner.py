from flask_app.scripts.create_flask_app import db, app
from flask_app.scripts.PeriodicWriters.categoricalWriters import send_pdf_report
from flask_app.scripts.PeriodicWriters.weekly import Report
import sys
import pandas as pd


if __name__ == "__main__":
    if sys.argv[1] == "parse":
        if sys.argv[2] == 'all':
            df = Report(parsed=True)
            df.parse_all_categories()
        else:
            df = Report(parsed=True)
            df.parse_category(sys.argv[2])

    elif sys.argv[1] == "send":

        if sys.argv[2] == 'day':
            timeframe = '_day'
            days_back = 3
            frequency = 'Daily'
        elif sys.argv[2] == 'week':
            timeframe = '_week'
            days_back = 7
            frequency = 'Weekly'

        with app.app_context():
            journalists_db = pd.read_sql_table(f'cat_writers{timeframe}', db.engine)

            for index, row in journalists_db.iterrows():
                print(row[1])
                with app.app_context():
                    send_pdf_report(row[0], row[1], frequency, row[2])

            #send_pdf_report(df_for_email, email, subject, clientname)
