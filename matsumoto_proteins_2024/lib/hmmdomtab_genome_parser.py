from Bio import SearchIO
from Bio import SeqIO
import re
import os
import sys
import json
sys.path.append('../')
from . import common
 
class HmmDomtabParser():
    def __init__(self,file_path,target_domain_name,fetch_neighborhood_gene_number_oneside):
        common.set_environment_variable()
        self.file_path = file_path
        self.ie_value = 10**(-10)
        self.hmm_coverage_th = 0.75
        self.target_domain_name = target_domain_name
        self.fetch_neighborhood_gene_number_oneside = fetch_neighborhood_gene_number_oneside
    
    #1. sequence gathering, 2. center gene of neighborhood genes cluster
    def fetch_target_gene(self):
        #description example↓
        # 1684 # 2100 # 1 # ID=169_3;partial=00;start_type=ATG;rbs_motif=GGA/GAG/AGG;rbs_spacer=5-10bp;gc_cont=0.609
        target_gene_dict = {}
        qresults=SearchIO.parse(self.file_path, 'hmmsearch3-domtab')
        for qresult in qresults:
            domain_name = qresult.id
            if domain_name == self.target_domain_name: #not require
                for hit in qresult:
                    env_coordinates = []
                    for hsp in hit:
                        for hsp_flag in hsp:
                            hmm_coverage = (hsp_flag.query_end - hsp_flag.query_start + 1)/qresult.seq_len
                            if (float(hsp.evalue) < self.ie_value) and (hmm_coverage > self.hmm_coverage_th):
                                description = hit.description.split("#")
                                gene_start = int(re.sub(' ','',description[1]))
                                gene_end = int(re.sub(' ','',description[2]))
                                sequence_direction = int(re.sub(' ','',description[3]))
                                gene_position_id = re.sub(" |ID=","",description[4].split(";")[0])
                                gene_accession = hit.id
                                env_coordinates.append((hsp.env_start,hsp.env_end))
                                target_gene_dict[gene_accession]={'target_sequence_direction':sequence_direction,'target_gene_position_id':gene_position_id,'target_gene_start':gene_start,'target_gene_end':gene_end,'env_coordinates':env_coordinates}
        return target_gene_dict

    def fetch_target_seq(self,domain=False,target_gene_dict=False):
        seq_dict = {}
        proteome_path = f"{os.environ['GTDBDirPath']}/{re.sub('txt','faa',self.file_path.split('/')[-1])}"
        if target_gene_dict == False:
            target_gene_dict = self.fetch_target_gene()
        else:
            target_gene_dict = target_gene_dict
        for record in SeqIO.parse(proteome_path, 'fasta'):
            id_part = record.id
            desc_part = record.description
            seq = record.seq
            if id_part in set(target_gene_dict.keys()) and domain ==True:
                env_coordinates = target_gene_dict[id_part]['env_coordinates']
                env_idx = 1
                for env_coordinate in env_coordinates:
                    seq_dict[f"{id_part}_{env_idx}"] = {"sequence":seq[env_coordinate[0]:env_coordinate[1]],"description":desc_part}
                    env_idx += 1
            elif id_part in set(target_gene_dict.keys()):
                seq_dict[id_part] = {"sequence":seq,"description":desc_part}
        return seq_dict

    def output_fasta_seq(self,domain=False):
        seq_dict = self.fetch_target_seq(domain)
        if seq_dict == {}:
            pass
        else:
            fasta_seq = ""
            for key in seq_dict:
                fasta_seq += f">{key}\n{seq_dict[key]['sequence']}\n"
            return fasta_seq
    
    #1. fetch neighborhood gene 
    def fetch_neighborhood_gene(self,target_gene_detail_dict):
        #search on same contigfile
        neighborhood_gene_dict = {f"n{i}" : {} for i in range(-self.fetch_neighborhood_gene_number_oneside,self.fetch_neighborhood_gene_number_oneside+1)}
        qresults=SearchIO.parse(self.file_path, 'hmmsearch3-domtab')
        for qresult in qresults:
            domain_name = qresult.id
            for hit in qresult:
                description = hit.description.split("#")
                gene_start = int(re.sub(' ','',description[1]))
                gene_end = int(re.sub(' ','',description[2]))
                sequence_direction = int(re.sub(' ','',description[3]))
                gene_position_id = re.sub(" |ID=","",description[4].split(";")[0])
                gene_accession = hit.id
                gene_distance = 0

                if target_gene_detail_dict['target_gene_position_id'].split('_')[0] == gene_position_id.split('_')[0]:
                    neighborhood_idx = (int(gene_position_id.split('_')[1]) - int(target_gene_detail_dict['target_gene_position_id'].split('_')[1]))
                    if abs(neighborhood_idx) <= self.fetch_neighborhood_gene_number_oneside and sequence_direction == target_gene_detail_dict['target_sequence_direction']:
                        if neighborhood_gene_dict[f"n{neighborhood_idx}"] == {}:
                            domain_annotation = "Unknown"
                            if neighborhood_idx < 0:
                                gene_distance = target_gene_detail_dict['target_gene_start'] - gene_end
                            elif neighborhood_idx > 0:
                                gene_distance = gene_start - target_gene_detail_dict['target_gene_end']
                            neighborhood_gene_dict[f"n{neighborhood_idx}"] = {'gene_accession':gene_accession,'domain_annotation':domain_annotation,'sequence_direction':sequence_direction,'gene_position_id':gene_position_id,'gene_start':gene_start,'gene_end':gene_end,'gene_distance':gene_distance}
                        #domain annotation
                        for hsp in hit:
                            for hsp_flag in hsp:
                                hmm_coverage = (hsp_flag.query_end - hsp_flag.query_start + 1)/qresult.seq_len
                                if (float(hsp.evalue) < self.ie_value) and (hmm_coverage > self.hmm_coverage_th):
                                    if neighborhood_gene_dict[f"n{neighborhood_idx}"]["domain_annotation"] == "Unknown":
                                        neighborhood_gene_dict[f"n{neighborhood_idx}"]["domain_annotation"] = domain_name 
                                    else:
                                        domain_annotation = neighborhood_gene_dict[f"n{neighborhood_idx}"]["domain_annotation"] + f"/{domain_name}"
                                        neighborhood_gene_dict[f"n{neighborhood_idx}"]["domain_annotation"] = domain_annotation
        return neighborhood_gene_dict
  
    def search_neighborhood_gene(self,target_gene_dict):
        print(self.target_domain_name)
        target_neighborhood_gene_dict = {'query_domain':self.target_domain_name}
        if target_gene_dict == {}:
            return target_neighborhood_gene_dict
        target_gene_accession_list = list(target_gene_dict.keys())
        for target_gene_accession in target_gene_accession_list:
            target_gene_detail_dict = target_gene_dict[target_gene_accession]
            target_neighborhood_gene_dict[target_gene_accession] = self.fetch_neighborhood_gene(target_gene_detail_dict)
        return target_neighborhood_gene_dict
   
    def dict2json(self,dict,output_dir):
        with open(output_dir, mode="wt", encoding="utf-8") as f:
            json.dump(dict, f, ensure_ascii=False, indent=2)
 
 
   
if __name__ == "__main__":
    current_dir = '/'.join(__file__.split('/')[:-1])
    output_dir = f"{current_dir}/sample/GB_GCA_900539675.1_protein.json"
    test_sample ={
        'Class2':f"{current_dir}/sample/GB_GCA_900539675.1_protein.faa",
    }
    hmmdomtab = HmmDomtabParser(test_sample[sys.argv[1]],"PPK2",5)
    ppk2_dict = hmmdomtab.fetch_target_gene()
    hmmdomtab.dict2json(hmmdomtab.search_neighborhood_gene(ppk2_dict),output_dir)
 

    