import os
from itertools import repeat
from more_itertools import zip_offset
from typing import List
from shuffle_sentence import ShuffleSentence
from operator import itemgetter


class MeasureNaturalness:
    def __init__(self, ngram_length: int, filename: str):
        self.filename = filename
        self.ngram_length = ngram_length

    @property
    def get_ngrams_file_path(self) -> str:
        """ Path to the file with ngrams data """

        ngrams_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                              '..', '..', 'data',
                                              self.filename)

        return ngrams_path

    def get_consistent_ngrams(self, sentence: str) -> List:
        """
        Get all n-elem consistent combinations of the tokens
        """

        # Tokens to zip
        tokens = list(repeat(sentence.split(), self.ngram_length))

        # All consistent ngrams
        ngrams = list(zip_offset(*tokens,
                      offsets=tuple(range(self.ngram_length))))

        ngrams_strings = [' '.join(ngram) for ngram in ngrams]

        return ngrams_strings

    def measure_sum_freq(self, sentence: str) -> int:
        """
        Calculate sum of frequencies of each consistent
        ngram in the sentence
        """

        sum_of_freq = 0
        sentence_ngrams = self.get_consistent_ngrams(sentence)

        with open(self.get_ngrams_file_path) as f:
            for line in f:
                freq, ngram = int(line.split()[0]), ' '.join(line.split()[1:])

                for sentence_ngram in sentence_ngrams:
                    if sentence_ngram == ngram:
                        sum_of_freq += freq

        return sum_of_freq

    def index_sentence_permutations(self, sentence: str,
                                    n_permutations: int = 3) -> List:

         shuffler = ShuffleSentence(sentence)

         sentences = shuffler.get_new_sentences(n_sentences=n_permutations)

         sentences_with_freq = [(sentence, self.measure_sum_freq(sentence))
                                for sentence in sentences]

         # Sort by freq desc
         sentences_with_freq.sort(key=itemgetter(1), reverse=True)

         return sentences_with_freq
