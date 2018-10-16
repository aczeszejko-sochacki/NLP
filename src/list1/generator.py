import random
from abc import ABC, abstractmethod
from parser import Parser
from typing import Dict


class Generator(ABC):
    """ Most abstract generator class """

    def generate_struct(self, filename: str) -> Dict:
        ngrams_struct = Parser()
        ngrams_struct.parse_poleval_file(filename)

        return ngrams_struct.tokens_successors

    def generate_sentence(self, filename: str, first_ngram: str) -> str:
        ngrams_struct = self.generate_struct(filename)

        # First ngram is either given by the user or drawn
        ngram = first_ngram or random.choice(bigrams_struct.keys())

        sentence = ''

        # Generate tokens while successor exists
        while ngram:
            ngram = self.generate_next_token(ngram)
            ' '.join((sentence, ngram))

    @abstractmethod
    def generate_next_token(self, predecessors: str) -> str:
        pass


class BiUniGenerator(BiGenerator):
    """
    A generator drawing successors uniformly
    basing on bigrams struct
    """

    def generate_next_token(self, predecessors: str) -> str:
        pass


class TriUniGenerator(TriGenerator):
    """
    A generator drawing successors uniformly
    basing on trigrams struct
    """

    def generate_next_token(self, predecessors: str) -> str:
        pass


class BiFreqGenerator(BiGenerator):
    """
    A generator drawing successors directly proportional
    to the number of the occurrences in bigrams struct
    """

    def generate_next_token(self, predecessors: str) -> str:
        pass


class TriFreqGenerator(Generator):
    """
    A generator drawing successors directly proportional
    to the number of the occurrences in trigrams struct
    """

    def generate_next_token(self, predecessors: str) -> str:
        pass
