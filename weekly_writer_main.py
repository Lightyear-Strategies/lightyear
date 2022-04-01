import flaskMain as fm
import pandas as pd
from weeklyWriters.muckRack.google_muckrack import google_muckrack

csv_filename = "" # TODO: add way to port csv filename from upload page
uploaded_df = pd.read_csv(csv_filename)
gm = google_muckrack(uploaded_df, 'Name')
df_with_links = gm.get_dataframe()
# upload to our muckrack_links table
df_with_links.to_sql(name='muckrack_links', con=fm.db.engine, index=False, if_exists='append')
# remove duplicates from table
whole_link_table = pd.read_sql_table(table_name='muckrack_links', con=fm.db.engine)
whole_link_table.drop_duplicates(subset=['links'], inplace=True)
whole_link_table.to_sql(name='muckrack_links', con=fm.db.engine, index=False, if_exists='replace')