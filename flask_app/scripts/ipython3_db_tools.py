# all things are for using in ipython3

import pandas as pd
from flask_app.scripts.create_flask_app import db, app
import sqlalchemy

with app.app_context():
    journalists_df = pd.read_sql_table(f'journalists_week', db.engine)


with app.app_context():
    print(db.engine.table_names())

with app.app_context():
    jour_table = db.Table('journalists_week', db.metadata, autoload=True, autoload_with=db.engine)
    jour_table.drop(db.engine)
