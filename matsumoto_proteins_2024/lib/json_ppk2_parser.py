from .json_parser import JsonParser
from . import common

common.set_environment_variable()

class Ppk2JsonParser(JsonParser):
    def __init__(self,file_path):
        super().__init__(file_path)
        self.gene_distance_th = 500 
 