from flask_app.scripts.HaroTable.haro_table_functions import addDBData
from haroListener.haro_listener import HaroListener

if __name__ == "__main__":
    hl = HaroListener('george@lightyearstrategies.com')
    recent_haro = hl.find_haro_from()[0]
    haro_df = recent_haro.get_dataframe()
    addDBData(haro_df)

