# REQUIRES:
# python 3.6
# pydicom

import os
import pydicom
from collections import defaultdict as df
from pprint import pprint

def PatientSetup( src_dir, dest_dir ):
    pass




# COMPONENTS
def mkdir_Acquisitions( src_dir, dest_dir, params ):
    # UNPACK PARAMETERS
    # C:\Users\smalk\Desktop\EXAMPLE\DEST_DIR\AIDR3D_Standard_FC03\Acq01_Stress_CTP_AIDR3D_Standard_FC03\DICOM
    # PATIENT_DIR............................\FILTERTYPE..........\ACQDD_COMMENT....FILTERTYPE..........\DICOM
    cur_dest_patient_dir = os.path.join(dest_dir, params['PATIENT_DIR'])
    cur_search_dcm_tags = params['SEARCH_DCM_TAGS']
    template_acq_vol_dir = '{PATIENTDIR}/{FILTERTYPE}/Acq{ACQNUM}_{ACQTYPE}_{FILTERTYPE}/DICOM'
    
    # FIND ALL DICOM VOLUME DIRECTORIES IN SOURCE DIRECTORY
    src_dcm_vols = find_vol_dcm(src_dir, cur_search_dcm_tags)
    
    # SEPARATE SOURCE DIRECTORY VOLUMES INTO ACQUISITIONS
    sort_vol_dcm_acq(src_dcm_vols)
    # MOVE EACH VOLUME TO DESTINATION DIRECTORY

# TEMPLATES
def mkdir_EXAMPLE( src_dir, dest_dir, params ):
    pass


# HELPER FUNCTIONS
def find_vol_dcm( src_dir, search_dcm ):
    def tag_in_dcm( k_, fn_, search_dcm_):
        cur_value = pydicom.dcmread(fn_)[k_].value
        # INSERT SPECIAL CASES HERE... SHOULD BE GENERALIZED
        if type(cur_value) == str:
            return cur_value.strip() == search_dcm_[k_].strip()
        elif type(cur_value) == bytes:
            return cur_value.decode('utf-8').strip() == search_dcm_[k_].strip()
        elif len(cur_value) > 1:
            return all(c in search_dcm_[k_] for c in cur_value)
            
    files = [os.path.join(dp, fn[0]) for dp, dn, fn in os.walk(src_dir) if len(fn) > 0] # THIS COULD BE CHANGED TO >= 100 TO INDICATE A VOLUME
    dcm_files = [fn for fn in files if any(fn.endswith(ext) for ext in ['dcm'])]
           
    return {os.path.dirname(fn) : pydicom.dcmread(fn) for fn in dcm_files 
            if all(tag_in_dcm(k, fn, search_dcm) for k in search_dcm.keys())}
    
def sort_vol_dcm_acq( src_dcm_vols ):
    # FIND ALL ACQUISITIONS
    # SEPARATE AND NUMBER ACQUISITIONS
    # acq_vol_dcm = { dcm_tags[0x002000D] : (fn, dcm_tags)
    #               for fn, dcm_tags in src_dcm_vols}
    acq_vol_dcm = df(list)
    'ACQ'
    #for fn, dcm_tags in src_dcm_vols.items():
    #    acq_vol_dcm['.'.join(dcm_tags[0x0020000E].value.strip().split('.')[:-1])].append((fn, dcm_tags))
    for fn, dcm_tags in src_dcm_vols.items():
        acq_vol_dcm = 0

def mv_vol_dcm( src_dir, dest_dir ):
    #IGNORE BMP HERE
    pass


