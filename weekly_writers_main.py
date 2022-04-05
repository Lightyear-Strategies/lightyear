import flaskMain as fm
from weeklyWriters.muckRack import google_muckrack as gm, Muckrack as mr
import sys
import pandas as pd

journalists_db = journalists = pd.read_sql_table('journalists', fm.db.engine)

if sys.argv[1] == "links":
    links_needed = journalists_db[journalists_db['Muckrack'].isnull()]
    gm_ob = gm.google_muckrack(links_needed, 'Journalist')
    new_df = gm_ob.get_dataframe()
    journalists_db[journalists_db['Muckrack'].isnull()] = new_df
    journalists_db.to_sql('journalists', fm.db.engine, index=False, if_exists='replace')

if sys.argv[1] == "parse":
    # TODO: PARSING
    grouped = journalists_db.groupby('ClientEmail', axis=0)
    print(journalists_db)