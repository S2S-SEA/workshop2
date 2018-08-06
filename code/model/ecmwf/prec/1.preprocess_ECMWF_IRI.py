'''
1. This program processes the downloaded perturbed forecast (pf) and control
forecast dataset (cf). It combines the 10 ensembles members of ECMWF's pf
with the 1 ECMWF's cf.
2. Next, the 'accumulated rainfall' datasets are converted into daily values
& re-packed to 7 dimensions[step:week:year:days:members:lat:lon] (step = lead_times,
week = "full" weeks, days = 7 days in a week, members = ensemble members). The repacked
dataset is then saved for next processing step.
3. Also the daily rainfall '20th percentile climatology mask' (bias-correct for each
grid points, for each "full" weeks and for each lead times) is generated from this re-packed dataset.
'''
import netCDF4
import numpy as np
import datetime
import os
import sys    
import s2s_utility_prec
import calendar

# Define data folder
data_dir = '../../../../data/model/ecmwf/prec/'


# Initial setup
# All the initial dates with complete 7-day week in Dec for the 2017 runs
init_date = ['11-13','11-16','11-20','11-23','11-27','11-30','12-04','12-07','12-11','12-14','12-18','12-21','12-25'] #format needed to read .nc files
week_initial_date = [4,7,11,14,18,21,25]
target_month = 12
start_year = 1998
end_year = 2014
lead_times = 4 #lead_times = 4
days = 7 #7days = 1week


members = 11 #11 ensemble members
threshold = 30 #change this value for your group project!

#where the data will be saved
ec_output = '../../../../data/model/ecmwf/prec'


## PLOTTING INPUTS
plot_figure = True
plot_dir = '../../../../plot/model/' #where the data will be saved
target_week = 6 # this is the week that plots out for the plots if plotting
lat_down = -15
lat_up = 30
lon_left = 90
lon_right = 150
grid_lat = 10
grid_lon = 10
##------------------------------------------------------------------------------------------------------
#                                              Processing
##------------------------------------------------------------------------------------------------------

#Read ECMWF lat/lon
nc = netCDF4.Dataset(data_dir + 'ecmwf_iri_dec2017_pf.nc')
ec_lat = nc.variables['Y'][:]
ec_lon = nc.variables['X'][:]
nc.close()

# Create an array to store the repacked daily data based on lead_time 1/2/3/4
ec_daily = np.empty([lead_times,len(week_initial_date),end_year-start_year+1,days,members,len(ec_lat),len(ec_lon)]) #step,week,year,days,members,lat,lon

#-----------------------------------------
# 1. Combine 10 pf members and 1 cf member
#-----------------------------------------
print("Processing ECMWF file...")
ds_cf = netCDF4.Dataset(data_dir + 'ecmwf_iri_dec2017_cf.nc') #Load the pf file
ds_pf = netCDF4.Dataset(data_dir + 'ecmwf_iri_dec2017_pf.nc') #Load the cf file

# You may want to uncomment the following lines
# to print out the file and variable information
#print(ds_pf.file_format)
#print(ds_pf.dimensions.keys())
#print(ds_pf.variables)

# Read in the variables from cf
prec_hd = ds_cf.variables['hdate'][:]
prec_lead = ds_cf.variables['L'][:]
prec_lat = ds_cf.variables['Y'][:]
prec_lon = ds_cf.variables['X'][:]
prec_temp= ds_cf.variables['S']
prec_start= netCDF4.num2date(prec_temp[:],prec_temp.units)

if ec_lat.all() != prec_lat.all():
    print('Latitdue files are not the same')
if ec_lon.all() != prec_lon.all():
    print('Longitude files are not the same')
# Read in the array from pf's total precip ('tp') variable
arr_pf = ds_pf.variables['tp'][:]
# Read in the cf's total precip ('tp') variable
arr_cf = ds_cf.variables['tp'][:]

arr_shp = arr_pf.shape

# Create a new array to accommodate the 10 pf and 1 cf members
arr_comb = np.empty([arr_shp[0], arr_shp[1],arr_shp[2], arr_shp[3]+1, arr_shp[4], arr_shp[5]]) #year,days,members,lat,lon
# Populate arr_comb with pf and cf data
arr_comb[:,:,:,0:10,:,:] = arr_pf
arr_comb[:,:,:,10,:,:] = arr_cf


##----------------------------------------
## 2. Calculate daily precipitation totals
##----------------------------------------
arr_daily = np.empty([arr_shp[0],arr_shp[1], arr_shp[2]-1, arr_shp[3]+1, arr_shp[4], arr_shp[5]]) #29days minus 1day = 28days
for i in range(arr_shp[2]-1):
    arr_daily[:,:,i,:,:,:] = np.subtract(arr_comb[:,:,i+1,:,:,:], arr_comb[:,:,i,:,:,:]) #Substract to get daily totals


#------------------------------------------------------------------
# 2. Repack according to lead_times, "full" weeks and days' indexes
#------------------------------------------------------------------
count_model_run =0
for i_date in prec_start:

    ec_time = i_date
    #For each model lead time
    for i_lead in range(0,lead_times): 
        i_step= int(i_lead*7 + 6)
       # print(i_step)
        end_date = ec_time + datetime.timedelta(days=i_step)
        start_date = end_date - datetime.timedelta(days=6)
        #Check if forecasted week is within the target month
        if start_date.month == target_month and end_date.month == target_month:
            try:
                i_week = week_initial_date.index(start_date.day)
            except:
                print(i_step)
                print("The date "+str(start_date) +" was not found inthe weeks list. Check the model initdal date list and the weeks list")
            #i_week = week_initial_date.index("%02d"%start_date.month + "%02d"%start_date.day)
            #For each day
            for i_day in range(0,days):
                #print ('ilead: ' + str(i_lead))
                #print ('iweek: ' + str(i_week))
                #print ('iday: ' + str(i_day))
               # print (7*(i_step+1)-days+i_day)
                ec_daily[i_lead,i_week,:,i_day,:,:,:] = arr_daily[:,count_model_run, 7*(i_lead+1)-days+i_day,:,:,:] #broadcasting ,:,
    count_model_run +=1
ds_pf.close()
ds_cf.close()
print ('Done!')

##------------------------------------------------------------------------
## 3. Generate the ECMWF daily rainfall percentile values
##------------------------------------------------------------------------
print ('Finding ECMWF daily rainfall '+ str(threshold)+'  percentile ...')

ec_climatology_mask = np.empty([lead_times,len(week_initial_date),len(ec_lat),len(ec_lon)])    #step,week,lat,lon
for n in range(len(prec_lat)):
    ec_climatology_mask[:, :, n, :] = np.percentile(ec_daily[:,:, :, :, :, n,:], threshold, axis=(2,3,4)) #axis2:years,axis3:7 days in a week,axis4:11 members
#ec_climatology_mask = np.percentile(ec_daily, threshold, axis=(2,3,4)) #axis2:years,axis3:7 days in a week,axis4:11 members

print ('Done!')

##--------------------------------------------------------------------------------------
## This part is to output all netCDF files 
##--------------------------------------------------------------------------------------
#Define ECMWF output path

ec_step = range(0,lead_times)
ec_week = range(0,len(week_initial_date))
ec_year = range(start_year,end_year+1)
ec_day = range(0,days)
ec_member = range(0,members)

ec_filename = 'ECMWF_' + calendar.month_abbr[target_month] + '_Total_Daily.nc'
s2s_utility_prec.write_ec_daily(ec_output,ec_filename,ec_daily,ec_step,ec_week,ec_year,ec_day,ec_member,prec_lat,prec_lon,'Daily')
print('File saved! ' + ec_filename + ' to directory ' + ec_output)

ec_filename = 'ECMWF_' + calendar.month_abbr[target_month] + '_threshold' + str(threshold) + '_Climatology_Mask_Daily.nc'
s2s_utility_prec.write_ec(ec_output,ec_filename,ec_climatology_mask,ec_step,ec_week,ec_year,prec_lat,prec_lon,'Climatology')
print('File saved! ' + ec_filename + ' to directory ' + ec_output)

#-------------------------------------------------------------------------------------
# 3. This part is to output and display ECMWF Rainfall 20th percentile climatology mask
#-------------------------------------------------------------------------------------

if plot_figure:
   #Define the domain for display

   #Plot ECMWF daily Rainfall 20th percentile climatology mask
   for i_step in range(0,lead_times):
       start_date = week_initial_date[target_week]
       end_date = "%02d"%target_month + "%02d"%(int(start_date)+6)

       data_range = [0,10]    #change data range for plotting accordingly
       title_str = 'ECMWF Daily Rainfall '+str(threshold)+'th Percentile Climatology' + '\n' + str(start_date) + '-' + str(end_date) + ' (LT' + str(i_step+1) + ')'
       name_str = plot_dir + 'ECMWF_' + str(start_date) + '-' + str(end_date) + '_' + 'LT' + str(i_step+1) + '_threshold' + str(threshold) + '_Climatology_Mask.png'
       s2s_utility_prec.plot_processing(ec_climatology_mask[i_step,target_week,:,:],prec_lat,prec_lon,lat_down,lat_up,lon_left,lon_right,grid_lat,grid_lon,data_range,title_str,name_str,'Climatology_Mask')
