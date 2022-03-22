import flaskMain as fm
import haroListener.haro_listener as hl
import pandas as pd

def df_getter(haro):
    return haro.get_dataframe()
lis = hl.HaroListener('george@lightyearstrategies.com')

haros_list = lis.find_haro_from('2021-12-03')
df_list = list(map(df_getter, haros_list))
big_df = pd.concat(df_list)

fm.addDBData(big_df)