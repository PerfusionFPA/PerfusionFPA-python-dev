from tools.system.patient_setup import patient_setup




def init_05_11_2018():
    print('INITIALIZING PATIENT DIRECTORIES...')
    parent_dir = 'F:/bpziemer/HUMAN_PERFUSION_DATA/05_11_18_data_py_auto'
    
    patient_setup('X:/KPACS_Data/1.2.392.200036.9116.2.6.1.48.1216111650.1525997223.225594/',
                 parent_dir + '/PATIENT_5/')
    patient_setup('X:/KPACS_Data/1.2.392.200036.9116.2.6.1.48.1216111650.1526000319.648512/',
                 parent_dir + '/PATIENT_6/')    
    patient_setup('X:/KPACS_Data/1.2.392.200036.9116.2.6.1.48.1216111650.1526003583.454035/',
                 parent_dir + '/PATIENT_7/')
    patient_setup('X:/KPACS_Data/1.2.392.200036.9116.2.6.1.48.1216111650.1526006342.805447/',
                 parent_dir + '/PATIENT_8/')
    patient_setup('X:/KPACS_Data/1.2.392.200036.9116.2.6.1.48.1216111650.1526009142.609754/',
                 parent_dir + '/PATIENT_9/')
    patient_setup('X:/KPACS_Data/1.2.392.200036.9116.2.6.1.48.1216111650.1526012645.312390/',
                 parent_dir + '/PATIENT_10/')
    patient_setup('X:/KPACS_Data/1.2.392.200036.9116.2.6.1.48.1216111650.1526015546.555759/',
                 parent_dir + '/PATIENT_11/')
    patient_setup('X:/KPACS_Data/1.2.392.200036.9116.2.6.1.48.1216111650.1526019325.781743/',
                 parent_dir + '/PATIENT_12/')
    patient_setup('X:/KPACS_Data/1.2.392.200036.9116.2.6.1.48.1216111650.1526022142.640006/',
                 parent_dir + '/PATIENT_13/')

if __name__ == '__main__':
    init_05_11_2018()
