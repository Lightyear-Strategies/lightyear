from flask_app.scripts.HaroTable.haro_table_functions import addDBData
from haroListener.haro_listener import HaroListener
from flaskMain import app
import pandas as pd

import traceback
import logging
import sys
from logging import StreamHandler, Formatter

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)


if __name__ == "__main__":
    try:
        hl = HaroListener('george@lightyearstrategies.com')
        recent_haro = hl.find_haro_from()[0]
        haro_df = recent_haro.get_dataframe()


        # Debugging
        # haro_df = pd.read_csv('flask_app/scratch_files/Aleksei.csv')

        logger.info(f'Adding {len(haro_df)} New Haros')
        pd.set_option('display.max_columns', None)
        logger.info(f'{haro_df.head(1)}')

        with app.app_context():
            addDBData(haro_df)
    except Exception:
        logger.info('\nProblem:')
        traceback.print_exc(file=sys.stdout)


