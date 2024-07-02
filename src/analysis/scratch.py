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

# Dicom creation Script
@author: ftan1

import numpy as np
import pydicom as pyd
import datetime
import os
import glob
import sys
import imoco_recon.imoco_py.sigpy_e.cfl as cfl


# set image dir
image_dir = '/container_data/iMRH0074B'
image_file = image_dir + 'raw_data/MRI_Raw_imoco'

# load image
im = np.abs(cfl.read_cfl(image_file))
#im = np.transpose(im[::-1,::-1,:], axes=[2,0,1])
im = np.transpose(im[:,::-1,::-1], axes=[0,2,1])
# exam number, series number
dcm_ls = glob.glob(image_dir +'/BaseRecon'+ '/*.dcm')


    # load original dicom
series_mimic_dir = dcm_ls[0]
ds = pyd.dcmread(series_mimic_dir)

# parse exam number, series number
dcm_file = os.path.basename(series_mimic_dir)
exam_number, series_mimic, _ = dcm_file.replace('Exam', '').replace('Series', '_').replace('Image','_').replace('.dcm','').split('_')
exam_number = int(exam_number)
series_write = int(series_mimic) + 10  #  adding 10, this should ensure no overlap with other series numbers for Philips numbering which uses series number (in order acquired) *100 

# modified time
dt = datetime.datetime.now()
    #ds.FileModTime = dt.strftime('%Y%m%d%H%M%S.%f') + '-0800' # PST
    
ds.SeriesDescription = "3D UTE iMoCo"
    
        # Update SliceLocation information
series_mimic_slices = np.double(ds.Columns)  # assume recon is isotropic
SliceLocation_center = ds.SliceLocation - (series_mimic_slices-1)/2*ds.SpacingBetweenSlices
ImagePosition_zcenter = ds.ImagePositionPatient[2] + (series_mimic_slices-1)/2*ds.SpacingBetweenSlices

im_shape = np.shape(im)
ds.Columns, ds.Rows= im_shape[-2], im_shape[-1]
spatial_resolution = ds.SliceThickness

ds.SpacingBetweenSlices = spatial_resolution
ds.PixelSpacing = [spatial_resolution, spatial_resolution]
ds.SliceThickness = spatial_resolution
ds.ReconstructionDiameter = spatial_resolution*im_shape[-1]

SliceLocation_original = ds.SliceLocation
ImagePositionPatient_original = ds.ImagePositionPatient

series_write_dir = image_dir + 'imoco_recon' #+ str(series_write)
try:
        os.mkdir(series_write_dir)
except OSError as error:  
        # print(error)
        pass
        
im = np.abs(im)  / np.amax(np.abs(im)) * 4095 #65535
im = im.astype(np.uint16)

    # Window and level for the image
ds.WindowCenter = int(np.amax(im)/2)
ds.WindowWidth = int(np.amax(im))

    # dicom series UID
ds.SeriesInstanceUID = pyd.uid.generate_uid()

    # not currently accounting for oblique slices...
for z in range(im_shape[0]):
        ds.InstanceNumber = z+1;
        ds.SeriesNumber = series_write
        ds.SOPInstanceUID = pyd.uid.generate_uid()
        ds.file_meta.MediaStorageSOPInstanceUID = ds.SOPInstanceUID # SOPInstanceUID should == MediaStorageSOPInstanceUID
        Filename = '{:s}/E{:d}S{:d}I{:d}.DCM'.format(series_write_dir, exam_number, series_write, z+1)
        ds.SliceLocation = SliceLocation_original + (im_shape[0]/2 - (z+1)) * spatial_resolution;
        ds.ImagePositionPatient = pyd.multival.MultiValue(float, [float(ImagePositionPatient_original[0]), float(ImagePositionPatient_original[1]), ImagePositionPatient_original[2] - (im_shape[0]/2 - (z+1)) * spatial_resolution])
        b = im[z,:,:].astype('<u2')
        ds.PixelData = b.T.tobytes()
        #ds.is_little_endian = False
        ds.save_as(Filename)