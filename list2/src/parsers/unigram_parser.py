import os
from typing import List, Dict
from .paths import DATA_DIR_PATH


class Unigrams:
    """ A class representing token: freq struct """

    def __init__(self, unigrams: Dict):
        self.unigrams = unigrams


class UnigramParser:
    """
    A class creating unigrams statistics
    basing on data/poleval_2grams.txt file
    """

    def __init__(self, poleval_filename: str):
        self.poleval_path = os.path.join(DATA_DIR_PATH, poleval_filename)
        self.unigrams = {}

    def update_unigram_freq_of_tag(self, tokens: List, freq: int) -> None:
        """ Update unigram freqs of the given tokens """

        for token in tokens:
            if token in self.unigrams:
                self.unigrams[token] += freq
            else:
                self.unigrams[token] = freq

    def create_unigrams_struct(self) -> Unigrams:
        """ Read the file and create token-freq struct """

        with open(self.poleval_path) as poleval:
            for line in poleval:
                freq, *tokens = line.split()

                self.update_unigram_freq_of_tag(tokens, int(freq))

        return Unigrams(self.unigrams)
