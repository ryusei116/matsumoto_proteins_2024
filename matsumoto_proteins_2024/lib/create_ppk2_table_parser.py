import sys
from . import common
common.set_environment_variable()
from .create_table_parser import CreateTableParser
from . import taxonomy_tools as taxonomy_tools
from . import fasta_tools as fasta_tools
from . import ppk2_tools as ppk2_tools

class CreatePPK2TableParser(CreateTableParser):
    
    def __init__(self,file_path):
        self.file_path = file_path
        self.gene_distance_th = 500
        self.finished_target_accession_keys = []
        self.dict_data = self.json2dict()

    def prepare_one_record(self,accession,seq_df,taxonomy_df):  
        one_record = super().prepare_one_record(accession,seq_df,taxonomy_df)
        class_dict = ppk2_tools.create_class_dict()
        if accession in set(class_dict['class1']):
            one_record['ppk2_class'] = 1
        elif accession in set(class_dict['class2']):
            one_record['ppk2_class'] = 2
        elif accession in set(class_dict['class3']):
            one_record['ppk2_class'] = 3

        nearest_dict = self.fetch_nearest_domain(accession,"domain_annotation")
        if ('PPK2' in nearest_dict) or ('PPK2/PPK2' in nearest_dict):
            one_record['ppk2_duplicate'] = 1
        else:
            one_record['ppk2_duplicate'] = 0
        return one_record
    
if __name__ == "__main__":
    current_dir = '/'.join(__file__.split('/')[:-1])
    test_sample = {
        "SinglePPK2":f"{current_dir}/sample/GB_GCA_900539675.1_protein.json",
    }
    create_table_parser = CreatePPK2TableParser(test_sample[sys.argv[1]])
    df_taxonomy = taxonomy_tools.create_taxonomy_df()
    df_fasta = fasta_tools.create_df_fasta(f"{current_dir}/../../data/ppk2_gene_all.fasta")
    print(create_table_parser.create_table(df_fasta,df_taxonomy).__next__())
