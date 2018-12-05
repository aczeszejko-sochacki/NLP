import os
from typing import List, Dict
from .paths import DATA_DIR_PATH, BIGRAMS_PATH
from ..exceptions import NoContinuation


class Bigrams:
    """ A class representing predecessor: successors struct """

    def __init__(self, bigrams: Dict):
        self.bigrams = bigrams

    def get_predecessor_conts(self, predecessor: str) -> List:
        try:
            return self.bigrams[predecessor]
        except KeyError:
            raise NoContinuation


class SimpleBigrams:
    """
    A class representing a simple dict
    of pairs predecesor: successor
    """

    def __init__(self, bigrams: Dict):
        self.bigrams = bigrams

class BigramParser:
    """
    A class creating bigrams statistics
    basing on data/poleval_2grams.txt file
    """

    def __init__(self, poleval_filename: str):
        self.poleval_path = os.path.join(DATA_DIR_PATH, poleval_filename)
        self.bigrams = {}

    def update_bigram_struct(self, tokens: List, freq: int) -> None:
        """ Append the second token to the successors of the first """

        predecessor, successor = tokens

        if predecessor in self.bigrams:
            self.bigrams[predecessor].append((successor, freq))
        else:
            self.bigrams[predecessor] = [(successor, freq)]

    def create_bigrams_struct(self, k: int = 5) -> Bigrams:
        """ Read the file and create token-successors struct """

        with open(self.poleval_path) as poleval:
            for line in poleval:
                freq, *tokens = line.split()

                # Update only if freq meet the expectation
                if int(freq) > k:
                    self.update_bigram_struct(tokens, int(freq))

        return Bigrams(self.bigrams)

    def create_simple_bigrams_struct(self, k: int = 3) -> SimpleBigrams:
        """ Create {(token_1, token_2): freq, } struct """

        bigrams = {}

        with open(BIGRAMS_PATH) as poleval:
            for line in poleval:
                freq, predecesor, successor = line.split()

                # Update dict
                if int(freq) >= k:
                    bigrams[(predecesor, successor)] = freq

        return SimpleBigrams(bigrams)
