import re
from typing import List


class TokenParser:
    """ A class implementing operations on tokens """

    def find_vowel_occurrences(self, token: str) -> List:
        """
        Return list of indices of the vowels
        occurrences in the token ('i' + another vowel
        treated as one vowel)
        """

        vowels_but_i = 'aeouąęóy'
        vowels = vowels_but_i + 'i'

        patterns = [
            'i[{0}]'.format(vowels_but_i),  # double vowels, e.g. '..ia..'
            '[{0}]'.format(vowels)          # single vowels
        ]

        double_vowel_occurrences = [(match.start(), match.group())
                                    for match in re.finditer(patterns[0],
                                                             token,
                                                             re.IGNORECASE)]

        # Replace double vowels containing i by something neutral
        # to avoid double matches
        token = re.sub('i[{0}]'.format(vowels_but_i), '__', token)

        # IGNORECASE is really important here
        single_vowel_occurrences = [(match.start(), match.group())
                                    for match in re.finditer(patterns[1],
                                                             token,
                                                             re.IGNORECASE)]

        vowels_dict = {
            'double': double_vowel_occurrences,
            'single': single_vowel_occurrences,
        }

        return vowels_dict

    def count_syllables(self, token: str) -> int:
        """ Return number of token syllables """

        vowel_occurrences = self.find_vowel_occurrences(token)

        n_syllables = len(sum(vowel_occurrences.values(), []))

        return n_syllables

    def get_token_end_for_a_rhyme(self, token: str) -> str:
        """ Return the last syllable + prepending vowel """

        vowel_occurrences = self.find_vowel_occurrences(token)

        all_vowels_occ = sum(vowel_occurrences.values(), [])
        all_vowels_occ.sort()

        try:
            index_lbnl_vowel, _ = all_vowels_occ[-2]

            return token[index_lbnl_vowel:]
        except IndexError:
            # One syllable token
            return token
