import os
from typing import Dict
 
 
class Bigrams:
    """ A class representing pairs predecesor: successor """
 
    def __init__(self, bigrams: Dict):
        self.bigrams = bigrams
 
class BigramParser:
    """
    A class creating bigrams statistics
    basing on data/poleval_2grams.txt file
    """
 
    DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '..', '..', 'data', 'poleval_2grams.txt')
 
    def create_bigrams_struct(self, k: int = 3) -> Bigrams:
        """ Create {(token_1, token_2): freq, } struct """
 
        bigrams = {}
 
        with open(self.DATA_PATH) as poleval:
            for line in poleval:
                freq, predecesor, successor = line.split()
 
                # Update bigrams
                if int(freq) >= k:
                    bigrams[(predecesor, successor)] = int(freq)
 
        return Bigrams(bigrams)
        