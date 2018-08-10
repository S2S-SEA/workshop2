'''
Plot out the time series for dry days anomaly over the years for TRMMM and ECMWF model data for particular region
All 4 lead times are included in the plot for the ECMWF model data
'''

import numpy
import calendar
from scipy import interpolate
import plot_timeseries
import configparser
config = configparser.ConfigParser()
config.read('../../../../code/settings.ini')

#Initial setup
week_initial_date = config.get('Process','week_initial_date').split(',')
target_month      = config.getint('Process','target_month')
start_year        = 1998
end_year          = 2014
lead_times        = 4
threshold         = config.getint('Process','threshold')

#Define the week for display, can be changed
target_week = 0    # week number starting from 0
#Define the domain for display, can be changed
lat_down    = -20
lat_up      = -10
lon_left    = 110
lon_right   = 120

#---------------------------------------------------
#This part is to prepare TRMM and ECMWF anomaly data
#---------------------------------------------------

#Define TRMM input path
trmm_input    = '../../../../data/obs/prec'
trmm_filename = 'TRMM_' + calendar.month_abbr[target_month] + '_threshold' + str(threshold) + '_Anomaly_Weekly_EC_res.nc'
cur_trmm_path = trmm_input + '/' + trmm_filename

#Define ECMWF input path
ec_input    = '../../../../data/model/ecmwf/prec'
ec_filename = 'ECMWF_' + calendar.month_abbr[target_month] + '_threshold' + str(threshold) + '_Anomaly_Weekly.nc'
cur_ec_path = ec_input + '/' + ec_filename

#Read TRMM and ECMWF data
trmm_lat,trmm_lon,trmm_anomaly = plot_timeseries.read_anomaly(cur_trmm_path,'TRMM')
ec_lat,ec_lon,ec_anomaly       = plot_timeseries.read_anomaly(cur_ec_path,'ECMWF')

#-----------------------------------------------------
#This part is to display the time series for anomalies
#-----------------------------------------------------
#Plot time series
start_date = week_initial_date[target_week]
print(start_date)
end_date   = "%02d"%(int(start_date[-2:])+6)
title_str  = 'Number of Dry Days, Anomaly: Time Series' + '\n' + start_date + '-' + end_date
name_str   = 'ECMWF_DryDays_Timeseries_' + start_date + '-' + end_date + '.png'
plot_timeseries.plot_fig(trmm_anomaly,ec_anomaly,target_week,start_year,end_year,ec_lat,ec_lon,lat_down,lat_up,lon_left,lon_right,title_str,name_str)

print('Finished!')
