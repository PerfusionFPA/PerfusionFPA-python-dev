import src.tools.system
import src.components.Component
import os
import pprint


if __name__ == '__main__':
    INPUT_STREAM_TEST_JSON_PATH = os.path.join(src.tools.system.JSON_PATH, 'streams/default_stream.json')
    TEST_EXAMPLE1_FILE = os.path.join(src.tools.system.TEST_DATA_PATH, 'example1/dummy_data.csv')
    
    PIPELINE_ROUTINE = [ (src.components.Component.InitComponent, 'Initiating'),
                         (src.components.Component.LoadFileComponent, 'Loading Files') ]
    
    cur_stream = open(INPUT_STREAM_TEST_JSON_PATH) # WILL COME FROM EXTERNAL PROGRAM
    for component in PIPELINE_ROUTINE:
        cur_component = component[0](cur_stream)
        cur_stream = cur_component.push_stream()
    pprint.pprint(cur_stream)
        