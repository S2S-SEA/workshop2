'''
Verification of the NDD for ECMWF model data with TRMM data is done with CORA and MSSS.
'''

import numpy as np
import calendar
import s2s_utility_prec
import configparser
config = configparser.ConfigParser()
config.read('../../../../code/settings.ini')

#Initial setup
target_month = 12
threshold    = 20

#Process and plot
process_cora = False
process_msss = False

#Define plot folder
plot_dir  = '../../../../plot/skill_scores/anomaly/'
#Define the domain for display
lat_down  = config.getint('Plot','lat_down')
lat_up    = config.getint('Plot','lat_up')
lon_left  = config.getint('Plot','lon_left')
lon_right = config.getint('Plot','lon_right')
grid_lat  = config.getint('Plot','grid_lat')
grid_lon  = config.getint('Plot','grid_lon')

#---------------------------------------------------------------
#This part is to prepare TRMM and ECMWF anomaly data
#---------------------------------------------------------------
#Define TRMM input path
trmm_input    = '../../../../data/obs/prec'
trmm_filename = 'TRMM_' + calendar.month_abbr[target_month] + '_threshold' + str(threshold) + '_Anomaly_BiWeekly_EC_res.nc'
cur_trmm_path = trmm_input + '/' + trmm_filename

#Define ECMWF input path
ec_input    = '../../../../data/model/ecmwf/prec'
ec_filename = 'ECMWF_' + calendar.month_abbr[target_month] + '_threshold' + str(threshold) + '_Anomaly_BiWeekly.nc'
cur_ec_path = ec_input + '/' + ec_filename

#Read TRMM and ECMWF data
trmm_lat,trmm_lon,trmm_anomaly = s2s_utility_prec.read_method(cur_trmm_path,'TRMM')
ec_lat,ec_lon,ec_anomaly       = s2s_utility_prec.read_method(cur_ec_path,'ECMWF')

#---------------------------------------------------------------
#This part is to prepare TRMM Climatology data (for dry masking)
#---------------------------------------------------------------
trmm_filename_1 = 'TRMM_' + calendar.month_abbr[target_month] + '_threshold' + str(threshold) + '_Climatology_BiWeekly_EC_res.nc'
cur_trmm_path_1 = trmm_input + '/' + trmm_filename_1
#Read TRMM data
trmm_lat,trmm_lon,trmm_climo = s2s_utility_prec.read_method(cur_trmm_path_1,'TRMM_Climo') #week,lat,lon
trmm_climo = np.mean(trmm_climo, axis=0) #collapse the week axis 0

#---------------------------------------------------------------
#This part is to process and display CORA/MSSS
#---------------------------------------------------------------
if process_cora == True:
   #For each model lead time
   for i_step in range(0,ec_anomaly.shape[0]):
       sum_ec_trmm = np.zeros([len(ec_lat),len(ec_lon)])
       sum_ec      = np.zeros([len(ec_lat),len(ec_lon)])
       sum_trmm    = np.zeros([len(ec_lat),len(ec_lon)])

       #For each week
       for i_week in range(0,ec_anomaly.shape[1]):
           #For each year
           for i_year in range(0,ec_anomaly.shape[2]):
               sum_ec_trmm = sum_ec_trmm + ec_anomaly[i_step,i_week,i_year,:,:]*trmm_anomaly[i_week,i_year,:,:]
               sum_ec      = sum_ec + ec_anomaly[i_step,i_week,i_year,:,:]**2
               sum_trmm    = sum_trmm + trmm_anomaly[i_week,i_year,:,:]**2

       np.seterr(divide='ignore', invalid='ignore') # ignore error msgs in divide by 0/NaN
       cora = sum_ec_trmm/(sum_ec*sum_trmm)**(1.0/2)

       #Plot CORA
       title_str = 'NDD in 2-week (Anomaly): CORA' + '\n' + calendar.month_abbr[target_month] + ' (LT' + str(i_step+1) + ')'
       name_str  = plot_dir + 'ECMWF_' + calendar.month_abbr[target_month] + '_LT' + str(i_step+1) + '_threshold' + str(threshold) + '_CORA_BiWeekly.png'
       s2s_utility_prec.plot_verification(cora,ec_lat,ec_lon,lat_down,lat_up,lon_left,lon_right,grid_lat,grid_lon,title_str,name_str,'CORA')

       #Plot CORA (with TRMM climatology dry mask)
       cora[trmm_climo > 6] = 99 # apply TRMM climatology dry mask, with dummy value of 99

       title_str = 'NDD in 2-week (Anomaly): CORA' + '\n' + calendar.month_abbr[target_month] + ' (LT' + str(i_step+1) + ') - white areas denote dry climatological mask'
       name_str  = plot_dir + 'ECMWF_' + calendar.month_abbr[target_month] + '_LT' + str(i_step+1) + '_threshold' + str(threshold) + '_CORA_BiWeekly_drymask.png'
       s2s_utility_prec.plot_verification(cora,ec_lat,ec_lon,lat_down,lat_up,lon_left,lon_right,grid_lat,grid_lon,title_str,name_str,'CORA')

if process_msss == True:
   #For each model lead time
   for i_step in range(0,ec_anomaly.shape[0]):
       sum_ec_trmm = np.zeros([len(ec_lat),len(ec_lon)])
       sum_trmm    = np.zeros([len(ec_lat),len(ec_lon)])

       #For each week
       for i_week in range(0,ec_anomaly.shape[1]):
           #For each year
           for i_year in range(0,ec_anomaly.shape[2]):
               sum_ec_trmm = sum_ec_trmm + (ec_anomaly[i_step,i_week,i_year,:,:]-trmm_anomaly[i_week,i_year,:,:])**2
               sum_trmm    = sum_trmm + trmm_anomaly[i_week,i_year,:,:]**2
       msss = 1 - sum_ec_trmm/sum_trmm

       #Plot MSSS
       title_str = 'NDD in 2-week (Anomaly): MSSS' + '\n' + calendar.month_abbr[target_month] + ' (LT' + str(i_step+1) + ')'
       name_str  = plot_dir + 'ECMWF_' + calendar.month_abbr[target_month] + '_LT' + str(i_step+1) + '_threshold' + str(threshold) + '_MSSS_BiWeekly.png'
       s2s_utility_prec.plot_verification(msss,ec_lat,ec_lon,lat_down,lat_up,lon_left,lon_right,grid_lat,grid_lon,title_str,name_str,'MSSS')

       #Plot MSSS (with TRMM climatology dry mask)
       msss[trmm_climo > 6] = 99 # apply TRMM climatology dry mask, with dummy value of 99

       title_str = 'NDD in 2-week (Anomaly): MSSS' + '\n' + calendar.month_abbr[target_month] + ' (LT' + str(i_step+1) + ') - white areas denote dry climatological mask'
       name_str  = plot_dir + 'ECMWF_' + calendar.month_abbr[target_month] + '_LT' + str(i_step+1) + '_threshold' + str(threshold) + '_MSSS_BiWeekly_drymask.png'
       s2s_utility_prec.plot_verification(msss,ec_lat,ec_lon,lat_down,lat_up,lon_left,lon_right,grid_lat,grid_lon,title_str,name_str,'MSSS')

print('Finished!')
