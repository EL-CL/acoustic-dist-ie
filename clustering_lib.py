import io
import numpy as np
import pandas as pd
from scipy.cluster import hierarchy
from scipy.spatial.distance import squareform
from Bio import Phylo
from Bio.Phylo.TreeConstruction import _DistanceMatrix, DistanceTreeConstructor

constructor = DistanceTreeConstructor()


def read_matrix(file_path):
    df = pd.read_csv(file_path)
    matrix, languages = df.iloc[:, 1:].values.tolist(), df.iloc[:, 0].tolist()
    return matrix, languages


def node2newick(node, parent_dist, leaf_names, newick=''):
    # https://stackoverflow.com/a/31878514
    if node.is_leaf():
        return '%s:%f%s' % (leaf_names[node.id], parent_dist - node.dist, newick)
    else:
        if len(newick) > 0:
            newick = '):%f%s' % (parent_dist - node.dist, newick)
        else:
            newick = ');'
        newick = node2newick(
            node.get_left(), node.dist, leaf_names, newick=newick)
        newick = node2newick(
            node.get_right(), node.dist, leaf_names, newick=',%s' % (newick))
        newick = '(%s' % (newick)
        return newick


def cluster(matrix, languages, method):
    if method == 'nj':
        triangle = [[matrix[i][j] if i >= j else matrix[j][i]
                    for j in range(i + 1)] for i in range(len(matrix))]
        distance_matrix = _DistanceMatrix(languages, triangle)
        tree = constructor.nj(distance_matrix)
        string = io.StringIO()
        Phylo.write(tree, string, 'newick')
        return string.getvalue().replace('\n', '')
    condensed = squareform(np.array(matrix))
    z = hierarchy.linkage(condensed, method)
    root_node = hierarchy.to_tree(z)
    newick = node2newick(root_node, root_node.dist, languages)
    return newick.replace('\n', '')
