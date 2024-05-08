# let's define paths 
data_path = "/container_data/lung_mri/"
imoco_path = "/usr/src/"
# add to system path
import sys 
import os
sys.path.append(imoco_path)
sys.path.append(data_path)
# import packages 
import numpy as np
import sigpy.plot as pl
import imoco_recon.imoco_py.sigpy_e.cfl as cfl

# start analysis
# 1. Read and subset data 
num_ro = 200
datam = cfl.read_cfl(os.path.join(data_path,'MRI_Raw_datam'))
datam = datam[:,:,:,:,:num_ro,:]
cfl.write_cfl(os.path.join(data_path,'MRI_Raw_datam'), datam)

dcf2m = cfl.read_cfl(os.path.join(data_path,'MRI_Raw_dcf2m'))
dcf2m = dcf2m[:,:,:,:,:num_ro,:]
cfl.write_cfl(os.path.join(data_path,'MRI_Raw_dcf2m'), dcf2m)

trajm = cfl.read_cfl(os.path.join(data_path,'MRI_Raw_trajm'))
trajm = trajm[:,:,:,:,:num_ro,:]
cfl.write_cfl(os.path.join(data_path,'MRI_Raw_trajm'),trajm)

# release RAM
del datam
del dcf2m
del trajm

# 2. iMoCo Reconstruction
!python3 imoco_recon/imoco_py/recon_imoco.py /container_data/lung_mri/MRI_Raw --reg_flag 1 --device -1
