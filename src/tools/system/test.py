from patient_setup import find_vol_dcm, sort_vol_dcm_acq
from pprint import pprint

def test_find_vol_dcm():
    src_dir = 'C:/Users/smalk/Desktop/EXAMPLE/SRC_DIR'
    
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
    
    pprint(find_vol_dcm(src_dir, search_dcm))
    # Should only find TWO volumes with the provided search criteria
    assert(len(find_vol_dcm(src_dir, search_dcm)) == 2)
    
def test_sort_vol_dcm_acq():
    src_dir = 'C:/Users/smalk/Desktop/EXAMPLE/SRC_DIR'
    search_dcm = {0x7005100b : 'AIDR 3D STD',
                  0x70051006 : 'FULL',
                  0x00181030 : 'CARDIAC REST CTP + CTA',
                  0x00080008 : ['ORIGINAL','PRIMARY', 'AXIAL'],
                  }
    cur_dcm_vols = find_vol_dcm(src_dir, search_dcm)
    sort_vol_dcm_acq(cur_dcm_vols)
    

if __name__ == '__main__':
    test_find_vol_dcm()
    test_sort_vol_dcm_acq()