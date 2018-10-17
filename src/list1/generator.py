import numpy as np
import random
from abc import ABC, abstractmethod
from parser import Parser
from typing import Dict


class Generator(ABC):
    """ Abstract generator class """

    def __init__(self, filename: str, k: int):
        self.ngrams_struct = self.generate_struct(filename, k)

    def generate_struct(self, filename: str, k: int = 2) -> Dict:
        ngrams_struct = Parser()
        ngrams_struct.parse_poleval_file(filename, k=k)

        return ngrams_struct.tokens_successors

    def generate_sentence(self, first_ngram: str = None) -> str:

        # First ngram is either given by the user or drawn
        ngram = first_ngram or random.choice(list(self.ngrams_struct))

        sentence = ngram

        # Generate tokens while any successor exists
        while True:
            next_token = self.generate_next_token(ngram)
            if not next_token:
                return sentence

            sentence = ' '.join((sentence, next_token))

            ngram = ' '.join(ngram.split()[1:] + [next_token])

    @abstractmethod
    def generate_next_token(self, predecessors: str) -> str:
        pass


class BiUniGenerator(Generator):
    """
    A generator drawing successors uniformly
    basing on bigrams struct
    """

    def __init__(self, filename: str = 'poleval_2grams.txt', k: int = 2):
        super().__init__(filename, k=k)

    def generate_next_token(self, predecessors: str) -> str:

        # Check if predecesscors are in struct and have any successor
        if predecessors in self.ngrams_struct and \
            self.ngrams_struct[predecessors]:
            return np.random.choice(self.ngrams_struct[predecessors])[0]
        else:
            return None


class TriUniGenerator(Generator):
    """
    A generator drawing successors uniformly
    basing on trigrams struct
    """

    def __init__(self, filename: str = 'poleval_3grams.txt', k: int = 2):
        super().__init__(filename, k=k)

    def generate_next_token(self, predecessors: str) -> str:

        # Check if predecesscors are in struct and have any successor
        if predecessors in self.ngrams_struct and \
            self.ngrams_struct[predecessors]:

            # Draw successor using random distribution
            return np.random.choice(self.ngrams_struct[predecessors])[0]
        else:
            return None


class BiFreqGenerator(Generator):
    """
    A generator drawing successors directly proportional
    to the number of the occurrences in bigrams struct
    """

    def __init__(self, filename: str = 'poleval_2grams.txt', k: int = 2):
        super().__init__(filename, k=k)

    def generate_next_token(self, predecessors: str) -> str:

        # Check if predecesscors are in struct and have any successor
        if predecessors in self.ngrams_struct and \
            self.ngrams_struct[predecessors]:

            # Draw successor with chance of ... directly proportional
            # to the number of the occurencces
            values, freqs = list(zip(*self.ngrams_struct[predecessors]))

            # Cast to int
            freqs = [int(freq) for freq in freqs]
            all_freqs = sum(freqs)
            probs = [freq / all_freqs for freq in freqs]

            return np.random.choice(values, p=probs)
        else:
            return None


class TriFreqGenerator(Generator):
    """
    A generator drawing successors directly proportional
    to the number of the occurrences in trigrams struct
    """

    def __init__(self, filename: str = 'poleval_3grams.txt', k: int = 2):
        super().__init__(filename, k=k)

    def generate_next_token(self, predecessors: str) -> str:

        # Check if predecesscors are in struct and have any successor
        if predecessors in self.ngrams_struct and \
            self.ngrams_struct[predecessors]:

            # Draw successor with chance of ... directly proportional
            # to the number of the occurencces
            values, freqs = list(zip(*self.ngrams_struct[predecessors]))

            # Cast to int
            freqs = [int(freq) for freq in freqs]
            all_freqs = sum(freqs)
            probs = [freq / all_freqs for freq in freqs]

            return np.random.choice(values, p=probs)
        else:
            return None
