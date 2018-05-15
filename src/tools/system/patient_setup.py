import os
import pydicom
from collections import defaultdict as df
import re
from shutil import copyfile

def PatientSetup( src_dir, dest_dir ):
    fp_queue = mkdir_Acquisitions(src_dir, dest_dir)[0]
    mv_dcm_dir(fp_queue)
    fp_queue = mkdir_MiscDCM(src_dir, dest_dir, {'SUB_FOLDER' : 'MISC'})
    mv_dcm_dir(fp_queue)
    

# COMPONENTS
def mkdir_Acquisitions( src_dir, dest_dir, params=None ):
    # TODO:  CLEAN CODE AND BREAK UP COMPONENTS INTO SUBFUNCTIONS; CODE CAN ALSO BE GENERALIZED...
    # UNPACK PARAMETERS
    # C:\Users\smalk\Desktop\EXAMPLE\DEST_DIR\AIDR3D_Standard_FC03\Acq01_Stress\DICOM
    # PATIENT_DIR............................\FILTERTYPE..........\ACQDD_COMMENT...\DICOM)
    template_acq_vol_dir = '{PATIENTDIR}/{FILTERTYPE}/Acq{ACQNUM:02d}_{ACQTYPE}/DICOM/{VOLUMEDIR}/' # TODO: GENERALIZE
    
    # GET ALL VOLUMES:
    all_dcm_vols = find_vol_dcm(src_dir, {0x00080060 : 'CT'})
    sorted(all_dcm_vols)
    
    # FIND PROTOCOL AND FILTER TYPES:
    protocol_types = set(tag[0x00181030].value for k, tag in all_dcm_vols.items())
    filter_types = set(tag[0x7005100b].value.decode('utf-8').strip() for k, tag in all_dcm_vols.items())
    kernal_types = set(tag[0x00181210].value.strip() for k, tag in all_dcm_vols.items())
    recon_types = set(tag[0x70051006].value.decode('utf-8').strip() for k, tag in all_dcm_vols.items())
    [sorted(protocol_types), sorted(filter_types), sorted(kernal_types), sorted(recon_types)]
    # SORT VOLUMES INTO APPROPRIATE FOLDERS:
    #  File hierarchy will be saved as a dictionary first, for future-proofing
    #  Save image data in directories as we do now is not scalable
    acq_dict = df(dict) # MORE INFORMATIVE
    fp_queue = [ ] # SIMPLE LIST OF DICT ENTRIES, SIMPLIFIED TO USE FOR FILE TRANSFER
    for rtype in recon_types: # TODO: GENERALIZE FOR LOOP AND FOLDER CRITERIA
        for ktype in kernal_types:
            for ftype in filter_types:
                for ptype in protocol_types: 
                    # FIND ALL VOLUMES IN SPECIFIC ACQUISITION (USUALLY ONLY 2, UNLESS CFA)
                    acq_vols = find_vol_dcm(src_dir, {0x7005100b : ftype,
                                                      0x00181030 : ptype,
                                                      0x00181210 : ktype,
                                                      0x70051006 : rtype,})
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

def mkdir_MiscDCM(src_dir, dest_dir, params=None):
    template_dest_dir = '{PATIENTDIR}/{MISCDIR}/'
    misc_dcm_files = find_misc_dcm(src_dir)
    fp_queue = [ ]
    for k, v in misc_dcm_files:
        cur_dest_path = template_dest_dir.format(PATIENTDIR=dest_dir,
                                                 MISCDIR=params['SUB_FOLDER'])
        fp_queue.append({'DEST_PATH'    : cur_dest_path,
                         'SRC_PATH'     : k})
    return fp_queue
         

def find_misc_dcm( src_dir ):
    files = [os.path.join(dp, fn[1]) for dp, dn, fn in os.walk(src_dir) if len(fn) < 50]
    dcm_files = [fn for fn in files if any(fn.endswith(ext) for ext in ['dcm'])]
    return {os.path.dirname(fn) : pydicom.dcmread(fn) for fn in dcm_files} 


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
            
    files = [os.path.join(dp, fn[1]) for dp, dn, fn in os.walk(src_dir) if len(fn) > 100] # THIS COULD BE CHANGED TO >= 100 TO INDICATE A VOLUME #TODO: GENERALIZE THIS
    dcm_files = [fn for fn in files if any(fn.endswith(ext) for ext in ['dcm'])]
           
    return {os.path.dirname(fn) : pydicom.dcmread(fn) for fn in dcm_files 
            if all(tag_in_dcm(k, fn, search_dcm) for k in search_dcm.keys())}
    
def mv_dcm_dir( fp_queue ):
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
        if not os.path.exists(cur_src_path):
            continue
        mv_dcm(cur_src_path, cur_dest_path)
        
        


