#!/bin/bash
# MASTER SCRIPT
# To run all the scripts for the automatic production of both forecasts/verifications

source $HOME/.bashrc

#module load python/3.5.0
#module load python library

export PYTHON=/scratch/singadm/pkg_helios/Python/3.5.0/bin/python
export PYTHONPATH=/scratch/singadm/pkg_helios/Python/3.5.0/lib/python3.5/site-packages

scriptdir='/home/rkang/test_2018/code' #Change this line only!

# To run TRMM Obs's production script first
cd $scriptdir/obs/prec/ #Locate the correct directory to run the setting.ini file
$PYTHON $scriptdir/obs/prec/process_trmm_threshold.py
echo -ne "TRMM Production done! \r\n"

# Next, to run ECMWF Model's production scripts
cd $scriptdir/model/ecmwf/prec/ #Locate the correct directory to run the setting.ini file
$PYTHON $scriptdir/model/ecmwf/prec/1.preprocess_ecmwf_prec_daily.py
echo -ne "Preprocessing of ECMWF data done! \r\n"
$PYTHON $scriptdir/model/ecmwf/prec/2.process_ecmwf_threshold_weekly.py
echo -ne "Processing of ECMWF Weekly threshold Production done! \r\n"

# To run all verification scripts last
$PYTHON $scriptdir/model/ecmwf/prec/3.process_verification_anomaly_threshold.py
echo -ne "Verification of ECMWF Weekly threshold (Anomaly) done! \r\n"
$PYTHON $scriptdir/model/ecmwf/prec/4.process_verification_total_threshold_v3.py
echo -ne "Verification of ECMWF Weekly threshold (Total) done! \r\n"

######## END
