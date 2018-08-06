'''
This list functions use in the workshop practical.

Each function starts with 'def' followed by the name of the function then round brackets containing any of the variable names

'''
#Only one library is needed for this function
import netCDF4



def read_trmm(cur_trmm_path):
#This file reads TRMM data downloaded from IRI datalibrary into python. 
#It requires the name of the file (including path if contained in a different folder) 
#The function returns the coordinate variables time, latitude, longitude, and the trmm precipitation data. 

    #Open TRMM path to retreive data
    nc = netCDF4.Dataset(cur_trmm_path)

    #Read TRMM time, latitude and longitude and data
    time_var = nc.variables['T']
    data_time = netCDF4.num2date(time_var[:],time_var.units)
    trmm_lat = nc.variables['Y'][:]
    trmm_lon = nc.variables['X'][:]
    trmm_data = nc.variables['precipitation'][:]    #time,lat,lon

    #Store TRMM time 
    trmm_time = []
    for i in range(0,len(data_time)):
        trmm_time.append(data_time[i])

    return trmm_time,trmm_lat,trmm_lon,trmm_data
    nc.close()

def final_message():

      message = 'This example provides similar results to ncdump. See, there is more than one way to skin a cat.'
      return message