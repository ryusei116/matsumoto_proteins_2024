# matsumoto_proteins_2024
This repository contains the  source code associated with the study "Distribution of Polyphosphate Kinase 2 Genes in Bacteria Underscores a Dynamic Evolutionary History," which investigates the distribution and evolutionary history of Polyphosphate Kinase 2 (PPK2) genes across various bacterial species.

This source code has been tested on Ubuntu 22.04.3 LTS.

## Git clone and virtual environment setup
```
$ git clone git@github.com:ryusei116/matsumoto_proteins_2024.git
$ cd matsumoto_proteins_2024
$ pyenv install 3.11.9
$ pyenv local 3.11.9
$ python -m venv venv
$ source venv/bin/activate
(venv)$ pip install ./matsumoto_proteins_2024/
```
## Downloading analysis data and required external files
```
$ mkdir data
$ cd data
$ wget https://data.gtdb.ecogenomic.org/releases/release207/207.0/genomic_files_reps/gtdb_proteins_aa_reps_r207.tar.gz
$ wget https://data.gtdb.ecogenomic.org/releases/release207/207.0/bac120_taxonomy_r207.tsv.gz
$ tar -zxvf gtdb_proteins_aa_reps_r207.tar.gz
$ gunzip bac120_taxonomy_r207.tsv.gz
```
The data stored in Zenodo (`DOI 10.5281/zenodo.14047164`) should also be included in the same directory. Additionally, modify `matsumoto_proteins_2024/matsumoto_proteins_2024/lib/common.py` so that the `workspace_path` is set to the absolute path where this repository is located (e.g., `"<arbitrary path>/matsumoto_proteins_2024"`).

##  Installing dependent libraries.
```
$  pip install ./matsumoto_proteins_2024/
```
Install the modules in `/matsumoto_proteins_2024/matsumoto_proteins_2024/lib` and the libraries listed in `requirements.txt`.

## Module test
```
$ python
>>> import lib.ppk2_tools
>>>
```
If `lib.ppk2_tools` can be successfully imported, the environment has been set up correctly.
