import numpy as np
import calendar
import s2s_utility_prec
import configparser
config = configparser.ConfigParser()
config.read('../../../../code/settings.ini')

#Initial setup
target_month = config.getint('Process','target_month')
threshold = config.getint('Process','threshold')
method = config.get('Process','method') #NDD=Dry NWD=Wet
process_cora = True
process_msss = True

#---------------------------------------------------
#This part is to prepare TRMM and ECMWF anomaly data
#---------------------------------------------------

#Define TRMM input path
trmm_input = '../../../../data/obs/prec'
trmm_filename = 'TRMM_' + calendar.month_abbr[target_month] + '_threshold' + str(threshold) + '_Anomaly_Weekly_' + method + '.nc'
cur_trmm_path = trmm_input + '/' + trmm_filename

#Define ECMWF input path
ec_input = '../../../../data/model/ecmwf/prec'
ec_filename = 'ECMWF_' + calendar.month_abbr[target_month] + '_threshold' + str(threshold) + '_Anomaly_Weekly_' + method + '.nc'
cur_ec_path = ec_input + '/' + ec_filename

#Read TRMM and ECMWF data
trmm_lat,trmm_lon,trmm_anomaly = s2s_utility_prec.read_method(cur_trmm_path,'TRMM')
ec_lat_0,ec_lon,ec_anomaly_0 = s2s_utility_prec.read_method(cur_ec_path,'ECMWF')
ec_lat = ec_lat_0[::-1] #reverse lat to follow trmm lat's convention
ec_anomaly = ec_anomaly_0[:,:,:,::-1,:] #step,week,year,lat,lon; reverse lat in axis/dimension 3

#-----------------------------------------------
#This part is to calculate and display CORA/MSSS
#-----------------------------------------------

#Define plot folder
plot_dir = '../../../../plot/skill_scores/anomaly/'

#Define the domain for display
lat_down = config.getint('Plot','lat_down')
lat_up = config.getint('Plot','lat_up')
lon_left = config.getint('Plot','lon_left')
lon_right = config.getint('Plot','lon_right')
grid_lat = config.getint('Plot','grid_lat')
grid_lon = config.getint('Plot','grid_lon')

if process_cora == True:
   #For each model lead time
   for i_step in range(0,ec_anomaly.shape[0]):
       sum_ec_trmm = np.zeros([len(ec_lat),len(ec_lon)])
       sum_ec = np.zeros([len(ec_lat),len(ec_lon)])
       sum_trmm = np.zeros([len(ec_lat),len(ec_lon)])

       #For each week
       for i_week in range(0,ec_anomaly.shape[1]):
           #For each year
           for i_year in range(0,ec_anomaly.shape[2]):
               sum_ec_trmm = sum_ec_trmm + ec_anomaly[i_step,i_week,i_year,:,:]*trmm_anomaly[i_week,i_year,:,:]
               sum_ec = sum_ec + ec_anomaly[i_step,i_week,i_year,:,:]**2
               sum_trmm = sum_trmm + trmm_anomaly[i_week,i_year,:,:]**2

       np.seterr(divide='ignore', invalid='ignore') # ignore error msgs in divide by 0/NaN
       cora = sum_ec_trmm/(sum_ec*sum_trmm)**(1.0/2)

       #Plot CORA
       title_str = method + ' in a week (Anomaly): CORA' + '\n' + calendar.month_abbr[target_month] + ' (LT' + str(i_step+1) + ')'
       name_str = plot_dir + 'ECMWF_' + calendar.month_abbr[target_month] + '_LT' + str(i_step+1) + '_threshold' + str(threshold) + '_CORA_' + method + '.png'
       s2s_utility_prec.plot_verification(cora,ec_lat,ec_lon,lat_down,lat_up,lon_left,lon_right,grid_lat,grid_lon,title_str,name_str,'CORA')

if process_msss == True:
   #For each model lead time
   for i_step in range(0,ec_anomaly.shape[0]):
       sum_ec_trmm = np.zeros([len(ec_lat),len(ec_lon)])
       sum_trmm = np.zeros([len(ec_lat),len(ec_lon)])

       #For each week
       for i_week in range(0,ec_anomaly.shape[1]):
           #For each year
           for i_year in range(0,ec_anomaly.shape[2]):
               sum_ec_trmm = sum_ec_trmm + (ec_anomaly[i_step,i_week,i_year,:,:]-trmm_anomaly[i_week,i_year,:,:])**2
               sum_trmm = sum_trmm + trmm_anomaly[i_week,i_year,:,:]**2
       msss = 1 - sum_ec_trmm/sum_trmm

       #Plot MSSS
       title_str = method + ' in a week (Anomaly): MSSS' + '\n' + calendar.month_abbr[target_month] + ' (LT' + str(i_step+1) + ')'
       name_str = plot_dir + 'ECMWF_' + calendar.month_abbr[target_month] + '_LT' + str(i_step+1) + '_threshold' + str(threshold) + '_MSSS_' + method + '.png'
       s2s_utility_prec.plot_verification(msss,ec_lat,ec_lon,lat_down,lat_up,lon_left,lon_right,grid_lat,grid_lon,title_str,name_str,'MSSS')
