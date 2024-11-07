import datetime
import os

def set_environment_variable():
    os.environ['workspace_path'] = "/home/ryusei/research/ppk2_bioinfo_paper/matsumoto_proteins_2024"
    os.environ["GTDBDirPath"] = "/mnt/d/Research_backup_240714/GTDB/protein_faa_reps/bacteria"
    os.environ["TaxonomyPath"] = "/mnt/d/Research_backup_240714/GTDB/bac120_taxonomy.tsv"
    os.environ["Describe"] = f"{os.environ['workspace_path']}/data/ppk2_bacteria_table.tsv"
    os.environ["class3"] = f"{os.environ['workspace_path']}/data/ppk2_classification/ppk2_classIII_rep.txt"
    os.environ["class2"] = f"{os.environ['workspace_path']}/data/ppk2_classification/ppk2_classII_rep.txt"
    os.environ["class1"] = f"{os.environ['workspace_path']}/data/ppk2_classification/ppk2_classI_rep.txt"
    os.environ["PPK2_rep_clstr"] = f"{os.environ['workspace_path']}/data/ppk2_classification/ppk2_gene_c70.fasta.clstr"

def create_todays_dir():
    today = "{0:%Y%m%d}".format(datetime.date.today())
    new_dir_path = f"{os.environ['OutputDirPath']}{today}"
    os.makedirs(new_dir_path, exist_ok=True)
    return new_dir_path
