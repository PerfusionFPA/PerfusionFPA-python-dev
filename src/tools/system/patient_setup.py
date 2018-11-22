"""
patient_setup.py
Author:  Shant Malkasian
Date: 05/14/2018
Description:  This module contains functions that will be used to transfer files from a PACS directory to a file-server.
Currently, PatientSetup is the main executable function, which organizes patient cardiac CT data from multiple exam images
into similar acquisitions.  By organizing image data, calculating perfusion is more streamlined.
"""

import os
import pydicom
from collections import defaultdict as df
import re
from shutil import copyfile

def patient_setup( src_dir, dest_dir ):
    """
    PatientSetup
    This function organizes patient images into a readable format, to allow for streamlined processing
    and easy prototyping.  Examples of using this code can be seen in test.py.
    
    INPUTS:
    
    src_dir         STR
                    Path to source directory; each image volume is expected to be organized into
                    its own folder, comprised of DICOM files, where each file is a DICOM file of
                    a 2D slice of the image volume.  This directory should also be specific to
                    one patient.  There is no check to ensure that each image volume is from the
                    same patient (that should probably be added).
                    
    dest_dir        STR
                    Path to destination directory; this path should be specific to a single
                    patient.
        
    """
    if os.path.exists(dest_dir):
        print('patient_setup: FAILED \nDESTINATION DIRECTORY: {DEST} ALREADY EXISTS'.format(DEST=dest_dir))
        return False
    if not os.path.exists(src_dir):
        print('patient_setup: FAILED \nSOURCE DIRECTORY: {SRC} DOES NOT EXIST'.format(SRC=src_dir))
        return False
    fp_queue = mkdir_acquisitions(src_dir, dest_dir)[0]
    mv_dcm_dir(fp_queue)
    n_vols_xferred = len(fp_queue)
    fp_queue = mkdir_misc_dcm(src_dir, dest_dir, {'SUB_FOLDER' : 'MISC'})
    mv_dcm_dir(fp_queue)
    n_dcm_misc_xferred = len(fp_queue)

    print('TRANSFER COMPLETE FOR: {DEST}\nVOLUMES TRANSFERRED: {NVOL}  |  MISC DCM TRANSFERED: {NDCMMISC}'.format(DEST=dest_dir,
                                                                                                                  NVOL=n_vols_xferred,
                                                                                                                  NDCMMISC=n_dcm_misc_xferred))
    return True
    
    
def mkdir_acquisitions( src_dir, dest_dir, params=None ):
    """
    mkdir_acquisitions
    
    Base function to organize patient acquisitions into sub-folders for a patient.  Currently,
    this function searches the following DICOM tags, in order to organize image data:
    DCM NAME         DCM NUMBER
    PROTOCOL TYPE    0x00181030         This tag describes whether the acquisition was a
                                        STRESS exam or REST exam
    FILTER TYPE      0x7005100b         The type of reconstruction filter applied (AIDR 3D usually)
    RECON TYPE       0x70051006         Reconstruction type; HALF or FULL reconstruction
    KERNEL TYPE      0x00181210         Kernel used for reconstruction (FC03 or FC12 usually)
    
    Although params is provided as an input, it serves no function currently.  It is just a place
    holder for future-proofing, in case further functionality is desired.
    
    """
    
    # TODO:  CLEAN CODE AND BREAK UP COMPONENTS INTO SUBFUNCTIONS; CODE CAN ALSO BE GENERALIZED...
    # UNPACK PARAMETERS
    # C:\Users\smalk\Desktop\EXAMPLE\DEST_DIR\AIDR3D_Standard_FC03\Acq01_Stress\DICOM
    # PATIENT_DIR............................\FILTERTYPE..........\ACQDD_COMMENT...\DICOM)
    template_acq_vol_dir = '{PATIENTDIR}/{FILTERTYPE}/Acq{ACQNUM:02d}_{ACQTYPE}/DICOM/{VOLUMEDIR}/' # TODO: GENERALIZE
    
    # GET ALL VOLUMES:
    all_dcm_vols = find_vol_dcm(src_dir)
    sorted(all_dcm_vols)
    
    # FIND PROTOCOL AND FILTER TYPES:
    protocol_types = set(tag[0x00181030].value for k, tag in all_dcm_vols.items())
    filter_types = set(tag[0x7005100b].value.decode('utf-8').strip() for k, tag in all_dcm_vols.items())
    kernel_types = set(tag[0x00181210].value.strip() for k, tag in all_dcm_vols.items())
    recon_types = set(tag[0x70051006].value.decode('utf-8').strip() for k, tag in all_dcm_vols.items())
    [sorted(protocol_types), sorted(filter_types), sorted(kernel_types), sorted(recon_types)]
    # SORT VOLUMES INTO APPROPRIATE FOLDERS:
    #  File hierarchy will be saved as a dictionary first, for future-proofing
    #  Save image data in directories as we do now is not scalable
    acq_dict = df(dict)
    fp_queue = [ ] # SIMPLE LIST OF DICT ENTRIES, SIMPLIFIED TO USE FOR FILE TRANSFER
    for rtype in recon_types: # TODO: GENERALIZE FOR LOOP AND FOLDER CRITERIA
        for ktype in kernel_types:
            for ftype in filter_types:
                for ptype in protocol_types: 
                    # FIND ALL VOLUMES IN SPECIFIC ACQUISITION (USUALLY ONLY 2, UNLESS CFA)
                    acq_vols = find_vol_dcm(src_dir, {0x7005100b : ftype,
                                                      0x00181030 : ptype,
                                                      0x00181210 : ktype,
                                                      0x70051006 : rtype,
                                                      })
                    sorted(acq_vols)
                    
                    # ENTER VOLUMES IN DICT acq_dict[cur_ftype][acqn_acqtype] 
                    cur_ftype = ftype.replace(' ', '_') + '_'+ ktype
                    cur_acqtype = re.search('(REST)|(STRESS)', ptype).group(0) + '_' + rtype
                    
                    if cur_ftype not in acq_dict.keys():
                        # APPEND
                        acq_dict[cur_ftype] = df(dict)
                    
                    cur_acqnum = 1
                    cur_acq = 'Acq{:02d}'.format(cur_acqnum)
                    while cur_acq in acq_dict[cur_ftype].keys():
                        cur_acqnum += 1
                        cur_acq = 'Acq{:02d}'.format(cur_acqnum)
                        
                    vol_num = 1
                    for k, v in acq_vols.items():
                        # CREATE PATHS
                        cur_dest_path = template_acq_vol_dir.format(PATIENTDIR=dest_dir,
                                                                    FILTERTYPE=cur_ftype,
                                                                    ACQNUM=cur_acqnum,
                                                                    ACQTYPE=cur_acqtype,
                                                                    VOLUMEDIR=os.path.basename(k))
                        acq_dict[cur_ftype][cur_acq][vol_num] = {'DEST_PATH' : cur_dest_path,
                                                                 'SRC_PATH'  : k,
                                                                 'TAGS_DCM'  : v, # DO WE WANT THE DCM TAGS TO BE SAVED HERE?
                                                                }
                        fp_queue.append({'DEST_PATH' : cur_dest_path,
                                         'SRC_PATH'  : k,})
                        vol_num += 1
    return fp_queue, acq_dict

# HELPER FUNCTIONS

def mkdir_misc_dcm(src_dir, dest_dir, params=None):
    """
    mkdir_misc_dcm
    
    Base function to find and save DICOM image data that is NOT a volume image
    """
    template_dest_dir = '{PATIENTDIR}/{MISCDIR}/{DCMDIR}'
    misc_dcm_files = find_misc_dcm(src_dir)
    fp_queue = [ ]
    for k, v in misc_dcm_files.items():
        cur_dest_path = template_dest_dir.format(PATIENTDIR=dest_dir,
                                                 MISCDIR=params['SUB_FOLDER'],
                                                 DCMDIR=os.path.basename(k))
        fp_queue.append({'DEST_PATH'    : cur_dest_path,
                         'SRC_PATH'     : k})
    return fp_queue
         

def find_misc_dcm( src_dir ):
    """
    find_misc_dcm
    
    Helper function to find miscellaneous DICOM files, or DICOM files that are not image volumes.
    """
    dcm_files = [os.path.join(dp, f) for dp, dn, fn in os.walk(src_dir) for f in fn[:2] if f.endswith('dcm')]
    dcm_vol_dirs = list(find_vol_dcm(src_dir).keys())
    return {os.path.dirname(fn) : pydicom.dcmread(fn) for fn in dcm_files if os.path.dirname(fn) not in dcm_vol_dirs }


def find_vol_dcm( src_dir, search_dcm={0x00180050 : '0.5'}):
    """
    find_vol_dcm
    
    Helper function to find directories of DICOM image volumes.  Currently, I have defined a 'DICOM
    image volume' as any set of DICOM images, where the 'Slice Thickness'<0x00180050> is 0.5.  This
    should be refined in the future, to be more robust.
    """
    def tag_in_dcm( k_, fn_, search_dcm_):
        if k_ not in pydicom.dcmread(fn_).keys():
            return False
        cur_value = pydicom.dcmread(fn_)[k_].value
        # INSERT SPECIAL CASES HERE... SHOULD BE GENERALIZED
        if type(cur_value) == str:
            return cur_value.strip() == search_dcm_[k_].strip()
        elif type(cur_value) == bytes:
            return cur_value.decode('utf-8').strip() == search_dcm_[k_].strip()
        elif type(cur_value) == pydicom.valuerep.DSfloat:
            return str(cur_value).strip() == search_dcm_[k_].strip()
        elif type(cur_value) == pydicom.multival.MultiValue:
            return all(c in search_dcm_[k_] for c in cur_value)
            
    dcm_files = [os.path.join(dp, f) for dp, dn, fn in os.walk(src_dir) for f in fn[:6] if f.endswith('dcm')]    
    return {os.path.dirname(fn) : pydicom.dcmread(fn) for fn in dcm_files 
            if all(tag_in_dcm(k, fn, search_dcm) for k in search_dcm.keys())}
    
def mv_dcm_dir( fp_queue ):
    """
    mv_dcm_dir
    
    Helper function to copy DICOM images from a source directory to a destination directory.
    fp_queue is expected to be a list of dictionary entries.  Each dictionary should have
    fields 'SRC_PATH' and 'DEST_PATH', where the source and destination paths to DICOM
    image directories for the source and destinations to copy files to are provided,
    respectively.
    """
    def check_dir(dir_):
        ls_dir = os.path.normpath(dir_).split(os.sep)
        for i in range(len(ls_dir)):
            cur_dir = os.sep.join(ls_dir[:i+1])
            if not os.path.exists(cur_dir):
                os.mkdir(cur_dir)
                    
    def mv_dcm(src_, dest_):
        print('MOVING {SRC} -> {DEST}'.format(SRC=src_, DEST=dest_))
        check_dir(dest_)
        for f in os.listdir(src_):
            if f.endswith('.dcm'):
                src_f = os.path.join(src_, f)
                dest_f = os.path.join(dest_, f)
                copyfile(src_f, dest_f)
                
                
    for file_mv in fp_queue:
        cur_src_path = file_mv['SRC_PATH']
        cur_dest_path = file_mv['DEST_PATH']
        if os.path.exists(cur_dest_path):
            continue
        mv_dcm(cur_src_path, cur_dest_path)
        
        


