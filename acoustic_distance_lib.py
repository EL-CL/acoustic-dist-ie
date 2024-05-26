import os
import joblib
from time import perf_counter
from tqdm import tqdm
from itertools import combinations
import multiprocessing as mp
import numpy as np
import pandas as pd
from scipy.io import wavfile
import spafe.features.bfcc
import spafe.features.cqcc
import spafe.features.gfcc
import spafe.features.lfcc
import spafe.features.lpc
import spafe.features.mfcc
import spafe.features.msrcc
import spafe.features.ngcc
import spafe.features.pncc
import spafe.features.psrcc
import spafe.features.rplp
import python_speech_features
from dtaidistance import dtw_ndim
from dtw import dtw

feature_funcs = {
    'BFCC': spafe.features.bfcc.bfcc,
    'CQCC': spafe.features.cqcc.cqcc,
    'GFCC': spafe.features.gfcc.gfcc,
    'IMFCC': spafe.features.mfcc.imfcc,
    'LFCC': spafe.features.lfcc.lfcc,
    'LPCC': spafe.features.lpc.lpcc,
    'MFCC': spafe.features.mfcc.mfcc,
    'MSRCC': spafe.features.msrcc.msrcc,
    'NGCC': spafe.features.ngcc.ngcc,
    'PNCC': spafe.features.pncc.pncc,
    'PSRCC': spafe.features.psrcc.psrcc,
    'RPLP': spafe.features.rplp.rplp,
    'logFBank': python_speech_features.logfbank,
}
feature_normalization_funcs = {
    'CMVN': lambda x: (x - np.mean(x, axis=0)) / np.std(x, axis=0),
    'CMN': lambda x: (x - np.mean(x, axis=0)),
    'MMVN': lambda x: (x - np.mean(x)) / np.std(x),
    'MMN': lambda x: (x - np.mean(x)),
    'none': lambda x: x,
}
# Use hamming window, same as in Praat
hamming_window = spafe.utils.preprocessing.SlidingWindow(
    0.015, 0.005, 'hamming')

dtw_funcs = {
    # Dependent DTW. https://doi.org/10.1007/s10618-016-0455-0
    'DTW-D': lambda x, y: dtw_ndim.distance_fast(x, y, use_pruning=False),
    # Open-end DTW. https://doi.org/10.1016/j.artmed.2008.11.007
    'DTW-OE': lambda x, y: dtw(x, y, distance_only=True).distance,
}
distance_normalization_funcs = {
    'by-sum': lambda x, len_1, len_2: x / (len_1 + len_2),
    'by-max': lambda x, len_1, len_2: x / max(len_1, len_2),
    'none': lambda x, len_1, len_2: x,
}


def extract_feature(feature_name, audio, rate, normalization):
    # Arguments are from Spafe’s example, except for `window` and `normalize`
    kwargs = {
        'sig': audio, 'fs': rate,
        'pre_emph': 1, 'pre_emph_coeff': 0.97,
        'window': hamming_window,
        'nfilts': 128, 'nfft': 2048,
        'low_freq': 0, 'high_freq': rate / 2,
        'normalize': None,  # Normalization will be done later
    }
    if feature_name == 'CQCC':
        kwargs.pop('nfilts')
    elif feature_name == 'LPCC':
        for k in ('nfilts', 'nfft', 'low_freq', 'high_freq'):
            kwargs.pop(k)
    elif feature_name == 'logFBank':
        kwargs = {
            'signal': audio, 'samplerate': rate,
            'winlen': 0.015, 'winstep': 0.005,
            'nfilt': 128, 'nfft': 2048,
            'lowfreq': 0, 'highfreq': rate / 2,
            'preemph': 0.97,
        }
    feature = feature_funcs[feature_name](**kwargs)
    return feature_normalization_funcs[normalization](feature)


def calculate_distance(feature_1, feature_2, dtw_method, normalization):
    distance = dtw_funcs[dtw_method](feature_1, feature_2)
    return distance_normalization_funcs[normalization](distance, feature_1.shape[0], feature_2.shape[0])


# distances: {language_pair: distance}
def distances2matrix(distances, languages):
    matrix = pd.DataFrame(None, columns=languages, index=languages)
    for pair, distance in distances.items():
        matrix.at[pair[0], pair[1]] = distance
        matrix.at[pair[1], pair[0]] = distance
    for language in languages:
        matrix.at[language, language] = 0
    return matrix


def process_word(languages_folder, languages, audio_filename,
                 language_pairs, all_audios, rate,
                 feature_name, feature_normalization, dtw_method, distance_normalization):
    features = {}
    for language in languages:
        audio = all_audios[(languages_folder, language, audio_filename)]
        features[language] = extract_feature(
            feature_name, audio, rate, feature_normalization)
    distances = {}
    for pair in language_pairs:
        distances[pair] = calculate_distance(
            features[pair[0]], features[pair[1]], dtw_method, distance_normalization)
    return distances


def process_queued_words(input_queue, output_queues,
                         languages, language_pairs, all_audios, rate,
                         feature_name, feature_normalization, dtw_method, distance_normalization):
    while True:
        item = input_queue.get()
        if item is None:  # Poison pill to stop the process
            input_queue.task_done()
            break
        languages_folder, audio_filename = item
        distances = process_word(languages_folder, languages, audio_filename,
                                 language_pairs, all_audios, rate,
                                 feature_name, feature_normalization, dtw_method, distance_normalization)
        for pair, distance in distances.items():
            output_queues[pair].put(distance)
        input_queue.task_done()
        print(audio_filename, 'in', languages_folder, 'done')


def process_all_words(languages_folders, languages, audio_filenames,
                      result_folder, process_count, skip_existing,
                      all_audios, rate,
                      feature_name, feature_normalization, dtw_method, distance_normalization):
    language_pairs = [pair for pair in list(combinations(languages, 2))
                      if pair[0] != pair[1]]
    result_filename = '_'.join(
        (dtw_method, distance_normalization, feature_normalization, feature_name)) + '.csv'
    result_path = os.path.join(result_folder, result_filename)
    if skip_existing and os.path.exists(result_path):
        print('Skip existing', result_path)
        return

    # https://docs.python.org/3/library/multiprocessing.html
    # https://www.geeksforgeeks.org/python-multiprocessing-queue-vs-multiprocessing-manager-queue/
    # https://superfastpython.com/multiprocessing-joinablequeue-on-python/
    start_time = perf_counter()
    print('Start processing', result_path)
    with mp.Manager() as manager:
        input_queue = manager.JoinableQueue()
        for audio_filename in audio_filenames:
            for languages_folder in languages_folders:
                input_queue.put((languages_folder, audio_filename))
        print('Item count:', input_queue.qsize())
        for _ in range(process_count):
            # Poison pill to stop each process
            input_queue.put(None)

        output_queues = {pair: manager.Queue() for pair in language_pairs}
        processes = []
        for _ in range(process_count):
            p = mp.Process(
                target=process_queued_words,
                args=(input_queue, output_queues,
                      languages, language_pairs, all_audios, rate,
                      feature_name, feature_normalization, dtw_method, distance_normalization))
            p.start()
            processes.append(p)

        # Wait for all processes to complete
        all_exited = False
        while all_exited and input_queue.empty():
            all_exited = True
            for p in processes:
                if p.exitcode is None:
                    all_exited = False
                    break
        # Close the queue
        input_queue.join()
        # Close the processes
        for p in processes:
            p.join()
        print('Calculation completed. Time',
              perf_counter() - start_time, 's')

        distances = {}
        for pair in language_pairs:
            results = []
            while not output_queues[pair].empty():
                results.append(output_queues[pair].get())
            distances[pair] = np.mean(results)
        matrix = distances2matrix(distances, languages)
        matrix.to_csv(result_path)
        print('Save completed. Time',
              perf_counter() - start_time, 's')


def read_all_audios(languages_folders, languages, audio_filenames, joblib_filename='audios.joblib'):
    if os.path.exists(joblib_filename):
        return joblib.load(joblib_filename)

    audios = {}
    for audio_filename in tqdm(audio_filenames):
        for languages_folder in languages_folders:
            for language in languages:
                rate, audio = wavfile.read(os.path.join(
                    languages_folder, language, audio_filename))
                audios[(languages_folder, language, audio_filename)] = audio
    joblib.dump((audios, rate), joblib_filename)
    return audios, rate
