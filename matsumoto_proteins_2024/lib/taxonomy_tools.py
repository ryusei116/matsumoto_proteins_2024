import sys
sys.path.append('../')
import os
import pandas as pd
from . import common
common.set_environment_variable()

def create_taxonomy_df(taxonomy_path = os.environ["TaxonomyPath"]):
    df_taxonomy = pd.read_table(taxonomy_path,header = None)
    df_taxonomy.columns = ['org_accession','taxonomy']
    df_taxonomy.index = df_taxonomy['org_accession']
    df_taxonomy = df_taxonomy.drop('org_accession',axis = 1)
    return df_taxonomy

def create_bac_gtdb_accession_list():
    with open(f"{os.environ['workspace_path']}/data/bac_gtdb_accession.txt") as read_file:
        return [line.strip("\n") for line in read_file.readlines()]

def create_arc_gtdb_accession_list():
    with open(f"{os.environ['workspace_path']}/data/arc_gtdb_accession.txt") as read_file:
        return [line.strip("\n") for line in read_file.readlines()]
