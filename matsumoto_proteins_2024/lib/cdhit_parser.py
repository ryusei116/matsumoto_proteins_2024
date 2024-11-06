import linecache
import re

class CDHit_Parser():
    def __init__(self,file_path):
        self.file_path = file_path
    
    def parse_one_file(self):
        cluster_dict = {}
        idx = 1
        with open(self.file_path) as read_file:
            while True:
                line = read_file.readline()
                if not line:
                    break
                elif line[0] == '>':
                    cluster_rep,cluster_list = self.parse_one_cluster(idx)
                    cluster_dict[cluster_rep] = cluster_list
                idx += 1
        return cluster_dict

    def parse_one_cluster(self,idx):
        cluster_idx = idx + 1
        cluster_list =[]
        cluster_rep = ''
        while True:
            target_line = linecache.getline(self.file_path, cluster_idx)
            if not target_line:
                return cluster_rep,cluster_list
            elif target_line[0] == '>':
                return cluster_rep,cluster_list
            accession_filed,rep_filed =target_line.split("...")
            if re.sub("\s","",rep_filed) == "*":
                cluster_rep = accession_filed.split('>')[1]
            cluster_list.append(accession_filed.split('>')[1])
            cluster_idx += 1
    
if __name__ == "__main__":
    cdhit_parser = CDHit_Parser('./sample/ppk2_domain_c70_sample.clstr')
    print(cdhit_parser.parse_one_file())
    