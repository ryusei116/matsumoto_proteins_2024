import pandas as pd
from . import common
from Bio import SeqIO
common.set_environment_variable()

def create_df_fasta(file_path):
    fasta_list = []
    for record in SeqIO.parse(file_path, 'fasta'):
        accession = record.id
        sequence = str(record.seq)
        fasta_list.append({'accession':accession,'sequence':sequence})
    df_fasta = pd.DataFrame(fasta_list)
    df_fasta.index = df_fasta['accession']
    df_fasta = df_fasta.drop('accession',axis = 1)
    return df_fasta