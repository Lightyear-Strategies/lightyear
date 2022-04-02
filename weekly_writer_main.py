import flaskMain as fm
import pandas as pd
from weeklyWriters.muckRack.google_muckrack import google_muckrack

csv_filename = "" # TODO: add way to port csv filename from upload page
uploaded_df = pd.read_csv(csv_filename)
# TODO: write uniform column name function
gm = google_muckrack(uploaded_df, 'Name')
df_with_links = gm.get_dataframe()
# upload to our muckrack_links table
df_with_links.to_sql(name='muckrack_links', con=fm.db.engine, index=False, if_exists='append')