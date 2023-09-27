import pandas as pd
from points import *
import json
from dotenv import load_dotenv
import os

load_dotenv()
MAPS_API_KEY=os.getenv("MAPS_API_KEY")

path = './Allpoints.csv'
ndf = pd.read_csv(path)

pdf = pd.DataFrame(columns=['panoid','lat','lon','year','month','lat_og','lon_og'])
err_arr = []

for i in range(100000):
    lo = ndf.x[i]
    la = ndf.y[i]
    if panoids(la,lo, MAPS_API_KEY) is not None:
        try:
            df = pd.DataFrame(panoids(la,lo, MAPS_API_KEY)).fillna(0)
            df['lat_og'] = df['lat']
            df['lon_og'] = df['lon']
            df.loc[df['year'] != 0, 'lat_og'] = la
            df.loc[df['year'] != 0, 'lon_og'] = lo
            pdf = pd.concat([pdf,df]).drop_duplicates().reset_index(drop=True)
        except:
            err_arr.append(i)
            continue
            
with open('err_arr.txt', 'w') as filehandle:
    json.dump(err_arr, filehandle)
    
pdf.to_csv('./AllPanoids.csv')