import pandas as pd
import flaskMain as fm
from haroListener.haro_listener import HaroListener

lis = HaroListener('george@lightyearstrategies.com')

haros_list = lis.find_haro_from('2021-12-01')

def df_getter(h):
    return h.get_dataframe()

df_list = list(map(df_getter, haros_list))

big_df = pd.concat(df_list)

fm.addDBData(big_df)
