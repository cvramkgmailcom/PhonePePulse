import pandas as pd
from sqlalchemy import create_engine
import pymysql
# Create a DataFrame
# Create a connection to the MySQL database
engine = create_engine('mysql+pymysql://rk:rk123@localhost/guvi_phonePe')
# Insert the DataFrame into a MySQL table
agg_trans.to_sql(name='agg_trans', con=engine, if_exists='replace', index=False)
agg_user.to_sql(name='agg_user', con=engine, if_exists='replace', index=False)
map_trans.to_sql(name='map_trans', con=engine, if_exists='replace', index=False)
map_user.to_sql(name='map_user', con=engine, if_exists='replace', index=False)
