from patient_setup import find_vol_dcm, mkdir_Acquisitions, PatientSetup
from pprint import pprint
from collections import defaultdict as df

SRC_DIR = 'C:/Users/Shant Malkasian/Desktop/HUMAN_TRIALS/EXAMPLE/SRC_DIR'
DEST_DIR = 'C:/Users/Shant Malkasian/Desktop/HUMAN_TRIALS/EXAMPLE/DEST_DIR'
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