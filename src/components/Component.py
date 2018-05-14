import abc
import json

class Component(abc.ABC):
    """ABSTRACT CLASS: Component
    Abstract parent class that will be used to create concrete, specialized components for pipeline processing
    """
    # BUILTIN
    def __init__(self, stream):
        #CHECK INPUTS
        
        #UNPACKAGE INPUTS
        self.stream = stream
        self.component_routine()
        super(Component, self).__init__()
        
    # PUBLIC
    @abc.abstractmethod
    def component_routine(self):
        pass
    
    def push_stream(self):
        return self.stream
    
    # PRIVATE
    def _tag_stream(self, var_tags=['all'], stream_type_tags=['']):
        if type(var_tags) != list:
            var_ids = [var_tags]
            
        for k in list(self.stream.keys()):
            for v in list(self.stream[k].keys()):
                if 'all' in var_ids or self.stream[k][v]['id'] in var_ids or k in stream_type_tags:
                    self.stream[k][v]['history'].append(self.__class__.__name__)
        
        
class InitComponent(Component):
    """CONCRETE CLASS: InitComponent
    Concrete class used to convert a json stream into a dictionary, to allow for data to be passed in Python
    """
    
    # PUBLIC
    def component_routine(self):
        print('Initialization Routine')
        open_json = self.stream
        self.stream = json.load(open_json)
        open_json.close()
        self._tag_stream()
    
class LoadFileComponent(Component):
    """CONCRETE CLASS: LoadFileComponent
    Concrete class used to load files specified in the stream; during the same pipeline routine a streamed variable will only be loaded once
    """
    
    # PUBLIC
    def component_routine(self):
        var_type = 'INPUT_FILE_PATHS'
        
        
        
    

