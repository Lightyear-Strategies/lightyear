from flask_app.scripts.HaroTable.haro_table_functions import addDBData
from haroListener.haro_listener import HaroListener
from flaskMain import app
import pandas as pd

import logging
import sys
from logging import StreamHandler, Formatter

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)


if __name__ == "__main__":
    # hl = HaroListener('george@lightyearstrategies.com')
    # recent_haro = hl.find_haro_from()[0]
    # haro_df = recent_haro.get_dataframe()

    haro_df = pd.read_csv('Aleksei.csv')

    # Debugging
    #haro_df.head(1).to_csv('Aleksei.csv')

    logger.info(f'Adding {len(haro_df)} New Haros')
    pd.set_option('display.max_columns', None)
    logger.info(f'{haro_df.head(1)}')

    with app.app_context():
        #logger.info('4')
        addDBData(haro_df)

# data = {'Summary ':'Short comings of DNA testing', 'Name':'Ameya Paleja','Category':'Biotech and Healthcare',
#         'Email':'query-e1yp@helpareporter.net', 'MediaOutlet':'Interesting Engineering', 'Deadline':'7:00 PM EST',
#         'Query':'What are the shortcomings of DNA testing for p', 'Requirements':'Experts with testing experience Experts with D',
#         'DateReceived':'2022-07-07 ','Used':None,'TimeStamp':' 1.657141e+09'
#         }

