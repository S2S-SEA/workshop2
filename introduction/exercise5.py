'''
Exercise 5. Debug the script
Note that there are no errors in the example_function file. 
'''

import example_function as ex


trmm_path = 'start/data3.nc'
trmm_file = 'data3.nc'


time, lat, lon, precip = ex.read_trmm(trmm_path, trmm_file)

print(time(0))
print(time[-1])


print(ex.final_message())