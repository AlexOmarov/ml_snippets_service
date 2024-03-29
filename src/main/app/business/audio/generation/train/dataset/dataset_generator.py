import os
import pickle

import numpy as np

from business.audio.generation.train.dataset.dto.audio_entry import AudioEntry


def get_dataset_generator(serialized_units_dir_path: str, init_batch: list):
    batches_amount = len(os.listdir(serialized_units_dir_path))
    while True:
        if batches_amount <= init_batch[0]:
            init_batch[0] = 4
        filename = f"/serialized_batch_{init_batch[0]}.pkl"
        with open(serialized_units_dir_path + filename, 'rb') as file:
            units: [AudioEntry] = pickle.load(file)
        batch_features = [_normalize(unit.feature_vector) for unit in units]
        batch_identification_vectors = [unit.speaker_identification_vector for unit in units]
        init_batch[0] = init_batch[0] + 1
        yield np.array(batch_features), np.array(batch_identification_vectors)


def _normalize(array):
    min_value = 0
    max_value = 100
    return ((array - (-1000)) / (1000 - (-1000))) * (max_value - min_value) + min_value

