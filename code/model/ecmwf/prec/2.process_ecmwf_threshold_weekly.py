'''
1. Load the 'weekly rainfall XXth percentile climatology mask' and 'ECMWF_Total_Weekly'
netCDF files.
2. Calculate 'NDD' in the 1-week' from the 'ECMWF_Total_Weekly' dataset,
by applying the 'Weekly Rainfall XXth percentile climatology mask and summing up the
total number of dry/wet days in each week.
3. Output/Plot the 'NDD/NWD' in the 1-week for ECMWF climatology/total/anomaly.
'''
import datetime
import numpy as np
import netCDF4
import calendar
import s2s_utility_prec
import configparser
config = configparser.ConfigParser()
config.read('../../../../code/settings.ini')

#Initial setup
week_initial_date = config.get('Process','week_initial_date').split(',')
target_month = config.getint('Process','target_month')
start_year = 1998
end_year = 2014
model_step = 4
days = 7
members = 11 #11 ensemble members
threshold = config.getint('Process','threshold')

#Define ECMWF input data folder
ec_input = '../../../../data/model/ecmwf/prec'

#--------------------------------------------------------------------------------------------------
# 1. Load the two netCDF4 files: 'ECMWF_Total_Weekly' and 'Rainfall XXth percentile climatology mask'
#--------------------------------------------------------------------------------------------------

#Read 'ECMWF_Total_Weekly' data
cur_ec_filename = 'ECMWF_' + calendar.month_abbr[target_month] + '_Total_Daily.nc'
cur_ec_path = ec_input + '/' + cur_ec_filename
ec_lat_weekly,ec_lon_weekly,ec_data = s2s_utility_prec.read_method(cur_ec_path,'ECMWF_Total')

#Read 'Rainfall XXth percentile climatology mask' data
cur_ec_filename = 'ECMWF_' + calendar.month_abbr[target_month] + '_threshold' + str(threshold) + '_Climatology_Mask_Weekly.nc'
cur_ec_path = ec_input + '/' + cur_ec_filename
ec_lat_mask,ec_lon_mask,ec_climatology_mask = s2s_utility_prec.read_method(cur_ec_path,'ECMWF_Mask')

#---------------------------------------------------------------------------------------------
# 2. This part is to calculate ECMWF (NDD) in a week [climatology/total/anomaly]
#---------------------------------------------------------------------------------------------

#Convert based on the ECMWF weekly 'Rainfall XXth percentile climatology mask' with minimum value of XXmm/day (XX=dynamic?)
ec_climatology_mask[ec_climatology_mask < 1] = 1

for i_year in range(0,end_year-start_year+1):
    for i_member in range(0,members):
        for i_day in range(0,days):
            ec_data[:,:,i_year,i_day,i_member,:,:] = (ec_data[:,:,i_year,i_day,i_member,:,:] < ec_climatology_mask).astype(np.int_)

#Sum up all 7 days in a week and compress the 'days' axis
ec_total_ens = np.sum(ec_data,axis=3) #use np.sum along axis3

#Average over the 'ensemble member' axis
ec_total_ens_avg = np.mean(ec_total_ens,axis=3)
ec_climatology = np.mean(ec_total_ens_avg,axis=2) #Obtain # of dry day in the week climatology by averaging over 'year' axis

ec_anomaly = np.empty([model_step,len(week_initial_date),end_year-start_year+1,len(ec_lat_weekly),len(ec_lon_weekly)])
for i_year in range(0,end_year-start_year+1):
    ec_anomaly[:,:,i_year,:,:] = ec_total_ens_avg[:,:,i_year,:,:] - ec_climatology

#--------------------------------------------------------------------------
#2. This part is to output and display ECMWF NDD climatology/total/anomaly
#--------------------------------------------------------------------------

#Define ECMWF output path and plot path
ec_output = '../../../../data/model/ecmwf/prec/'
plot_dir = '../../../../plot/model/'

#Choose to output or display data
data_output = True
plot_figure = True

if data_output == True:
   #Output ECMWF climatology/total/anomaly
   ec_step = range(0,model_step)
   ec_week = range(0,len(week_initial_date))
   ec_year = range(start_year,end_year+1)

   ec_filename = 'ECMWF_' + calendar.month_abbr[target_month] + '_threshold' + str(threshold) + '_Climatology_Weekly.nc'
   s2s_utility_prec.write_ec(ec_output,ec_filename,ec_climatology,ec_step,ec_week,ec_year,ec_lat_weekly,ec_lon_weekly,'Climatology')

   ec_filename = 'ECMWF_' + calendar.month_abbr[target_month] + '_threshold' + str(threshold) + '_Total_Weekly.nc'
   s2s_utility_prec.write_ec(ec_output,ec_filename,ec_total_ens_avg,ec_step,ec_week,ec_year,ec_lat_weekly,ec_lon_weekly,'Total')

   ec_filename = 'ECMWF_' + calendar.month_abbr[target_month] + '_threshold' + str(threshold) + '_Anomaly_Weekly.nc'
   s2s_utility_prec.write_ec(ec_output,ec_filename,ec_anomaly,ec_step,ec_week,ec_year,ec_lat_weekly,ec_lon_weekly,'Anomaly')

if plot_figure == True:
   #Define target week and year
   target_week = config.getint('Plot','target_week')    #week number starting from 0
   target_year = config.getint('Plot','target_year')

   #Define the domain for display
   lat_down = config.getint('Plot','lat_down')
   lat_up = config.getint('Plot','lat_up')
   lon_left = config.getint('Plot','lon_left')
   lon_right = config.getint('Plot','lon_right')
   grid_lat = config.getint('Plot','grid_lat')
   grid_lon = config.getint('Plot','grid_lon')

#   ec_lat_weekly = ec_lat_weekly[::-1]    #reverse lat for matplotlib's plotting convention

   #Plot ECMWF NDD/NWD climatology/total/anomaly
   for i_step in range(0,model_step):
       start_date = week_initial_date[target_week]
       end_date = "%02d"%target_month + "%02d"%(int(start_date[-2:])+6)

       data_range = [0,7]    #change data range for plotting accordingly
       title_str = 'ECMWF ' + '_NDD_' + ' Weekly Climatology' + '\n' + start_date + '-' + end_date + ' (LT' + str(i_step+1) + ')'
       name_str = plot_dir + 'ECMWF_' + start_date + '-' + end_date + '_' + 'LT' + str(i_step+1) + '_threshold' + str(threshold) + '_Climatology_Weekly_.png'
       s2s_utility_prec.plot_processing(ec_climatology[i_step,target_week,:,:],ec_lat_weekly,ec_lon_weekly,lat_down,lat_up,lon_left,lon_right,grid_lat,grid_lon,data_range,title_str,name_str,'Climatology')

       data_range = [0,7]
       title_str = 'ECMWF ' + '_NDD_' + '  Weekly Total' + '\n' + str(target_year) + ' ' + start_date + '-' + end_date + ' (LT' + str(i_step+1) + ')'
       name_str = plot_dir + 'ECMWF_' + str(target_year) + '_' + start_date + '-' + end_date + '_' + 'LT' + str(i_step+1) + '_threshold' + str(threshold) + '_Total_Weekly.png'
       s2s_utility_prec.plot_processing(ec_total_ens_avg[i_step,target_week,target_year-start_year,:,:],ec_lat_weekly,ec_lon_weekly,lat_down,lat_up,lon_left,lon_right,grid_lat,grid_lon,data_range,title_str,name_str,'Total')

       data_range = [-7,7]
       title_str = 'ECMWF ' + '_NDD_' + ' Weekly Anomaly' + '\n' + str(target_year) + ' ' + start_date + '-' + end_date + ' (LT' + str(i_step+1) + ')'
       name_str = plot_dir + 'ECMWF_' + str(target_year) + '_' + start_date + '-' + end_date + '_' + 'LT' + str(i_step+1) + '_threshold' + str(threshold) + '_Anomaly_Weekly.png'
       s2s_utility_prec.plot_processing(ec_anomaly[i_step,target_week,target_year-start_year,:,:],ec_lat_weekly,ec_lon_weekly,lat_down,lat_up,lon_left,lon_right,grid_lat,grid_lon,data_range,title_str,name_str,'Anomaly')
