import pandas as pd
import flaskMain as fm
from haroListener.haro_listener import HaroListener


lis = HaroListener('george@lightyearstrategies.com')

haros_list = lis.find_haro_from('2021-12-01')

def df_getter(h):
    return h.get_dataframe()

df_list = list(map(df_getter, haros_list))

big_df = pd.concat(df_list)
print(big_df)
big_df.drop_duplicates(subset=['Summary'], inplace=True)
print(big_df)
big_df.reset_index(drop=True, inplace=True)
print(big_df)

big_df.to_sql('haros', con=fm.db.engine, index=True, if_exists='replace')
