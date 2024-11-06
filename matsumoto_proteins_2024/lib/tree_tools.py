import pandas as pd
from . import common
from ete3 import PhyloTree
common.set_environment_variable()

def add_nodename(tree_path,import_format):
    tree=PhyloTree(tree_path,format=import_format)
    internal_node = 0
    for node in tree.traverse("preorder"):
        if node.name == '':
            internal_node += 1
            node.name = f"n{str(internal_node)}"
    return tree