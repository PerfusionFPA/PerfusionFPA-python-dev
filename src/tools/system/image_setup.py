import pydicom
import os
import numpy
import datetime
import time

def create_test_vol_dcm( dcm_dir, dcm_info, vol_data = numpy.zeros((10,10,10), dtype=numpy.int16) ):
    def mk_dcm(dcm_path, slice_data, meta):
        file_meta = pydicom.Dataset()
        file_meta.TransferSyntaxUID = '1.2.840.10008.1.2'
        file_meta.MediaStorageSOPClassUID = 'Secondary Capture Image Storage'
        file_meta.MediaStorageSOPInstanceUID = '1.3.6.1.4.1.9590.100.1.1.111165684411017669021768385720736873780'
        file_meta.ImplementationClassUID = '1.3.6.1.4.1.9590.100.1.0.100.4.0'
        ds = pydicom.FileDataset(dcm_path, {}, file_meta = file_meta,preamble=b'\0'*128)
        ds.Modality = 'WSD'
        ds.ContentDate = str(datetime.date.today()).replace('-','')
        ds.ContentTime = str(time.time()) #milliseconds since the epoch
        ds.StudyInstanceUID =  '1.3.6.1.4.1.9590.100.1.1.124313977412360175234271287472804872093'
        ds.SeriesInstanceUID = '1.3.6.1.4.1.9590.100.1.1.369231118011061003403421859172643143649'
        ds.SOPInstanceUID =    '1.3.6.1.4.1.9590.100.1.1.111165684411017669021768385720736873780'
        ds.SOPClassUID = 'Secondary Capture Image Storage'
        ds.SecondaryCaptureDeviceManufctur = 'Python 3.6'

        # TAGS NECESSARY TO CONTAIN IMAGE DATA:
        ds.SamplesPerPixel = 1
        ds.PhotometricInterpretation = "MONOCHROME2"
        ds.PixelRepresentation = 1
        ds.HighBit = 15
        ds.BitsStored = 16
        ds.BitsAllocated = 16
        ds.RescaleIntercept = 0
        ds.RescaleSlope = 1
        ds.WindowCenter = 80
        ds.WindowWidth = 600
        ds.Columns = slice_data.shape[0]
        ds.Rows = slice_data.shape[1]
        ds.PixelData = slice_data.tobytes()
        [ds.add_new(k,'LO', v) for k, v in meta.items()]
            
        ds.save_as(dcm_path)
    
    
    if not os.path.exists(dcm_dir):
        os.mkdir(dcm_dir)
    fname_template = '{:04d}.dcm'
    nslices = vol_data.shape[2]
    for i in range(nslices):
        cur_slice = vol_data[:,:,i]
        cur_dcm_path = os.path.join(dcm_dir, fname_template.format(i))
        mk_dcm(cur_dcm_path, cur_slice, dcm_info)
        
def load_vol_dcm( dcm_dir ):
    dcm_paths = [os.path.join(dcm_dir, f) for f in os.listdir(dcm_dir) if f.endswith('.dcm')]
    px_data = []
    for f in dcm_paths:
        if len(px_data) == 0:
            px_data = pydicom.read_file(f).pixel_array
        else:
            px_data = numpy.dstack((px_data, pydicom.read_file(f).pixel_array))
    return px_data



if __name__ == '__main__':
    test_dir = 'C:/Users/smalk/Desktop/EXAMPLE/test_dcm'   
    dcm_tags = {0x7005100b : 'AIDR 3D STD',
                0x70051006 : 'FULL',
                0x00181030 : 'CARDIAC REST CTP + CTA',
                0x00080008 : ['ORIGINAL','PRIMARY', 'AXIAL'],
                0x00180050 : '0.5',
                0x00181210 : 'FC03',
                }
    px_data = numpy.zeros((10,10), dtype = numpy.int16)                
    create_test_vol_dcm(test_dir, dcm_tags, 5, px_data)
     
    new_px_data = load_vol_dcm(test_dir)
    print('Finished')
    

