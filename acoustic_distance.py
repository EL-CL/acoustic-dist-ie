import os
from multiprocessing import cpu_count
from acoustic_distance_lib import read_all_audios, process_all_words
from acoustic_distance_lib import feature_funcs, feature_normalization_funcs, dtw_funcs, distance_normalization_funcs
from audio_metadata import *

if __name__ == '__main__':
    languages_folders = [
        '../acoustic-dist-ie-audio/female',
        '../acoustic-dist-ie-audio/male',
    ]
    process_count = cpu_count() // 2
    # When there is insufficient memory (including RuntimeError ‘can't start new thread’),
    # reduce the process count, e.g.:
    # process_count = 4
    print('CPU count:', cpu_count())
    print('Process count:', process_count)

    all_audios, rate = read_all_audios(languages_folders, languages, audio_filenames)
    result_folder = 'acoustic_distances'
    os.makedirs(result_folder, exist_ok=True)

    # Parameters needed for calculation
    params = []

    def add_params(feature_names, feature_normalizations, dtw_methods, distance_normalizations):
        for feature_name in feature_names:
            for feature_normalization in feature_normalizations:
                for dtw_method in dtw_methods:
                    for distance_normalization in distance_normalizations:
                        param = (feature_name, feature_normalization, dtw_method, distance_normalization)
                        if param not in params:
                            params.append(param)

    # Plese comment out the params you do not want to extract
    # To compare selected features
    selected_features = ['CQCC', 'LFCC', 'MFCC', 'NGCC', 'PNCC', 'logFBank']
    add_params(selected_features, ['CMN'], ['DTW-D'], ['by-sum', 'none'])
    # To compare feature normalization
    add_params(feature_funcs, feature_normalization_funcs, ['DTW-D'], ['by-sum'])
    # To compare DTW methods
    add_params(feature_funcs, ['CMN'], dtw_funcs, ['by-sum'])
    # To compare distance normalization
    add_params(feature_funcs, ['CMN'], ['DTW-D'], distance_normalization_funcs)
    # Add all
    add_params(feature_funcs, feature_normalization_funcs, dtw_funcs, distance_normalization_funcs)
    for i, param in enumerate(params):
        print(f'[{i + 1}/{len(params)}]')
        process_all_words(languages_folders, languages, audio_filenames,
                          result_folder, process_count, True,
                          all_audios, rate, *param)
