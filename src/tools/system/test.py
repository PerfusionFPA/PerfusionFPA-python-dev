"""
test.py
Author:  Shant Malkasian
Date: 05/14/2018
Description:  This module provides preliminary tests for tools.system modules
"""

import os
import pydicom
from tools.system.patient_setup import find_vol_dcm, mkdir_Acquisitions, PatientSetup

TEST_DIR = './../../../unittest/'
SRC_DIR = os.path.join(TEST_DIR, 'SRC_DIR')
DEST_DIR = os.path.join(TEST_DIR, 'DEST_DIR')

if not os.path.exists(SRC_DIR):
    os.mkdir(SRC_DIR)
if not os.path.exists(DEST_DIR):
    os.mkdir(DEST_DIR)

def create_test_vol_dcm( dcm_dir, dcm_info, nslices = 5 ):
    def add_dcm_info(cur_dcm_meta_, dcm_info_):
        [cur_dcm_meta_.setdefault(k, v) for k, v in dcm_info_.items()]
        return cur_dcm_meta_
    if not os.path.exists(dcm_dir):
        os.mkdir(dcm_dir)
    fname_template = 'slice{:02d}.dcm'
    for i in range(nslices):
        cur_dcm_path = os.path.join(dcm_dir, fname_template.format(i))
        cur_dcm_meta = add_dcm_info(pydicom.Dataset(), dcm_info)
        pydicom.FileDataset(cur_dcm_path, {}, file_meta=cur_dcm_meta).save_as(cur_dcm_path)
        
        

def test_find_vol_dcm():
    
    #  NOTE:  to search for specific DICOM tag, follow this paradigm:
    #  TAG          -> VALUE 
    #  (7005, 1006) -> 'HALF'
    #  TO SEARCH CONVERT TAG ABOVE TO:
    #  0x70051006
    
    #             TAG          VALUE
    search_dcm = {0x7005100b : 'AIDR 3D STD',
                  0x70051006 : 'FULL',
                  0x00181030 : 'CARDIAC REST CTP + CTA',
                  0x00080008 : ['ORIGINAL','PRIMARY', 'AXIAL'],
                  }
    create_test_vol_dcm(os.path.join(SRC_DIR, 'TESTVOL1'), search_dcm)
    # Should only find TWO volumes with the provided search criteria
    assert(len(find_vol_dcm(SRC_DIR, search_dcm)) == 2)
    
def test_mkdir_Acquisitions():
    fp_queue, acq_dict = mkdir_Acquisitions(SRC_DIR, DEST_DIR, None)
    assert(len(fp_queue) == 7)
    assert(len(acq_dict['AIDR_3D_STD_FC03']) == 3)

def test_PatientSetup():
    dest_dir = 'C:/Users/Shant Malkasian/Desktop/HUMAN_TRIALS/EXAMPLE/PATIENT_1'
    PatientSetup(SRC_DIR, dest_dir )

if __name__ == '__main__':
    test_find_vol_dcm()
    test_mkdir_Acquisitions()
    test_PatientSetup()