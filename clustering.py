import os
from tqdm import tqdm
from clustering_lib import read_matrix, cluster

input_folder = 'acoustic_distances'
output_path = 'trees/newicks.tsv'

filenames = [filename for filename in os.listdir(input_folder)
             if filename.endswith('.csv')]
methods = {
    'Single': 'single',
    'Complete': 'complete',
    'UPGMA': 'average',
    'WPGMA': 'weighted',
    'UPGMC': 'centroid',
    'WPGMC': 'median',
    'Ward': 'ward',
    'NJ': 'nj',
}
results = []
results.append(['DTW', 'DistanceNormalization', 'FeatureNormalization',
                'Clustering', 'Feature', 'Newick'])
for filename in tqdm(filenames):
    input_path = os.path.join(input_folder, filename)
    matrix, languages = read_matrix(input_path)
    for method in methods:
        params = filename.removesuffix('.csv').split('_')
        newick = cluster(matrix, languages, methods[method])
        line = params[:-1] + [method, params[-1], newick]
        results.append(line)
with open(output_path, 'w') as f:
    for line in results:
        f.write('\t'.join(line) + '\n')
