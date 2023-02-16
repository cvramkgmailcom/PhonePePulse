##### updating all 5 dataframes into mysql database as tables
print(6)
import pandas as pd
from sqlalchemy import create_engine
import pymysql
# Create a DataFrame
# Create a connection to the MySQL database
engine = create_engine('mysql+pymysql://rk:rk123@localhost/guvi_phonePe')
# Insert the DataFrame into a MySQL table
print('started')
print("agg_trans..")
agg_trans.to_sql(name='agg_trans', con=engine, if_exists='replace', index=False)
print('agg_user..')
agg_user.to_sql(name='agg_user', con=engine, if_exists='replace', index=False)
print('map_trans...')
map_trans.to_sql(name='map_trans', con=engine, if_exists='replace', index=False)
print('map_user...')
map_user.to_sql(name='map_user', con=engine, if_exists='replace', index=False)
print('map_location...')
m_locations.to_sql(name='m_locations', con=engine, if_exists='replace', index=False)
