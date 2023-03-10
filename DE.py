#### Cloning the data
import os
import csv
import json
import pandas as pd
from sqlalchemy import create_engine
import pymysql
import warnings
import mysql.connector

warnings.simplefilter(action='ignore', category=RuntimeWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)

# Clone the repository using Git
os.system("git clone https://github.com/PhonePe/pulse.git")

# Change to the repository directory
os.chdir("pulse/data")


####  fetching the transaction data from aggregated
print(1)
import pandas as pd
import os
import json
# The root directory to start searching for files
root_dir = "D:\\IITM\\project\\PhonePe\\pulse\\data\\aggregated\\transaction\\country\\india"

# List to store the full path of all the files
files = []
df=pd.DataFrame()
fdf=pd.DataFrame()
agg_trans = pd.DataFrame()
# Iterate through all the subdirectories and files in the root directory
i=0
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        # Add the full path of each file to the list
        fp = os.path.join(dirpath, filename)
        if fp.endswith('.json'):
          files.append(os.path.join(dirpath, filename, ))
          data=pd.read_json(fp)
        #   print(data)

          # print(data)
          # tf = pd.read_json(fp)
          # # tf = pd.json_normalize(tf)
          # tf['path']=fp
          # # print(tf)
          # df = df.append(tf)
          # i=i+1
          fp_split = fp.split("\\")
          cnt = 0
          n_country =None
          n_state =None
          n_year =None
          for fp_sp in fp_split:
            cnt = cnt+1
            if fp_sp=="country":
              n_country = fp_split[cnt]
            if fp_sp=="state":
              n_state = fp_split[cnt]
          n_year=fp_split[-2]
          n_qtr=fp_split[-1].replace(".json", "")
          df = pd.json_normalize(data['data']['transactionData'], record_path=['paymentInstruments'], meta=['name'])
          df['from'] = pd.to_datetime(data['data']['from'],unit='ms')
          df['to'] = pd.to_datetime(data['data']['to'],unit='ms')
          df['no_of_days'] = (df['to']-df['from']).dt.days
          # df['fp']=fp
          df['country'] =n_country
          df['state'] =n_state
          df['year'] =n_year
          df['qtr'] =n_qtr
          agg_trans = agg_trans.append(df)
agg_trans = agg_trans.reindex(columns=['from','to','no_of_days','country','state','year','qtr','name','type','count','amount'])
agg_trans.to_csv("agg_tran.csv")


##### fetching the user data from aggregated
print(2)
root_dir = "D:\\IITM\\project\\PhonePe\\pulse\\data\\aggregated\\user\\country\\india"


# List to store the full path of all the files
files = []
cnt=0
df=pd.DataFrame()
fdf=pd.DataFrame()
agg_user = pd.DataFrame()
# Iterate through all the subdirectories and files in the root directory
i=0
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        # Add the full path of each file to the list
        fp = os.path.join(dirpath, filename)
        # print(fp)
        if fp.endswith('.json'):
          files.append(os.path.join(dirpath, filename, ))
          fp_split = fp.split("\\")
          cnt = 0
          n_country =None
          n_state =None
          n_year =None
          for fp_sp in fp_split:
            cnt = cnt+1
            if fp_sp=="country":
              n_country = fp_split[cnt]
            if fp_sp=="state":
              n_state = fp_split[cnt]
          n_year=fp_split[-2]
          n_qtr=fp_split[-1].replace(".json", "")
          # print(fp)
          f1=pd.read_json(fp)
          # print(f1)
          cnt=cnt+1
          # print(cnt)
          try:
            df = pd.json_normalize(f1['data']['usersByDevice'])
          except NotImplementedError or KeyError:
            df = pd.DataFrame([{'brand':None, 'count':None, 'percentage':None}])
          try:
            df['registeredUsers'] = f1['data']['aggregated']['registeredUsers']
          except KeyError:
            df['registeredUsers'] = ''
          try:
            df['appOpens'] = f1['data']['aggregated']['appOpens']
          except KeyError:
            df['appOpens'] = ''
          try:
            df['responseTimestamp'] = f1['responseTimestamp'][0]
          except KeyError:
            df['responseTimestamp'] = ''
          df
          df['country'] =n_country
          df['state'] =n_state
          df['year'] =n_year
          df['qtr'] =n_qtr
          agg_user = agg_user.append(df)
agg_user.to_csv("agg_user.csv")


##### fetching the transaction data from map
print(3)
root_dir = "D:\\IITM\\project\\PhonePe\\pulse\\data\\map\\transaction\\hover\\country\\india"

# List to store the full path of all the files
files = []
df=pd.DataFrame()
fdf=pd.DataFrame()
map_trans = pd.DataFrame()
# Iterate through all the subdirectories and files in the root directory
i=0
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        # Add the full path of each file to the list
        fp = os.path.join(dirpath, filename)
        if fp.endswith('.json'):
          files.append(os.path.join(dirpath, filename, ))
          data=pd.read_json(fp)
          # print(data)
          # tf = pd.read_json(fp)
          # # tf = pd.json_normalize(tf)
          # tf['path']=fp
          # # print(tf)
          # df = df.append(tf)
          # i=i+1
          fp_split = fp.split("\\")
          cnt = 0
          n_country =None
          n_state =None
          n_year =None
          for fp_sp in fp_split:
            cnt = cnt+1
            if fp_sp=="country":
              n_country = fp_split[cnt]
            if fp_sp=="state":
              n_state = fp_split[cnt]

          n_year=fp_split[-2]
          n_qtr=fp_split[-1].replace(".json", "")
          df = pd.json_normalize(data['data']['hoverDataList'], record_path=['metric'], meta=['name'])
          df['country'] =n_country
          df['state'] =n_state
          df['year'] =n_year
          df['qtr'] =n_qtr
          df['responseTimestamp'] = data['responseTimestamp'][0]
          map_trans = map_trans.append(df)
map_trans = map_trans.rename(columns={'name':'district'})
map_trans['district'] = map_trans['district'].str.replace('district', '')
# fdf = fdf.reindex(columns=['from','to','no_of_days','country','state','year','qtr','name','type','count','amount'])

# print(df)


map_trans.to_csv("map_trans.csv")

##### fetching the user data from map
print(4)
root_dir = "D:\\IITM\\project\\PhonePe\\pulse\\data\\map\\user\\hover\\country\\india"

# List to store the full path of all the files
files = []
cnt=0
df=pd.DataFrame()
fdf=pd.DataFrame()
map_user = pd.DataFrame()
# Iterate through all the subdirectories and files in the root directory
i=0
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        # Add the full path of each file to the list
        fp = os.path.join(dirpath, filename)
        # print(fp)
        if fp.endswith('.json'):
          files.append(os.path.join(dirpath, filename, ))
          fp_split = fp.split("\\")
          cnt = 0
          n_country =None
          n_state =None
          n_year =None
          for fp_sp in fp_split:
            cnt = cnt+1
            if fp_sp=="country":
              n_country = fp_split[cnt]
            if fp_sp=="state":
              n_state = fp_split[cnt]
          n_year=fp_split[-2]
          n_qtr=fp_split[-1].replace(".json", "")
          # print(fp)
          with open(fp, 'r') as f:
              data = f.read()
          # Load the JSON data into a dictionary
          d = json.loads(data)
          # Create an empty DataFrame
          df = pd.DataFrame(columns=['location', 'registeredUsers', 'appOpens', 'responseTimestamp'])
          # Iterate over the dictionary and add the data to the DataFrame
          for location, values in d['data']['hoverData'].items():
              registered_users = values.get('registeredUsers', 0)
              app_opens = values.get('appOpens', 0)
              response_timestamp = d['responseTimestamp']
              df = df.append({'location': location, 'registeredUsers': registered_users, 'appOpens': app_opens, 'responseTimestamp': response_timestamp}, ignore_index=True)
          df['country'] =n_country
          df['state'] =n_state
          df['year'] =n_year
          df['qtr'] =n_qtr
          map_user = map_user.append(df)
map_user.to_csv("map_user.csv")

##### fetching lat_long
print(5)
from geopy.geocoders import Nominatim

# getting the lat_long
geolocator = Nominatim(user_agent="my-app")

def fetch_lat_long(location):
    try:
        loc = geolocator.geocode(location)
        return (loc.latitude, loc.longitude)
    except:
        return None
    
unique_values  = map_trans[['country', 'state', 'district']].apply(lambda x: tuple(x), axis=1).unique()
m_locations = pd.DataFrame(list(unique_values), columns=['country', 'state', 'district'])
m_locations["lat_long"] = m_locations.apply(lambda x: fetch_lat_long(f'{x["district"]}, {x["state"]}, {x["country"]}'), axis=1)
m_locations["lat_long"] = m_locations["lat_long"].astype(str)
m_locations

