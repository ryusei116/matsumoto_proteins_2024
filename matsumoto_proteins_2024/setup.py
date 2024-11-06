from setuptools import setup, find_packages
 
setup(
    name='lib',   
    version="0.0.1",
    description="Distribution of Polyphosphate Kinase 2 Genes in Bacteria Underscores a Dynamic Evolutionary History",
    long_description="",
    author='ryusei_matsumoto@elsi.jp',
    license='MIT',
    packages=find_packages(),
    install_requires=open('requirements.txt').read().splitlines(),
)