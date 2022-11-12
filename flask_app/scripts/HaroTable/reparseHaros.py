# To be used from ipython3

import pandas as pd
from flask_app.scripts.create_flask_app import db, app
from flask_app.scripts.HaroTable.haro_table_functions import addDBData
from haroListener.haro_listener import HaroListener

lis = HaroListener("george@lightyearstrategies.com")
haros_list = lis.find_haro_from('2021-12-01')


def df_get(h):
    return h.get_dataframe()


df_list = list(map(df_get,haros_list))
big_df = pd.concat(df_list)

big_df.columns = big_df.columns.str.replace(' ', '')
with app.app_context():
    addDBData(big_df)


"""
# In case of this error 
# OperationalError: attempt to write a readonly database

# use in the terminal within the directory where database is located 
sudo chmod a+w Database.sqlite3 
"""

# to drop a table within Databse
#table = db.Table('haros', db.metadata, autoload=True, autoload_with=db.engine)
#table.drop(db.engine)


