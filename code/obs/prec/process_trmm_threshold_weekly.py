import datetime
import numpy as np
import netCDF4
import calendar
from scipy import interpolate
import s2s_utility_prec
import configparser
config = configparser.ConfigParser()
config.read('../../../code/settings.ini')

#Initial setup
week_initial_date = config.get('Process','week_initial_date').split(',')
target_month = config.getint('Process','target_month')
days = 7
start_year = 1998
end_year = 2014
threshold = config.getint('Process','threshold') #change this value in the 'settings.ini' for your group project!
method = config.get('Process','method') #NDD=Dry NWD=Wet

#Define TRMM input path
trmm_input = '../../../data/obs/prec'
trmm_filename = 'TRMM_Daily_' + calendar.month_abbr[target_month] + '_1998-2014.nc'
cur_trmm_path = trmm_input + '/' + trmm_filename

#Read TRMM dataset
trmm_time,trmm_lat,trmm_lon,trmm_data = s2s_utility_prec.read_trmm(cur_trmm_path)

#--------------------------------------------------------------------------------------
# 1. Interpolate TRMM resolution(0.25deg x 0.25deg) to ECMWF resolution(1.5deg x 1.5deg)
#--------------------------------------------------------------------------------------
#Define ECMWF input path
ec_input = '../../../data/model/ecmwf/prec'

#Read ECMWF data lat/lon
nc = netCDF4.Dataset(ec_input + '/' + 'ECMWF_prec_2017_daily-11-06_cf.nc')
ec_lat_0 = nc.variables['latitude'][:]
ec_lat = ec_lat_0[::-1]    #reverse lat
ec_lon = nc.variables['longitude'][:]
nc.close()

#Interpolate TRMM resolution to ECMWF resolution
trmm_data_ec_resol = np.empty([trmm_data.shape[0],len(ec_lat),len(ec_lon)])
for i in range(0,trmm_data.shape[0]):
    pi = interpolate.interp2d(trmm_lon,trmm_lat,trmm_data[i,:,:])
    trmm_data_ec_resol[i,:,:] = pi(np.asarray(ec_lon),np.asarray(ec_lat))

#-------------------------------------------------------------------------------------
# 2. Repack TRMM daily rainfall to 5 dimensions (week_initial_date:years:days:lat:lon)
#-------------------------------------------------------------------------------------
trmm_data_repack = np.empty([len(week_initial_date),end_year-start_year+1,days,len(ec_lat),len(ec_lon)]) #week,year,day,lat,lon

#For each week initial date
for i_date in range(0,len(week_initial_date)):
    week_date = week_initial_date[i_date]
    #print (week_date)

    #For each year
    for i_year in range(0,end_year-start_year+1):
        cur_date = datetime.datetime(i_year+start_year,int(week_date[:2]),int(week_date[-2:]),12)
        #print (cur_date)
        time_index = trmm_time.index(cur_date)

        #For each day (7 days in a week)
        for i_day in range(0,days):
            #print (time_index+i_day)
            trmm_data_repack[i_date,i_year,i_day,:,:] = trmm_data_ec_resol[time_index+i_day,:,:] #broadcasting ,:,

#---------------------------------------------------------------------
# 3. Generating TRMM weekly rainfall 'XXth percentile climatology mask'
#---------------------------------------------------------------------
print ('Preparing TRMM weekly rainfall ' + str(threshold) + 'th percentile climatology mask...')
trmm_climatology_mask = np.empty([len(week_initial_date),len(ec_lat),len(ec_lon)])
trmm_climatology_mask = np.percentile(trmm_data_repack, threshold, axis=(1,2)) #axis1:years axis2:7 days in a week
print ('Mean of TRMM weekly rainfall ' + str(threshold) + 'th percentile climatology mask: ' + str(np.mean(trmm_climatology_mask)))
print ('Median of TRMM weekly rainfall ' + str(threshold) + 'th percentile climatology mask: ' + str(np.median(trmm_climatology_mask)))
print ('Done!')

#--------------------------------------------------------------------------------
# 4. This part is to calculate TRMM NDD/NWD in a week (climatology/total/anomaly)
#--------------------------------------------------------------------------------
if method == 'NDD':
    #Convert based on the TRMM weekly 'Rainfall XXth percentile climatology mask' with minimum value of XXmm/day (XX=dynamic?)
    trmm_climatology_mask[trmm_climatology_mask < 1] = 1
elif method == 'NWD':
    #Convert based on the TRMM weekly 'Rainfall XXth percentile climatology mask' with maximum value of XXmm/day (XX=dynamic?)
    trmm_climatology_mask[trmm_climatology_mask < 1] = 1
#else:
    #print('Please check that you type the correct method in your setting file.')

trmm_total = np.empty([len(week_initial_date),end_year-start_year+1,len(ec_lat),len(ec_lon)])    #week,year,lat,lon
trmm_anomaly = np.empty([len(week_initial_date),end_year-start_year+1,len(ec_lat),len(ec_lon)])

for i_year in range(0,end_year-start_year+1):
    for i_day in range(0,days):
        if method == 'NDD': #method NDD
            trmm_data_repack[:,i_year,i_day,:,:] = (trmm_data_repack[:,i_year,i_day,:,:] < trmm_climatology_mask).astype(np.int_)
        elif method == 'NWD': #method NWD
              trmm_data_repack[:,i_year,i_day,:,:] = (trmm_data_repack[:,i_year,i_day,:,:] > trmm_climatology_mask).astype(np.int_)

#Sum up all 7 days in a week and compress the 'days' axis
trmm_total = np.sum(trmm_data_repack,axis=2) #axis 2 = days
trmm_climatology = np.mean(trmm_total,axis=1) #axis 1 = years

for i_year in range(0,end_year-start_year+1):
    trmm_anomaly[:,i_year,:,:] = trmm_total[:,i_year,:,:] - trmm_climatology

#--------------------------------------------------------------------------
# This part is to output all netCDF files (For testing/viewing in Panoply)
# and display TRMM (in ECMWF resolution) NDD/NWD climatology/total/anomaly
#-------------------------------------------------------------------------

#Define ECMWF output path and plot path
trmm_output = '../../../data/obs/prec/'
plot_dir = '../../../plot/obs/'

#Choose to output or display data
data_output = True
plot_figure = True

if data_output == True:
   #Output TRMM climatology/total/anomaly
   trmm_week = range(0,len(week_initial_date))
   trmm_year = range(start_year,end_year+1)

   trmm_filename = 'TRMM_' + calendar.month_abbr[target_month] + '_threshold' + str(threshold) + '_Climatology_Weekly_' + method + '.nc'
   s2s_utility_prec.write_trmm(trmm_output,trmm_filename,trmm_climatology,trmm_week,trmm_year,ec_lat,ec_lon,'Climatology')

   trmm_filename = 'TRMM_' + calendar.month_abbr[target_month] + '_threshold' + str(threshold) + '_Total_Weekly_' + method + '.nc'
   s2s_utility_prec.write_trmm(trmm_output,trmm_filename,trmm_total,trmm_week,trmm_year,ec_lat,ec_lon,'Total')

   trmm_filename = 'TRMM_' + calendar.month_abbr[target_month] + '_threshold' + str(threshold) + '_Anomaly_Weekly_' + method + '.nc'
   s2s_utility_prec.write_trmm(trmm_output,trmm_filename,trmm_anomaly,trmm_week,trmm_year,ec_lat,ec_lon,'Anomaly')

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

   #Plot TRMM NDD/NWD climatology/total/anomaly
   start_date = week_initial_date[target_week]
   end_date = start_date[:2] + "%02d"%(int(start_date[-2:])+6)

   data_range = [0,7]    #change data range for plotting accordingly
   title_str = 'TRMM ' + method + ' Weekly Climatology' + '\n' + start_date + '-' + end_date
   name_str = plot_dir + 'TRMM_' + start_date + '-' + end_date + '_threshold' + str(threshold) + '_Climatology_Weekly_' + method + '.png'
   s2s_utility_prec.plot_processing(trmm_climatology[target_week,:,:],ec_lat,ec_lon,lat_down,lat_up,lon_left,lon_right,grid_lat,grid_lon,data_range,title_str,name_str,'Climatology')

   data_range = [0,7]
   title_str = 'TRMM ' + method + ' Weekly Total' + '\n' + str(target_year) + ' ' + start_date + '-' + end_date
   name_str = plot_dir + 'TRMM_' + str(target_year) + '_' + start_date + '-' + end_date + '_threshold' + str(threshold) + '_Total_Weekly_' + method + '.png'
   s2s_utility_prec.plot_processing(trmm_total[target_week,target_year-start_year,:,:],ec_lat,ec_lon,lat_down,lat_up,lon_left,lon_right,grid_lat,grid_lon,data_range,title_str,name_str,'Total')

   data_range = [-7,7]
   title_str = 'TRMM ' + method + ' Weekly Anomaly' + '\n' + str(target_year) + ' ' + start_date + '-' + end_date
   name_str = plot_dir + 'TRMM_' + str(target_year) + '_' + start_date + '-' + end_date + '_threshold' + str(threshold) + '_Anomaly_Weekly_' + method + '.png'
   s2s_utility_prec.plot_processing(trmm_anomaly[target_week,target_year-start_year,:,:],ec_lat,ec_lon,lat_down,lat_up,lon_left,lon_right,grid_lat,grid_lon,data_range,title_str,name_str,'Anomaly')
