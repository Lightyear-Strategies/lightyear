from flask_app.scripts.HaroTable.haro_table_functions import addDBData
from haroListener.haro_listener import HaroListener
from flaskMain import app

import logging
import sys
from logging import StreamHandler, Formatter

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)


if __name__ == "__main__":
    hl = HaroListener('george@lightyearstrategies.com')
    logger.info('1')
    recent_haro = hl.find_haro_from()[0]
    logger.info('2')
    haro_df = recent_haro.get_dataframe()
    logger.info('3')
    with app.app_context():
        logger.info('4')
        addDBData(haro_df)

