"""
test.py
Author:  Shant Malkasian
Date: 05/14/2018
Description:  This module provides preliminary tests for tools.dir modules
"""

import os
import shutil
import unittest
import numpy
from tools.system.patient_setup import find_vol_dcm, mkdir_acquisitions, patient_setup, get_dcm_tag
from tools.system.image_setup import create_test_vol_dcm, load_vol_dcm


class ImageSetup(unittest.TestCase):
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
        self.n_slices = 10
        self.pixel_data = numpy.zeros((10, 10, self.n_slices), dtype=numpy.int16)
        create_test_vol_dcm(os.path.join(self.src_dir, 'testvol{}'.format(0)), self.dcm_tags, self.pixel_data)
        
    def tearDown(self):
        shutil.rmtree(self.test_dir)
    
    def test_create_load_vol_dcm(self):
        test_vol = load_vol_dcm(os.path.join(self.src_dir, 'testvol{}'.format(0)))
        for i in range(self.n_slices):
            self.assertEqual(test_vol[:,:,i].all(), self.pixel_data.all())
    
        

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
        self.pixel_data = numpy.zeros((10,10, self.n_slices), dtype=numpy.int16)
        self.n_acqs = 5
        for i in range(self.n_acqs):
            create_test_vol_dcm(os.path.join(self.src_dir, 'testvol{}'.format(i)), self.dcm_tags, self.pixel_data)
    
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
    
    def test_patient_setup(self):
        self.assertTrue(patient_setup(self.src_dir, self.dest_dir))
        self.assertFalse(patient_setup(self.src_dir, self.dest_dir))

    def test_get_dcm_tag(self):
        test_val, test_kw = get_dcm_tag(self.src_dir + '/testvol1', 0x00180050)
        self.assertTrue(test_val == 0.5)
        self.assertTrue(test_kw == 'SliceThickness')
        
        test_val, test_kw = get_dcm_tag(self.src_dir + '/testvol1', None)
        self.assertTrue(test_val == None)
        self.assertTrue(test_kw == None)
        
if __name__ == '__main__':
    unittest.main()