'''
1. This program processes the downloaded perturbed forecast (pf) and control
forecast dataset (cf). It combines the 10 ensembles members of ECMWF's pf
with the 1 ECMWF's cf.
2. Next, the 'accumulated rainfall' datasets are converted into daily values
& re-packed to 7 dimensions[step:week:year:days:members:lat:lon] (step = lead_times,
week = "full" 2-week, days = 14 days in a 2-week, members = ensemble members). The repacked
dataset is then saved for next processing step.
3. Also the biweekly rainfall 'XXth percentile climatology mask' (bias-correct for each
grid points, for each "full" weeks and for each lead times) is generated from this re-packed dataset.
'''
import netCDF4
import numpy as np
import datetime
import os
import sys
import s2s_utility_prec
import calendar
import configparser
config = configparser.ConfigParser()
config.read('../../../../code/settings.ini')

# Define data folder
data_dir = '../../../../data/model/ecmwf/prec/'

# Initial setup
# All the initial dates with complete 14-day in 2 weeks in Dec for the 2017 runs
init_date = config.get('Download','init_date').split(',') #format needed to read .nc files
week_initial_date = ['1204','1207','1211','1214','1218']
target_month = config.getint('Process','target_month')
start_year = 1998
end_year = 2014
model_step = 3 #lead_times = 3 due to 28-day download data cap
week_hours_step = [168,336,504] #total number of hours for each corresponding week 1/2/3
days = 14 #14days = 2weeks
members = 11 #11 ensemble members
threshold = config.getint('Process','threshold') #change this value in the 'settings.ini' for your group project!

#Read ECMWF lat/lon
nc = netCDF4.Dataset(data_dir + 'ECMWF_prec_2017_daily-11-06_cf.nc')
ec_lat = nc.variables['latitude'][:]
ec_lon = nc.variables['longitude'][:]
nc.close()

# Create an array to store the repacked daily data based on lead_time 1/2/3
ec_data = np.empty([model_step,len(week_initial_date),end_year-start_year+1,days,members,len(ec_lat),len(ec_lon)]) #step,week,year,days,members,lat,lon

# For each initial date file
for i_date in range(0,len(init_date)):

    #-----------------------------------------
    # 1. Combine 10 pf members and 1 cf member
    #-----------------------------------------
    print("Processing initial date:",init_date[i_date])
    ds_pf = netCDF4.Dataset(data_dir + "ECMWF_prec_2017_daily-" + init_date[i_date] + '_pf.nc') #Load the pf file
    ds_cf = netCDF4.Dataset(data_dir + "ECMWF_prec_2017_daily-" + init_date[i_date] + '_cf.nc') #Load the cf file

    # You may want to uncomment the following lines
    # to print out the file and variable information
    #print(ds_pf.file_format)
    #print(ds_pf.dimensions.keys())
    #print(ds_pf.variables)

    # Read in the variables from cf
    prec_hd = ds_cf.variables['hdate'][:]
    prec_st = ds_cf.variables['step'][:]
    prec_lat = ds_cf.variables['latitude'][:]
    prec_lon = ds_cf.variables['longitude'][:]

    # Read in the array from pf's total precip ('tp') variable
    arr_pf = ds_pf.variables['tp'][:]
    # Read in the cf's total precip ('tp') variable
    arr_cf = ds_cf.variables['tp'][:]

    arr_shp = arr_pf.shape
    # Create a new array to accommodate the 10 pf and 1 cf members
    arr_comb = np.empty([arr_shp[0], arr_shp[1], arr_shp[2]+1, arr_shp[3], arr_shp[4]]) #year,days,members,lat,lon
    # Populate arr_comb with pf and cf data
    arr_comb[:,:,0:10,:,:] = arr_pf
    arr_comb[:,:,10,:,:] = arr_cf

    # Reverse the 'year' dimension to start from year 1998, instead of year 2014
    arr_comb = arr_comb[::-1,:,:,:,:] #Important!

    #----------------------------------------
    # 2. Calculate daily precipitation totals
    #----------------------------------------
    arr_daily = np.empty([arr_shp[0], arr_shp[1]-1, arr_shp[2]+1, arr_shp[3], arr_shp[4]]) #29days minus 1day = 28days
    for i in range(arr_shp[1]-1):
        arr_daily[:,i,:,:,:] = np.subtract(arr_comb[:,i+1,:,:,:], arr_comb[:,i,:,:,:]) #Substract to get daily totals

    #------------------------------------------------------------------
    # 2. Repack according to lead_times, "full" weeks and days' indexes
    #------------------------------------------------------------------
    model_date = init_date[i_date]
    # Create starting ec_time from filename's datetime information
    date_string = str(start_year) + '-' + model_date[:2] + '-' + model_date[-2:]
    ec_time = datetime.datetime.strptime(date_string, '%Y-%m-%d') #datetime format

    #For each model lead time
    for i_step in range(0,model_step):
        end_date = ec_time + datetime.timedelta(hours=int(week_hours_step[i_step])-24)
        start_date = end_date - datetime.timedelta(days=6)

        #Check if forecasted week is within the target month
        if start_date.month == target_month and end_date.month == target_month:

            if str("%02d"%start_date.month + "%02d"%start_date.day) in week_initial_date: #check if the data is in 'week_initial_date' range
                i_week = week_initial_date.index("%02d"%start_date.month + "%02d"%start_date.day)

                #For each day
                for i_day in range(0,days):
                    #print ('istep: ' + str(i_step))
                    #print ('iweek: ' + str(i_week))
                    #print ('iday: ' + str(i_day))
                    #print (7*(i_step+2)-days+i_day)
                    ec_data[i_step,i_week,:,i_day,:,:,:] = arr_daily[:,7*(i_step+2)-days+i_day,:,:,:] #broadcasting ,:,

    ds_pf.close()
    ds_cf.close()

#------------------------------------------------------------------------
# 3. Generate the ECMWF biweekly rainfall 'XXth percentile climatology mask'
#------------------------------------------------------------------------
print ('Preparing ECMWF biweekly rainfall ' + str(threshold) + 'th percentile climatology mask...')
ec_climatology_mask = np.empty([model_step,len(week_initial_date),len(ec_lat),len(ec_lon)])    #step,week,lat,lon
ec_climatology_mask = np.percentile(ec_data, threshold, axis=(2,3,4)) #axis2:years,axis3:14 days in 2-week,axis4:11 members
print ('Mean of ECMWF biweekly rainfall ' + str(threshold) + 'th percentile climatology mask: ' + str(np.mean(ec_climatology_mask)))
print ('Median of ECMWF biweekly rainfall ' + str(threshold) + 'th percentile climatology mask: ' + str(np.median(ec_climatology_mask)))
print ('Done!')

#--------------------------------------------------------------------------------------
# This part is to output all netCDF files (For testing/viewing in Panoply)
#--------------------------------------------------------------------------------------

#Define ECMWF output path
ec_output = '../../../../data/model/ecmwf/prec/'
ec_step = range(0,model_step)
ec_week = range(0,len(week_initial_date))
ec_year = range(start_year,end_year+1)
ec_day = range(0,days)
ec_member = range(0,members)

ec_filename = 'ECMWF_' + calendar.month_abbr[target_month] + '_Total_BiWeekly.nc'
s2s_utility_prec.write_ec_data(ec_output,ec_filename,ec_data,ec_step,ec_week,ec_year,ec_day,ec_member,prec_lat,prec_lon,'Total')
print('File saved! ' + ec_filename + ' to directory ' + ec_output)

ec_filename = 'ECMWF_' + calendar.month_abbr[target_month] + '_threshold' + str(threshold) + '_Climatology_Mask_BiWeekly.nc'
s2s_utility_prec.write_ec_data(ec_output,ec_filename,ec_climatology_mask,ec_step,ec_week,ec_year,ec_day,ec_member,prec_lat,prec_lon,'Climatology')
print('File saved! ' + ec_filename + ' to directory ' + ec_output)

#-------------------------------------------------------------------------------------
# 3. This part is to output and display ECMWF Rainfall XXth percentile climatology mask
#-------------------------------------------------------------------------------------

#Choose to display data
plot_figure = True

#Define plot folder
plot_dir = '../../../../plot/model/'
target_week = config.getint('Plot','target_week')

if plot_figure == True:
   #Define the domain for display
   lat_down = config.getint('Plot','lat_down')
   lat_up = config.getint('Plot','lat_up')
   lon_left = config.getint('Plot','lon_left')
   lon_right = config.getint('Plot','lon_right')
   grid_lat = config.getint('Plot','grid_lat')
   grid_lon = config.getint('Plot','grid_lon')

   prec_lat = prec_lat[::-1]    #reverse lat for matplotlib's plotting convention

   #Plot ECMWF biweekly Rainfall XXth percentile climatology mask
   for i_step in range(0,model_step):
       start_date = week_initial_date[target_week]
       end_date = "%02d"%target_month + "%02d"%(int(start_date[-2:])+13)

       data_range = [0,int(np.max(ec_climatology_mask))]    #change data range for plotting accordingly
       title_str = 'ECMWF Biweekly Rainfall ' + str(threshold) + 'th Percentile Climatology' + '\n' + start_date + '-' + end_date + ' (LT' + str(i_step+1) + ')'
       name_str = plot_dir + 'ECMWF_' + start_date + '-' + end_date + '_' + 'LT' + str(i_step+1) + '_threshold' + str(threshold) + '_Climatology_Mask_BiWeekly.png'
       #reverse lat for matplotlib's plotting convention
       s2s_utility_prec.plot_processing(ec_climatology_mask[i_step,target_week,::-1,:],prec_lat,prec_lon,lat_down,lat_up,lon_left,lon_right,grid_lat,grid_lon,data_range,title_str,name_str,'Climatology_Mask')
