# To be used from root directory

import pandas as pd
from flask_app.scripts.create_flask_app import db, app
from haroListener.haro_listener import HaroListener

lis = HaroListener("george@lightyearstrategies.com")
haros_list = lis.find_haro_from('2021-12-01')


def df_get(h):
    return h.get_dataframe()


df_list = list(map(df_get,haros_list))
big_df = pd.concat(df_list)

big_df.columns = big_df.columns.str.replace(' ', '')
big_df.drop_duplicates(subset=['Summary'], inplace=True)
big_df.reset_index(drop=True,inplace=True)

with app.app_context():
    big_df.to_sql(name='haros', con=db.engine, index=True, if_exists='replace')

#addDBData(big_df)


"""
# In case of this error 
# OperationalError: attempt to write a readonly database

# use in the terminal within the directory where database is located 
sudo chmod a+w Database.sqlite3 
"""

# to drop a table within Databse
#table = db.Table('haros', db.metadata, autoload=True, autoload_with=db.engine)
#table.drop(db.engine)


