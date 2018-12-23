from typing import Tuple
from itertools import product
import numpy as np
 
 
class TokenParser:
    """
    A class implementing operations
    on a single tokens
    """
 
    pl_uncertain_letters = ('a', 'o', 'e', 'z', 's', 'c')
    sign_possible_alts= {
        'a': ('a', 'ą'),
        'e': ('e', 'ę'),
        'o': ('o', 'ó'),
        'z': ('z', 'ź', 'ż'),
        's': ('s', 'ś'),
        'c': ('c', 'ć'),
     }
 
    def extract_pl_uncertain_letters(self, token: str) -> Tuple:
        """
        Return (letter, index of letter) pairs
        for all uncertain letter in the token
        """
 
        uncertain_letters = [(ind, letter) for ind, letter in enumerate(token)
                             if letter in self.pl_uncertain_letters]
 
        return uncertain_letters
 
    def gen_poss_rev_tokens(self, token: str) -> Tuple:
        """
        Generate all possible variations of the token
        with replaced (or not) uncertain letters
        """
 
        if set(self.pl_uncertain_letters).intersection(set(token)):
 
            # Get uncertain letters and their offsets
            inds, letters = tuple(zip(*self.extract_pl_uncertain_letters(token)))
 
            letter_sets = [self.sign_possible_alts[letter] for letter in letters]
 
            revised_letters_all = tuple(product(*letter_sets))
 
            # Delete uncertain letters
            revised_token_core = list(token)
            np.delete(revised_token_core, inds).tolist()
 
            revised_tokens = []
 
            for alt_letters in revised_letters_all:
                core = np.array(revised_token_core)
 
                np.put(core, inds, alt_letters)
 
                revised_tokens.append(''.join(core))
 
            return revised_tokens
 
        else:
            # There is no uncertain letter
            return [token]
            