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
process_hss = True

#---------------------------------------------------
#This part is to prepare TRMM and ECMWF Total data
#---------------------------------------------------

#Define TRMM input path
trmm_input = '../../../../data/obs/prec'
trmm_filename = 'TRMM_' + calendar.month_abbr[target_month] + '_threshold' + str(threshold) + '_Total_Weekly_' + method + '.nc'
cur_trmm_path = trmm_input + '/' + trmm_filename

#Define ECMWF input path
ec_input = '../../../../data/model/ecmwf/prec'
ec_filename = 'ECMWF_' + calendar.month_abbr[target_month] + '_threshold' + str(threshold) + '_Total_Weekly_' + method + '.nc'
cur_ec_path = ec_input + '/' + ec_filename

#Read TRMM and ECMWF data
trmm_lat,trmm_lon,trmm_total = s2s_utility_prec.read_method(cur_trmm_path,'TRMM')
ec_lat_0,ec_lon,ec_total_0 = s2s_utility_prec.read_method(cur_ec_path,'ECMWF')
ec_lat = ec_lat_0[::-1] #reverse lat to follow trmm lat's convention
ec_total = ec_total_0[:,:,:,::-1,:] #step,week,year,lat,lon; reverse lat in axis/dimension 3

#---------------------------------------------------------------
#This part is to prepare TRMM Climatology data (for dry masking)
#---------------------------------------------------------------
trmm_filename_1 = 'TRMM_' + calendar.month_abbr[target_month] + '_threshold' + str(threshold) + '_Climatology_Weekly_' + method + '.nc'
cur_trmm_path_1 = trmm_input + '/' + trmm_filename_1
#Read TRMM data
trmm_lat,trmm_lon,trmm_climo = s2s_utility_prec.read_method(cur_trmm_path_1,'TRMM_Climo') #week,lat,lon
trmm_climo = np.mean(trmm_climo, axis=0) #collapse the week axis 0

#-----------------------------------------------
#This part is to calculate and display HSS
#-----------------------------------------------

#Define plot folder
plot_dir = '../../../../plot/skill_scores/total/'

#Define the domain for display
lat_down = config.getint('Plot','lat_down')
lat_up = config.getint('Plot','lat_up')
lon_left = config.getint('Plot','lon_left')
lon_right = config.getint('Plot','lon_right')
grid_lat = config.getint('Plot','grid_lat')
grid_lon = config.getint('Plot','grid_lon')

if process_hss == True:
   #For each model lead time
   for i_step in range(0,ec_total.shape[0]):
       sum_boxR1_1 = np.zeros([len(ec_lat),len(ec_lon)])
       sum_boxR1_2 = np.zeros([len(ec_lat),len(ec_lon)])
       sum_boxR1_3 = np.zeros([len(ec_lat),len(ec_lon)])
       sum_boxR1_4 = np.zeros([len(ec_lat),len(ec_lon)])
       sum_boxR2_1 = np.zeros([len(ec_lat),len(ec_lon)])
       sum_boxR2_2 = np.zeros([len(ec_lat),len(ec_lon)])
       sum_boxR2_3 = np.zeros([len(ec_lat),len(ec_lon)])
       sum_boxR2_4 = np.zeros([len(ec_lat),len(ec_lon)])
       sum_boxR3_1 = np.zeros([len(ec_lat),len(ec_lon)])
       sum_boxR3_2 = np.zeros([len(ec_lat),len(ec_lon)])
       sum_boxR3_3 = np.zeros([len(ec_lat),len(ec_lon)])
       sum_boxR3_4 = np.zeros([len(ec_lat),len(ec_lon)])
       sum_boxR4_1 = np.zeros([len(ec_lat),len(ec_lon)])
       sum_boxR4_2 = np.zeros([len(ec_lat),len(ec_lon)])
       sum_boxR4_3 = np.zeros([len(ec_lat),len(ec_lon)])
       sum_boxR4_4 = np.zeros([len(ec_lat),len(ec_lon)])

       #For each week
       for i_week in range(0,ec_total.shape[1]):
           #For each year
           for i_year in range(0,ec_total.shape[2]):
               a = ec_total[i_step,i_week,i_year,:,:]
               b = trmm_total[i_week,i_year,:,:]
               sum_boxR1_1 = sum_boxR1_1 + (np.where(a<=1,1,0) & np.where(b<=1,1,0))
               sum_boxR2_1 = sum_boxR2_1 + (np.where(a<=3,1,0) & np.where(a>1,1,0) & np.where(b<=1,1,0))
               sum_boxR3_1 = sum_boxR3_1 + (np.where(a<=5,1,0) & np.where(a>3,1,0) & np.where(b<=1,1,0))
               sum_boxR4_1 = sum_boxR4_1 + (np.where(a>5,1,0) & np.where(b<=1,1,0))

               sum_boxR1_2 = sum_boxR1_2 + (np.where(a<=1,1,0) & np.where(b<=3,1,0) & np.where(b>1,1,0))
               sum_boxR2_2 = sum_boxR2_2 + (np.where(a<=3,1,0) & np.where(a>1,1,0) & np.where(b<=3,1,0) & np.where(b>1,1,0))
               sum_boxR3_2 = sum_boxR3_2 + (np.where(a<=5,1,0) & np.where(a>3,1,0) & np.where(b<=3,1,0) & np.where(b>1,1,0))
               sum_boxR4_2 = sum_boxR4_2 + (np.where(a>5,1,0) & np.where(b<=3,1,0) & np.where(b>1,1,0))

               sum_boxR1_3 = sum_boxR1_3 + (np.where(a<=1,1,0) & np.where(b<=5,1,0) & np.where(b>3,1,0))
               sum_boxR2_3 = sum_boxR2_3 + (np.where(a<=3,1,0) & np.where(a>1,1,0) & np.where(b<=5,1,0) & np.where(b>3,1,0))
               sum_boxR3_3 = sum_boxR3_3 + (np.where(a<=5,1,0) & np.where(a>3,1,0) & np.where(b<=5,1,0) & np.where(b>3,1,0))
               sum_boxR4_3 = sum_boxR4_3 + (np.where(a>5,1,0) & np.where(b<=5,1,0) & np.where(b>3,1,0))

               sum_boxR1_4 = sum_boxR1_4 + (np.where(a<=1,1,0) & np.where(b>5,1,0))
               sum_boxR2_4 = sum_boxR2_4 + (np.where(a<=3,1,0) & np.where(a>1,1,0) & np.where(b>5,1,0))
               sum_boxR3_4 = sum_boxR3_4 + (np.where(a<=5,1,0) & np.where(a>3,1,0) & np.where(b>5,1,0))
               sum_boxR4_4 = sum_boxR4_4 + (np.where(a>5,1,0) & np.where(b>5,1,0))

       total_count = (i_week+1) * (i_year+1)
       total_hit = sum_boxR1_1 + sum_boxR2_2 + sum_boxR3_3 + sum_boxR4_4
       total_obs_col_1 = sum_boxR1_1 + sum_boxR2_1 + sum_boxR3_1 + sum_boxR4_1
       total_obs_col_2 = sum_boxR1_2 + sum_boxR2_2 + sum_boxR3_2 + sum_boxR4_2
       total_obs_col_3 = sum_boxR1_3 + sum_boxR2_3 + sum_boxR3_3 + sum_boxR4_3
       total_obs_col_4 = sum_boxR1_4 + sum_boxR2_4 + sum_boxR3_4 + sum_boxR4_4
       total_fst_row_1 = sum_boxR1_1 + sum_boxR1_2 + sum_boxR1_3 + sum_boxR1_4
       total_fst_row_2 = sum_boxR2_1 + sum_boxR2_2 + sum_boxR2_3 + sum_boxR2_4
       total_fst_row_3 = sum_boxR3_1 + sum_boxR3_2 + sum_boxR3_3 + sum_boxR3_4
       total_fst_row_4 = sum_boxR4_1 + sum_boxR4_2 + sum_boxR4_3 + sum_boxR4_4
       cross_product = total_obs_col_1 * total_fst_row_1 + total_obs_col_2 * total_fst_row_2 + total_obs_col_3 * total_fst_row_3 + total_obs_col_4 * total_fst_row_4
       denominator = total_count**2 - cross_product
       np.seterr(divide='ignore', invalid='ignore') # ignore error msgs in divide by 0/NaN
       hss = (total_count * total_hit - cross_product)/denominator

       #Plot HSS
       title_str =  method + ' in a week (Total): HSS' + '\n' + calendar.month_abbr[target_month] + ' (LT' + str(i_step+1) + ')'
       name_str = plot_dir + 'ECMWF_' + calendar.month_abbr[target_month] + '_LT' + str(i_step+1) + '_threshold' + str(threshold) + '_HSS_' + method + '.png'
       s2s_utility_prec.plot_verification(hss,ec_lat,ec_lon,lat_down,lat_up,lon_left,lon_right,grid_lat,grid_lon,title_str,name_str,'HSS')

       #Plot HSS (with TRMM climatology dry mask)
       if method == 'NDD':
           hss[trmm_climo > 6] = 99 # apply TRMM climatology dry mask, with dummy value of 99
       elif method == 'NWD':
           hss[trmm_climo < 1] = 99 # apply TRMM climatology dry mask, with dummy value of 99

       title_str = method + ' in a week (Total): HSS' + '\n' + calendar.month_abbr[target_month] + ' (LT' + str(i_step+1) + ') - white areas denote dry climatological mask'
       name_str = plot_dir + 'ECMWF_' + calendar.month_abbr[target_month] + '_LT' + str(i_step+1) + '_threshold' + str(threshold) + '_HSS_' + method + '_drymask.png'
       s2s_utility_prec.plot_verification(hss,ec_lat,ec_lon,lat_down,lat_up,lon_left,lon_right,grid_lat,grid_lon,title_str,name_str,'HSS')
