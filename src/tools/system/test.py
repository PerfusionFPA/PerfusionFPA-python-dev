"""
test.py
Author:  Shant Malkasian
Date: 05/14/2018
Description:  This module provides preliminary tests for tools.system modules
"""

import os
import shutil
import pydicom
import unittest

from tools.system.patient_setup import find_vol_dcm, mkdir_acquisitions, patient_setup


def create_test_vol_dcm( dcm_dir, dcm_info, nslices = 5 ):
    def mk_dcm(dcm_path, meta):
        file_meta = pydicom.Dataset()
        file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2'
        file_meta.MediaStorageSOPInstanceUID = "1.2.3"
        file_meta.ImplementationClassUID = "1.2.3.4"
        ds = pydicom.FileDataset(dcm_path, {}, file_meta=file_meta, preamble=b"\0" * 128)
        ds.is_little_endian = True
        ds.is_implicit_VR = True
        [ds.add_new(k,'LO', v) for k, v in meta.items()]
        ds.save_as(dcm_path)
        
    if not os.path.exists(dcm_dir):
        os.mkdir(dcm_dir)
    fname_template = '{:04d}.dcm'
    for i in range(nslices):
        cur_dcm_path = os.path.join(dcm_dir, fname_template.format(i))
        mk_dcm(cur_dcm_path, dcm_info)

class PatientSetup(unittest.TestCase):
    def setUp(self):
        self.test_dir = './../../../unittest/'
        self.src_dir = os.path.join(self.test_dir, 'src_dir')
        self.dest_dir = os.path.join(self.test_dir, 'dest_dir')
        self.dcm_tags = {0x7005100b : 'AIDR 3D STD',
                         0x70051006 : 'FULL',
                         0x00181030 : 'CARDIAC REST CTP + CTA',
                         0x00080008 : ['ORIGINAL','PRIMARY', 'AXIAL'],
                         0x00180050 : '0.5',
                         0x00181210 : 'FC03'
                         }
        if not os.path.exists(self.test_dir):
            os.mkdir(self.test_dir)
        if not os.path.exists(self.src_dir):
            os.mkdir(self.src_dir)

        self.n_slices = 50
        self.n_acqs = 5
        for i in range(self.n_acqs):
            create_test_vol_dcm(os.path.join(self.src_dir, 'testvol{}'.format(i)), self.dcm_tags, self.n_slices)
    
    def tearDown(self):
        shutil.rmtree(self.test_dir)
    
    def test_find_vol_dcm_default(self):
        self.assertEqual(len(find_vol_dcm(self.src_dir, self.dcm_tags)), self.n_acqs)
    
    def test_find_vol_dcm_none(self):
        self.assertEqual(len(find_vol_dcm(self.src_dir, {0x7005100b : 'NONE'})), 0)
    
    def test_mkdir_acquisitions(self):
        fp_queue, acq_dict = mkdir_acquisitions(self.src_dir, self.dest_dir, None)
        self.assertEqual(len(fp_queue), self.n_acqs)
        self.assertEqual(len(acq_dict['AIDR_3D_STD_FC03']), 1)
    
    def test_PatientSetup(self):
        self.assertTrue(patient_setup(self.src_dir, self.dest_dir))
        self.assertFalse(patient_setup(self.src_dir, self.dest_dir))
    
    


if __name__ == '__main__':
    unittest.main()