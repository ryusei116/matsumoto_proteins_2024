import json
import re
from . import common
common.set_environment_variable()
from . import taxonomy_tools as taxonomy_tools
 
class JsonParser():
    def __init__(self,file_path):
        self.file_path = file_path
        self.gene_distance_th = float('inf')
        self.finished_target_accession_keys = []
        self.dict_data = self.json2dict()

    def json2dict(self):
        encoding = "utf-8"
        with open(self.file_path,encoding=encoding) as f:
            dict_data = json.load(f)
        return dict_data
    
    def return_gathering_object(self,target_accession_key,neighborhood_index,gathering_object):
        neighborhood_dict = self.dict_data[target_accession_key][self.gene_position_keys_dup[neighborhood_index]]
        if (neighborhood_dict["gene_accession"] not in self.finished_target_accession_keys) and (int(neighborhood_dict["gene_distance"]) <= self.gene_distance_th ):
            return neighborhood_dict[gathering_object]
        else:
            return None

    def fetch_nearest_domain(self,target_accession_key,gathering_object):
        #domain
        gathering_list = []
        gene_position_keys = list(self.dict_data[target_accession_key].keys())
        self.gene_position_keys_dup = [gene_position_key for gene_position_key in gene_position_keys if self.dict_data[target_accession_key][gene_position_key] != {}]
        n0_index = self.gene_position_keys_dup.index('n0')
        left_neighborhood_index = n0_index - 1 # get neighborhood index
        right_neighborhood_index = n0_index + 1
        if left_neighborhood_index >= 0:
            gathering_list.append(self.return_gathering_object(target_accession_key,left_neighborhood_index,gathering_object))
        if right_neighborhood_index < len(self.gene_position_keys_dup):
            gathering_list.append(self.return_gathering_object(target_accession_key,right_neighborhood_index,gathering_object))
        gathering_list = list(filter(None, gathering_list))
        return gathering_list

    def fetch_nearest_domain_dict(self):
        targetgene_accession_keys = list(self.dict_data.keys())
        targetgene_accession_keys.remove('query_domain')
        output = {"nearest_domain_dict" : {}, "nearest_accession_dict" : {}}
        if not targetgene_accession_keys:
            return output
        for gathering_target_key in output.keys():
            if gathering_target_key == "nearest_domain_dict":
                gathering_object = "domain_annotation"
            elif gathering_target_key == "nearest_accession_dict":
                gathering_object = "gene_accession"
            for target_accession_key in targetgene_accession_keys:
                output[gathering_target_key][target_accession_key] = self.fetch_nearest_domain(target_accession_key,gathering_object)
                self.finished_target_accession_keys.append(target_accession_key)
            self.finished_target_accession_keys = []
        return output
    
    def fetch_org_having_specific_nearest_domain(self,sp_nearest_domain,df_taxonomy):
        nearest_dict = self.fetch_nearest_domain_dict(self.json2dict())
        nearest_domain_dict = nearest_dict["nearest_domain_dict"]
        if sp_nearest_domain in set([x for nearest_domain_list in nearest_domain_dict.values() for x in nearest_domain_list]):
            org_accession = re.sub('_protein.json','',self.file_path.split('/')[-1])
            taxonomy = df_taxonomy.loc[org_accession,'taxonomy']
            print(f"{org_accession}\t{taxonomy}")
            return f"{org_accession}\t{taxonomy}"                     
        else:
            return ""

if __name__ == "__main__":
    current_dir = '/'.join(__file__.split('/')[:-1])
    json_path = f"{current_dir}/sample/GB_GCA_900539675.1_protein.json"
    jsonparser = JsonParser(json_path)
    dict_data = jsonparser.json2dict()
    taxonomy_df = taxonomy_tools.create_taxonomy_df()
    print(jsonparser.fetch_nearest_domain_dict())


 