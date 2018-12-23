import os
from typing import Dict
 
 
class Unigrams:
    """ A class representing token: freq struct """
 
    def __init__(self, unigrams: Dict):
        self.unigrams = unigrams
 
 
class UnigramParser:
    """
    A class creating unigrams statistics
    basing on data/poleval_2grams.txt file
    """
 
    DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '..', '..', 'data', 'poleval_2grams.txt')
 
    def create_unigrams_struct(self, k: int = 3) -> Unigrams:
        """ Read the file and create token-freq struct """
 
        unigrams = {}
 
        with open(self.DATA_PATH) as poleval:
            for line in poleval:
                freq, *tokens = line.split()
 
                if int(freq) >= k:
                    # Update unigrams
                    for token in tokens:
                        if token in unigrams:
                            unigrams[token] += int(freq)
                        else:
                            unigrams[token] = int(freq)
 
        return Unigrams(unigrams)