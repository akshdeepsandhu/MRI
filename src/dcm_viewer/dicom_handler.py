import pydicom
import numpy as np 


def load_dicom_series(dicom_dir : str) -> np.ndarray: 
    dicom_files = sorted([os.path.join(dicom_dir, f) for f in os.listdir(dicom_dir) if f.endswith('.DCM')])
    
    slices = [pydicom.dcmread(dcm) for dcm in dicom_files]
    slices.sort(key=lambda x: int(x.InstanceNumber))  # Sort by slice order
    
    # stack and make into 3d volume
    volume = np.stack([s.pixel_array for s in slices], axis=-1)
    return volume

def plot_slice(volume, x=None, y=None, z=None):
    if x is not None:
        slice_2d = volume[x, :, :]
        title = f'Slice at X={x}'
    elif y is not None:
        slice_2d = volume[:, y, :]
        title = f'Slice at Y={y}'
    elif z is not None:
        slice_2d = volume[:, :, z]
        title = f'Slice at Z={z}'
    else:
        raise ValueError("One of x, y, or z must be specified")
    
    return slice_2d, title