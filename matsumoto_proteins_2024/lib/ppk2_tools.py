import os
import pandas as pd
from . import common
common.set_environment_variable()
from .cdhit_parser import CDHit_Parser

def create_class_set(class_file_path):
    with open(class_file_path) as class_file:
        class_list = []
        while True:
            line = class_file.readline()
            if not line:
                break
            else:
                class_list.append(line[:-1])
        return set(class_list)
    
def assign_class(class_rep_file_path,class_name):
    same_class_accession_list = []
    class_rep_list = list(create_class_set(class_rep_file_path))
    cdhit_parser = CDHit_Parser(os.environ["PPK2_rep_clstr"])
    ppk2_rep_dict = cdhit_parser.parse_one_file() 
    for rep_accession in class_rep_list:
        same_class_accession_list += ppk2_rep_dict[rep_accession]
    return {class_name:same_class_accession_list}

def create_class_dict():
    class1_dict = assign_class(os.environ["class1"] ,"class1")
    class2_dict = assign_class(os.environ["class2"] ,"class2")
    class3_dict = assign_class(os.environ["class3"] ,"class3")
    return {**class1_dict,**class2_dict,**class3_dict}


def create_ppk2_describe_df():
    describe_path = os.environ["Describe"]
    #header = ["gene_accession","org_accession","ppk2_class","aalength","pI"]
    df_ppk2_all = pd.read_table(describe_path) 
    #df_ppk2_all.columns = header
    df_ppk2_all.index = df_ppk2_all["gene_accession"]
    df_ppk2_all = df_ppk2_all.drop("gene_accession",axis=1)     
    return df_ppk2_all 

if __name__ == "__main__":
    # print(len(assign_class(os.environ["class1"] ,"class1")["class1"]))
    # print(len(assign_class(os.environ["class2"] ,"class2")["class2"]))
    # print(len(assign_class(os.environ["class3"] ,"class3")["class3"]))
    print(create_class_dict()["class3"])
