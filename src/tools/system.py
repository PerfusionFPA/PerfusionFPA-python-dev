import os


# HELPER FUNCTIONS
def check_path( dir_path : str ):
    """Checks if dir_path exists, and creates it if it doesn't"""
    
    if not os.path.exists(dir_path):
        print(dir_path)
        os.mkdir(dir_path)
    
    return dir_path


# DEFINE IMPORTANT PATHS
SRC_PATH = os.path.dirname(__file__).replace('tools', '')
JSON_PATH = check_path(os.path.join(SRC_PATH, '../json/'))
BIN_PATH = check_path(os.path.join(SRC_PATH, '../bin/'))
TEST_DATA_PATH = check_path(os.path.join(SRC_PATH, '../test_data/'))
