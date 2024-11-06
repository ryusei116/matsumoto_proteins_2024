import sys
from .hmmdomtab_genome_parser import HmmDomtabParser

class HmmDomtabPPK2Parser(HmmDomtabParser):
    def __init__(self,file_path,target_domain_name="PPK2",fetch_neighborhood_gene_number_oneside=0):
        super().__init__(file_path,target_domain_name,fetch_neighborhood_gene_number_oneside)     

if __name__ == "__main__":
    current_dir = '/'.join(__file__.split('/')[:-1])
    test_sample ={
        'Class2':f"{current_dir}/sample/GB_GCA_900539675.1_protein.faa",
    }
    hmmdomtab = HmmDomtabPPK2Parser(test_sample[sys.argv[1]])
    print(hmmdomtab.output_fasta_seq(domain=True))




