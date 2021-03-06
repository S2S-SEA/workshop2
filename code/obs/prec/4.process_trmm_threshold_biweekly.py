'''
This script loads the TRMM data as downloaded by IRI data library and prepares the number of dry days
(total per model 2-week, the climatology per 2-week, and the anomaly per 2-week).
It can plot either at the TRMM resolution or the ECMWF model resolution.
'''

import datetime
import numpy as np
import netCDF4
import calendar
from scipy import interpolate
import s2s_utility_prec as s2s
import configparser
config = configparser.ConfigParser()
config.read('../../../code/settings.ini')

#-------------------------------------------------------
#Initial setup
#-------------------------------------------------------
week_initial_date = ['1204','1207','1211','1214','1218']
target_month      = 12
threshold         = 20

trmm_resolution = True #True for TRMM, False for ECMWF
days            = 14
start_year      = 1998
end_year        = 2014

#Options:
#Set print_data = 0 if nothing to print, otherwise enter [year, latitude point, longitude point]
print_data       = [2014, 1.3, 103.8]

#Define TRMM input path
trmm_input    = '../../../data/obs/prec'
trmm_filename = 'TRMM_Daily_' + calendar.month_abbr[target_month] + '_1998-2014.nc'
cur_trmm_path = trmm_input + '/' + trmm_filename
print(cur_trmm_path)

#Define ECMWF input path
ec_input = '../../../data/model/ecmwf/prec'

#Define ECMWF output path and plot path
trmm_output = '../../../data/obs/prec/'
plot_dir    = '../../../plot/obs/'

#Choose to output or display data
data_output = False
plot_figure = False

if plot_figure:
#Define target week and year
	target_week = config.getint('Plot','target_week')
	target_year = config.getint('Plot','target_year')

#----------------------------------------------------------------
# 					Processing
#----------------------------------------------------------------

#Read TRMM dataset
trmm_time,trmm_lat,trmm_lon,trmm_data = s2s.read_trmm(cur_trmm_path)

#----------------------------------------------------------------
# 1. Interpolate TRMM resolution(0.25deg x 0.25deg) to ECMWF resolution(1.5deg x 1.5deg)
#----------------------------------------------------------------
print('Keeping TRMM resolution: ' + str(trmm_resolution))

if not trmm_resolution:

    #Read ECMWF data lat/lon
    nc     = netCDF4.Dataset(ec_input + '/' + 'ecmwf_iri_' + calendar.month_abbr[target_month] + '2017_cf.nc')
    ec_lat = nc.variables['Y'][:]
    ec_lon = nc.variables['X'][:]
    nc.close()

    #Interpolate TRMM resolution to ECMWF model resolution
    trmm_data_ec_resol = np.empty([trmm_data.shape[0],len(ec_lat),len(ec_lon)])
    for i in range(0,trmm_data.shape[0]):
        pi = interpolate.interp2d(trmm_lon,trmm_lat,trmm_data[i,:,:])
        trmm_data_ec_resol[i,:,:] = pi(np.asarray(ec_lon),np.asarray(ec_lat))
    trmm_data = trmm_data_ec_resol

if trmm_resolution:
    new_lat = trmm_lat
    new_lon = trmm_lon
else:
    new_lat = ec_lat
    new_lon = ec_lon

#Find the location for the latitude, longitude points
if print_data!=0:
    X_trmm,R1, Y_trmm,R2 = s2s.find_point(new_lat, new_lon,print_data[1],print_data[1],print_data[2],print_data[2])

#----------------------------------------------------------------
# 2. Repack TRMM daily rainfall to 5 dimensions (week_initial_date:years:days:lat:lon)
#----------------------------------------------------------------
trmm_data_repack = np.empty([len(week_initial_date),end_year-start_year+1,days,len(new_lat),len(new_lon)]) #week,year,day,lat,lon

#For each week initial date
for i_date in range(0,len(week_initial_date)):
    week_date = week_initial_date[i_date]

    #For each year
    for i_year in range(0,end_year-start_year+1):
        cur_date = datetime.datetime(i_year+start_year,int(week_date[:2]),int(week_date[-2:]),12)
        time_index = trmm_time.index(cur_date)

        #For each day (14 days in 2-week)
        for i_day in range(0,days):
            trmm_data_repack[i_date,i_year,i_day,:,:] = trmm_data[time_index+i_day,:,:]

#----------------------------------------------------------------
# 3. Generating TRMM rainfall percentile values
#----------------------------------------------------------------
print ('Preparing TRMM rainfall ' + str(threshold) + 'th percentile...')
trmm_climatology_mask = np.empty([len(week_initial_date),len(new_lat),len(new_lon)])
trmm_climatology_mask = np.percentile(trmm_data_repack, threshold, axis=(1,2)) #axis1:years axis2:14 days in 2-week

if print_data !=0:
    print('TRMM values for '+ str(threshold)+ 'th percentile')
    print('For location ' + str(print_data[1]) +'N ' +str(print_data[2])  + 'E')
    print(trmm_climatology_mask[:, X_trmm, Y_trmm])
else:
    print ('Mean of TRMM rainfall ' + str(threshold) + 'th percentile: ' + str(np.mean(trmm_climatology_mask)))
    print ('Median of TRMM rainfall ' + str(threshold) + 'th percentile: ' + str(np.median(trmm_climatology_mask)))
print ('Done!')

#----------------------------------------------------------------
# 4. This part calculate TRMM # of dry days in 2-week (climatology/total/anomaly)
#----------------------------------------------------------------
#Convert based on the TRMM daily threshold mask to have a minimum value of 1mm
trmm_climatology_mask[trmm_climatology_mask < 1] = 1

trmm_total_ec = np.empty([len(week_initial_date),end_year-start_year+1,len(new_lat),len(new_lon)])    #week,year,lat,lon
trmm_anomaly  = np.empty([len(week_initial_date),end_year-start_year+1,len(new_lat),len(new_lon)])

for i_year in range(0,end_year-start_year+1):
        for i_day in range(0,days):
            trmm_data_repack[:,i_year,i_day,:,:] = (trmm_data_repack[:,i_year,i_day,:,:] < trmm_climatology_mask).astype(np.int_)

if print_data !=0:
    print('TRMM dry days')
    print('For year ' + str(print_data[0]) + ' location ' + str(print_data[1]) + 'N ' + str(print_data[2]) + 'E')
    print(trmm_data_repack[:,print_data[0]-start_year,:,X_trmm,Y_trmm])

#Sum up all 14 days in 2-week and compress the 'days' axis
trmm_total = np.sum(trmm_data_repack,axis=2)  #axis 2 = days
trmm_climatology = np.mean(trmm_total,axis=1) #axis 1 = years

if print_data !=0:
    print('TRMM total & climatology values')
    print(trmm_total[:,print_data[0]-start_year,X_trmm,Y_trmm])
    print(trmm_climatology[:,X_trmm,Y_trmm])

for i_year in range(0,end_year-start_year+1):
    trmm_anomaly[:,i_year,:,:] = trmm_total[:,i_year,:,:] - trmm_climatology

if print_data !=0:
    print('TRMM anomaly values')
    print(trmm_anomaly[:,print_data[0]-start_year,X_trmm,Y_trmm])

#----------------------------------------------------------------
# This part is to output all netCDF files
# and display TRMM rainfall climatology/total/anomaly
#----------------------------------------------------------------
if data_output == True:
   #Output TRMM climatology/total/anomaly
   trmm_week = range(0,len(week_initial_date))
   trmm_year = range(start_year,end_year+1)

   if trmm_resolution:
       version = 'TRMM_res'
   else:
       version = 'EC_res'

   trmm_filename = 'TRMM_' + calendar.month_abbr[target_month] + '_threshold' + str(threshold) + '_Climatology_BiWeekly_' + version + '.nc'
   s2s.write_trmm(trmm_output,trmm_filename,trmm_climatology,trmm_week,trmm_year,new_lat,new_lon,'Climatology')

   trmm_filename = 'TRMM_' + calendar.month_abbr[target_month] + '_threshold' + str(threshold) + '_Total_BiWeekly_' + version + '.nc'
   s2s.write_trmm(trmm_output,trmm_filename,trmm_total,trmm_week,trmm_year,new_lat,new_lon,'Total')

   trmm_filename = 'TRMM_' + calendar.month_abbr[target_month] + '_threshold' + str(threshold) + '_Anomaly_BiWeekly_' + version + '.nc'
   s2s.write_trmm(trmm_output,trmm_filename,trmm_anomaly,trmm_week,trmm_year,new_lat,new_lon,'Anomaly')

if plot_figure == True:
   if trmm_resolution:
       version = 'TRMM_res'
   else:
       version = 'EC_res'

   #Plot TRMM climatology/total/anomaly
   start_date = week_initial_date[target_week]
   end_date   = "%02d"%target_month + "%02d"%(int(start_date[-2:])+13)

   #Define the domain for display
   lat_down  = config.getint('Plot','lat_down')
   lat_up    = config.getint('Plot','lat_up')
   lon_left  = config.getint('Plot','lon_left')
   lon_right = config.getint('Plot','lon_right')
   grid_lat  = config.getint('Plot','grid_lat')
   grid_lon  = config.getint('Plot','grid_lon')

   data_range = [0,days]
   title_str  = 'TRMM Number of Dry Days Climatology' + '\n' + start_date + '-' + end_date
   name_str   = plot_dir + 'TRMM_' + start_date + '-' + end_date + '_threshold' + str(threshold) + '_Climatology_BiWeekly_' + version + '.png'
   s2s.plot_processing(trmm_climatology[target_week,:,:],new_lat,new_lon,lat_down,lat_up,lon_left,lon_right,grid_lat,grid_lon,data_range,title_str,name_str,'Climatology')

   data_range = [0,days]
   title_str  = 'TRMM Number of Dry Days Total' + '\n' + str(target_year) + ' ' + start_date + '-' + end_date
   name_str   = plot_dir + 'TRMM_' + str(target_year) + '_' + start_date + '-' + end_date + '_threshold' + str(threshold) + '_Total_BiWeekly_' + version + '.png'
   s2s.plot_processing(trmm_total[target_week,target_year-start_year,:,:],new_lat,new_lon,lat_down,lat_up,lon_left,lon_right,grid_lat,grid_lon,data_range,title_str,name_str,'Total')

   data_range = [-1*days,days]
   title_str  = 'TRMM Number of Dry Days Anomaly' + '\n' + str(target_year) + ' ' + start_date + '-' + end_date
   name_str   = plot_dir + 'TRMM_' + str(target_year) + '_' + start_date + '-' + end_date + '_threshold' + str(threshold) + '_Anomaly_BiWeekly_' + version + '.png'
   s2s.plot_processing(trmm_anomaly[target_week,target_year-start_year,:,:],new_lat,new_lon,lat_down,lat_up,lon_left,lon_right,grid_lat,grid_lon,data_range,title_str,name_str,'Anomaly')

   data_range = [0,10]    #change data range for plotting accordingly
   title_str  = 'TRMM Daily Rainfall '+ str(threshold) + 'th Percentile' + '\n' + str(start_date) + '-' + str(end_date)
   name_str   = plot_dir + 'TRMM_' + str(start_date) + '-' + str(end_date) +  '_threshold' + str(threshold) + '_climatology_mask_BiWeekly_' + version + '.png'
   s2s.plot_processing(trmm_climatology_mask[target_week,:,:],new_lat,new_lon,lat_down,lat_up,lon_left,lon_right,grid_lat,grid_lon,data_range,title_str,name_str,'Climatology_Mask')

print ('Finished!')
