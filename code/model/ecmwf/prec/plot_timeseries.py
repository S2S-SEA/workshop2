import os
import numpy
import netCDF4
import matplotlib.pyplot as plt

def find_point(data_lat,data_lon,lat_down,lat_up,lon_left,lon_right):

    #Find the nearest points
    lat_index1 = numpy.where(data_lat == data_lat.flat[numpy.abs(data_lat - lat_down).argmin()])
    lat_index2 = numpy.where(data_lat == data_lat.flat[numpy.abs(data_lat - lat_up).argmin()])
    lon_index1 = numpy.where(data_lon == data_lon.flat[numpy.abs(data_lon - lon_left).argmin()])
    lon_index2 = numpy.where(data_lon == data_lon.flat[numpy.abs(data_lon - lon_right).argmin()])
    L1 = lat_index1[0][0]
    R1 = lat_index2[0][0]
    L2 = lon_index1[0][0]
    R2 = lon_index2[0][0]

    return L1,R1,L2,R2

def read_anomaly(cur_data_path,index):

    #Open data path to retreive data
    nc = netCDF4.Dataset(cur_data_path)
    prcpvar = nc.variables['rainfall']

    #Read latitude and longitude and data
    data_lat = nc.variables['latitude'][:]
    data_lon = nc.variables['longitude'][:]
    if index == 'TRMM':
       pdata = prcpvar[:,:,:,:]    #week,year,lat,lon
    if index == 'ECMWF':
       pdata = prcpvar[:,:,:,:,:]    #step,week,year,lat,lon
       prcpvar = prcpvar[:,:,::-1,:,:]    #step,week,year,lat,lon

    return data_lat,data_lon,pdata
    nc.close()

def plot_fig(trmm_anomaly_0,ec_anomaly_0,target_week,start_year,end_year,lat_0,lon_0,lat_down,lat_up,lon_left,lon_right,title_str,name_str):

    #Find borders of the domain
    L1,R1,L2,R2 = find_point(lat_0,lon_0,lat_down,lat_up,lon_left,lon_right)
    trmm_anomaly = trmm_anomaly_0[:,:,L1:R1+1,L2:R2+1]
    ec_anomaly = ec_anomaly_0[:,:,:,L1:R1+1,L2:R2+1]
    
    #Write TRMM and ECMWF for specified domain and week into list
    trmm_anomaly_list = []
    ec_anomaly_list = []
    for i_year in range(0,trmm_anomaly.shape[1]):
        trmm_anomaly_list.append(numpy.mean(trmm_anomaly_0[target_week,i_year,:,:]))
    for i_step in range(0,ec_anomaly.shape[0]):
        for i_year in range(0,ec_anomaly.shape[2]):
            ec_anomaly_list.append(numpy.mean(ec_anomaly[i_step,target_week,i_year,:,:]))
    print(trmm_anomaly_list)
    #Plot time series
    fig,ax = plt.subplots(figsize=(12,5))
    xx = range(start_year,end_year+1)
    ax.plot(xx,trmm_anomaly_list,'--bo',linewidth=2,label='TRMM')
    ax.plot(xx,ec_anomaly_list[0:end_year-start_year+1],'--go',linewidth=2,label='EC_LT1')
    ax.plot(xx,ec_anomaly_list[end_year-start_year+1:(end_year-start_year+1)*2],'--co',linewidth=2,label='EC_LT2')
    ax.plot(xx,ec_anomaly_list[(end_year-start_year+1)*2:(end_year-start_year+1)*3],'--mo',linewidth=2,label='EC_LT3')
    ax.plot(xx,ec_anomaly_list[(end_year-start_year+1)*3:(end_year-start_year+1)*4],'--ro',linewidth=2,label='EC_LT4')
    ax.set_xticks(range(start_year,end_year+1))
    ax.set_xlabel('Year',fontsize=13)
    ax.set_ylabel('Dry Days Anomaly',fontsize=13)
    plt.axhline(y=0,color='k',linestyle='--',linewidth=2)
    plt.legend(loc=(1.02,0.57))

    #Add title and save figures
    plt.title(title_str,fontsize=13)
    plt.savefig(name_str,dpi=200,bbox_inches='tight')
#    plt.close()