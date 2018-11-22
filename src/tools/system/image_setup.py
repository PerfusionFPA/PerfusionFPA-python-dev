import pydicom
import os
import numpy
import datetime
import time

def create_test_vol_dcm( dcm_dir, dcm_info, nslices = 5, px_data = [ ] ):
    def mk_dcm(dcm_path, meta):
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
        ds.SecondaryCaptureDeviceManufctur = 'Python 2.7.3'


        
        ds.SamplesPerPixel = 1
        ds.PhotometricInterpretation = "MONOCHROME2"
        ds.PixelRepresentation = 0
        ds.HighBit = 15
        ds.BitsStored = 16
        ds.BitsAllocated = 16
        ds.SmallestImagePixelValue = b'\x00\x00'
        ds.LargestImagePixelValue = b'\xff\xff'
        ds.Columns = px_data.shape[0]
        ds.Rows = px_data.shape[1]
        ds.PixelData = px_data.tobytes()
        [ds.add_new(k,'LO', v) for k, v in meta.items()]
        
            
        ds.save_as(dcm_path)
        
    if not os.path.exists(dcm_dir):
        os.mkdir(dcm_dir)
    fname_template = '{:04d}.dcm'
    for i in range(nslices):
        cur_dcm_path = os.path.join(dcm_dir, fname_template.format(i))
        mk_dcm(cur_dcm_path, dcm_info)
        
def load_vol_dcm( dcm_dir ):
    dcm_paths = [os.path.join(dcm_dir, f) for f in os.listdir(dcm_dir) if f.endswith('.dcm')]
    px_data = []
    for f in dcm_paths:
        if len(px_data) == 0:
            px_data = pydicom.read_file(f).pixel_array
        else:
            px_data = numpy.concatenate((px_data, pydicom.read_file(f).pixel_array), axis=1)
        


if __name__ == '__main__':
    test_dir = 'C:/Users/smalk/Desktop/EXAMPLE/test_dcm'
#     fn_ = 'C:/Users/smalk/Desktop/EXAMPLE/SRC_DIR/1.2.392.200036.9116.2.1216111650.1516935725.5.1065400001.1/1.2.392.200036.9116.2.1216111650.1516935725.145697.1.1.dcm'
#     fn2_ = 'C:/Users/smalk/Desktop/EXAMPLE/SRC_DIR/1.2.392.200036.9116.2.1216111650.1516935725.5.1065400001.1/test00.dcm'
#     tags = pydicom.dcmread(fn_)
#     xx = tags.keys()
#     temp_data = str(tags[0x7FE00010].value)
#     new_data = numpy.zeros((512,512), dtype=numpy.int16)
#     nd = tags.pixel_array
#     tags.PixelData = new_data.tobytes()
#     tags.save_as(fn2_)
#     print()
#     print('COMPLETED')
    
    

    dcm_tags = {0x7005100b : 'AIDR 3D STD',
                0x70051006 : 'FULL',
                0x00181030 : 'CARDIAC REST CTP + CTA',
                0x00080008 : ['ORIGINAL','PRIMARY', 'AXIAL'],
                0x00180050 : '0.5',
                0x00181210 : 'FC03',
                }
    px_data = numpy.zeros((10,10), dtype = numpy.int16)                
    create_test_vol_dcm(test_dir, dcm_tags, 5, px_data)
     
    load_vol_dcm(test_dir)
    

