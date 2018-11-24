import tools.system.image_setup as tools_im
import tools.system.patient_setup as tools_patient
import numpy


if __name__ == '__main__':
    test_dir = 'C:/Users/smalk/Desktop/EXAMPLE/PERFUSION/'
    dcm_tags = {0x7005100b : 'AIDR 3D STD',
                0x70051006 : 'FULL',
                0x00181030 : 'CARDIAC REST CTP + CTA',
                0x00080008 : ['ORIGINAL','PRIMARY', 'AXIAL'],
                0x00180050 : '0.5',
                0x00181210 : 'FC03',
                0x00280030 : '0.470\\0.470'
                }
    imsize = (512, 512, 50)
    # CREATE ORGAN MASK:
    organ_mask = numpy.zeros(imsize, dtype=numpy.bool)
    aif_mask = numpy.zeros(imsize, dtype=numpy.bool)
    organ_mask[300:400, 300:400, 25:35] = True
    aif_mask[50:150, 100:150, 25:35] = True

    
    # CREATE VOL1:
    vol1_array = numpy.zeros(imsize, dtype=numpy.int16)
    vol1_array[organ_mask] = 75
    vol1_array[aif_mask] = 75
    tools_im.create_test_vol_dcm(test_dir + 'VOL1_dcm', dcm_tags, vol1_array)
        
    # CREATE VOL2:
    vol2_array = numpy.zeros(imsize, dtype=numpy.int16)
    vol2_array[aif_mask] = 800
    vol2_array[organ_mask] = 350
    tools_im.create_test_vol_dcm(test_dir + 'VOL2_dcm', dcm_tags, vol2_array)
    
    # LOAD VOL1:
    vol1 = tools_im.load_vol_dcm(test_dir + 'VOL1_dcm')
    
    # LOAD VOL2:
    vol2 = tools_im.load_vol_dcm(test_dir + 'VOL2_dcm')
    
    # GET TAGS:
    slice_thickness = float(tools_patient.get_dcm_tag(test_dir + 'VOL1_dcm', 0x00180050)[0])
    in_plane_size = [float(n) for n in tools_patient.get_dcm_tag(test_dir + 'VOL1_dcm', 0x00280030)[0]]
    
    
    # CALCULATE PERFUSION:
    vol2_integrated_mass = sum(vol2[organ_mask])
    
    vol1 = tools_im.load_vol_dcm(test_dir + 'VOL1_dcm')
    vol1_integrated_mass = sum(vol1[organ_mask])
    aif_conc = numpy.mean([numpy.mean(vol2[aif_mask]), numpy.mean(vol1[aif_mask])])
    
    organ_mass_vx = numpy.sum(organ_mask)
    organ_mass_g = organ_mass_vx * 1.053 * in_plane_size[0]**2 * slice_thickness / 1000
    
    # CALCULATE PERFUSION
    flow = (1/aif_conc) * (vol2_integrated_mass - vol1_integrated_mass) * (in_plane_size[0]**2) / 1000
    perfusion = flow / organ_mass_g
    print(organ_mass_g)
    print(flow)
    print(perfusion)
    
    

