from flask_app.scripts.create_flask_app import db, app
from flask_app.scripts.PeriodicWriters.categoricalWriters import send_pdf_report
from flask_app.scripts.PeriodicWriters.weekly import Report
import pandas as pd
import traceback
import sys

import logging
from logging import StreamHandler, Formatter

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)
# logger.info(f'Adding {len(haro_df)} New Haros')


if __name__ == "__main__":
    try:
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
                try:
                    journalists_db = pd.read_sql_table(f'cat_writers{timeframe}', db.engine)

                    for index, row in journalists_db.iterrows():
                        print(row[1])
                        with app.app_context():
                            send_pdf_report(row[0], row[1], frequency, row[2])

                        #send_pdf_report(df_for_email, email, subject, clientname)
                except Exception:
                    logger.info(f'Problem with smth particular:')
                    traceback.print_exc(file=sys.stdout)
    except Exception:
        logger.info(f'Problem with smth broad:')
        traceback.print_exc(file=sys.stdout)


