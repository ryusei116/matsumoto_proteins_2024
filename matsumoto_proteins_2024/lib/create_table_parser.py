import re
import sys
import os
from Bio.SeqUtils.IsoelectricPoint import IsoelectricPoint as IP
from . import common
common.set_environment_variable()
from .json_parser import JsonParser
from . import taxonomy_tools as taxonomy_tools
from . import fasta_tools as fasta_tools
 
class CreateTableParser(JsonParser):
    def create_table(self,seq_df,taxonomy_df):
        self.adjacent_dict = self.json2dict()
        self.query_domain = self.adjacent_dict["query_domain"]
        del self.adjacent_dict['query_domain']
        if self.adjacent_dict == {}:
            pass
        else:
            for accession in self.adjacent_dict.keys():
                yield(self.prepare_one_record(accession,seq_df,taxonomy_df))
    
    def count_orf_number(self):
        orf_number = 0
        host_org_accession = re.sub('_protein.json','',self.file_path.split('/')[-1])
        faa_filename = f"{host_org_accession}_protein.faa"
        with open(f"{os.environ['GTDBDirPath']}/{faa_filename}") as read_file:
            while True:
                line = read_file.readline()
                if not line:                     
                    break
                elif line[0] == '>':
                    orf_number += 1
        return orf_number
    
    def prepare_one_record(self,accession,seq_df,taxonomy_df):
        one_record = {}
        org_accession = re.sub('_protein.json','',self.file_path.split('/')[-1])
        target_gene_dict = self.adjacent_dict[accession]['n0']
        try:
            sequence = seq_df.at[accession,'sequence']
            protein = IP(sequence)
            pI = protein.pi()
            length = len(sequence)
        except KeyError as e:
            print('catch KeyError',e)
            sequence = None
            pI = None
            length = None
        except AttributeError as e:
            print('catch AttributeError. do not set seq_df',e)
            sequence = None
            pI = None
            length = None
            
        one_record['gene_accession'] = accession
        one_record['org_accession'] = org_accession
        one_record['gene_position_id'] = target_gene_dict['gene_position_id']
        one_record['query_domain'] = self.query_domain
        one_record['gene_annotation_by_domain'] = target_gene_dict['domain_annotation']
        one_record['gene_length'] = length
        one_record['pI'] = pI
        one_record['sequence'] = sequence
        one_record['taxonomy'] = taxonomy_df.at[org_accession,'taxonomy']
        # one_record['orf_number'] = self.count_orf_number()
        return one_record

if __name__ == "__main__":
    current_dir = '/'.join(__file__.split('/')[:-1])
    test_sample = {
        "SinglePPK2":f"{current_dir}/sample/GB_GCA_900539675.1_protein.json",
    }
    create_table_parser = CreateTableParser(test_sample[sys.argv[1]])
    df_taxonomy = taxonomy_tools.create_taxonomy_df()
    df_fasta = fasta_tools.create_df_fasta(f"{current_dir}/../../data/ppk2_gene_all.fasta")
    print(create_table_parser.create_table(df_fasta,df_taxonomy).__next__())