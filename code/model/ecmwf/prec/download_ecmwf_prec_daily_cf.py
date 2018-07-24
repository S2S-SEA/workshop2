#!/usr/bin/env python
'''
This program downloads the ECMWF hindcast data using MARS.
The example is for Dec 2017 run for all model output that
fall within Dec for control forecast ('cf').
Choice of 1998-2014 for download corresponds to TRMM data
available for the verification later.
'''
from subprocess import call # This library needed to make system call
from ecmwfapi import ECMWFDataServer # Load the ECMWF API library
server = ECMWFDataServer()
import configparser
config = configparser.ConfigParser()
config.read('../../../../code/settings.ini')

# All the initial dates that have full weeks in Dec
init_date = config.get('Download','init_date').split(',')

# Define data folder, and create it
dest_dir = '../../../../data/model/ecmwf/prec/'
call("mkdir -p " + dest_dir, shell=True)

# Remove all *cf.nc files, else grib_to_netcdf will convert with "protocol error"
#call("rm -rf " + dest_dir + "*_cf.nc", shell=True)

# For each initial date
for i in range(0, len(init_date)):
    server.retrieve({
        "class": "s2",
        "dataset": "s2s",
        "date": "2017-" + init_date[i],
        "expver": "prod",
        "hdate": "2014-" + init_date[i] + "/2013-" + init_date[i] + "/2012-" + init_date[i] + "/2011-" + init_date[i] + "/2010-" + init_date[i] + "/2009-" + init_date[i] + "/2008-" + init_date[i] + "/2007-" + init_date[i] + "/2006-" + init_date[i] + "/2005-" + init_date[i] + "/2004-" + init_date[i] + "/2003-" + init_date[i] + "/2002-" + init_date[i] + "/2001-" + init_date[i] + "/2000-" + init_date[i] + "/1999-" + init_date[i] + "/1998-" + init_date[i],
        "levtype": "sfc",
        "model": "glob",
        "origin": "ecmf",
        "param": "228228",
        "step": "0/to/672/by/24",
        "area": "30/80/-20/150",
        "stream": "enfh",
        "target": dest_dir + "ECMWF_prec_2017_daily-" + init_date[i] + "_cf.grib",
        "time": "00:00:00",
        "type": "cf",
    })

    # Convert from grib to netcdf using ECMWF Grib API
    call("grib_to_netcdf -M -I method,type,stream,refdate -T -o " + dest_dir + "ECMWF_prec_2017_daily-" + init_date[i] + "_cf.nc " + dest_dir + "ECMWF_prec_2017_daily-" + init_date[i] + "_cf.grib", shell=True)
    # Remove the grib file after download
    call("rm -rf " + dest_dir + "ECMWF_prec_2017_daily-" + init_date[i] + "_cf.grib", shell=True)
