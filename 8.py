#getting omega values from a netCDF file for a special domain with definit latitudes and longitudes, between special layers and showing them in csv format.

from netCDF4 import num2date
import cftime
import netCDF4
import numpy as np
import pandas as pd
from netCDF4 import Dataset

#omega.mon.mean.nc from https://downloads.psl.noaa.gov/Datasets/ncep.reanalysis.derived/pressure/omega.mon.mean.nc

f = Dataset ('/home/lida/Desktop/omega.mon.mean/omega.mon.mean.nc')

omega = f.variables['omega']
time = f.variables ['time']
level = f. variables['level']
latitudes = f.variables ['lat']
longitudes = f.variables ['lon']

time = num2date (time[:], units=time.units)
'''print(time)
if time[-1]==cftime.DatetimeGregorian(2021, 5,1):
    print('yes')'''

#omega.mon.mean.nc contains monthly mean of omega value so in DatetimeGregorian we write (year,month,mean) that for this file, the mean value is always equal to 1 (Generally in DatetimeGregorian we should write (year,month,day)).

def domain_bounderies(year, month, mean,lev1, lev2, lat1, lat2, lon1, lon2):
    
    lat_b = latitudes[:]>=lat1
    lat_s = latitudes[:]<=lat2
    lat = [a and b for a, b in zip(lat_b, lat_s)]

    lev_b = level[:]>=lev1
    lev_s = level[:]<=lev2
    lev = [a and b for a, b in zip(lev_b, lev_s)]

    times = time[:] == cftime.DatetimeGregorian(year,month,mean)
       
    lon_b = longitudes[:]>=lon1
    lon_s = longitudes[:]<=lon2
    lon = [a and b for a, b in zip(lon_b, lon_s)]

    times_grid, levels_grid, latitudes_grid, longitudes_grid = [x.flatten() for x in np.meshgrid(time[times], level[lev], latitudes[lat], longitudes[lon], indexing='xy')]

    df = pd.DataFrame({'time':times_grid,'level':levels_grid, 'latitude': latitudes_grid,'longitude': longitudes_grid,'omega': omega[times,lev,lat,lon].flatten()})

   #df.to_csv('/home/lida/Desktop/table.csv', index=False)  
    print('Done')
   #return df.to_csv'''
    return df

for month in range (2,10):     # 12 months in range (1,13) 
    
    latlon_value = domain_bounderies(2021,month,1, 100,1000,35,36,50,53)
    
    #getting omega values in distinct csv format files related to every month
    
    latlon_value.to_csv('/home/lida/Desktop/2021'+str(month)+'.csv', index=False) 
    
 
