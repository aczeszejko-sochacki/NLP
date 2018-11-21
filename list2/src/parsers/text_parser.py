import os
import re
from typing import Dict
from .paths import DANE_POZYTYWISTYCZNE_DIR_PATH
from .unigram_parser import Unigrams


class TextParser:
    """
    A class parsing text to extract
    sort of useful data
    """

    def update_unigrams(self, unigrams: Dict, token) -> Dict:
        """
        Add a new token to unigrams
        or update freq of an existing one
        """

        # Remove not alphanumeric chars
        token = re.sub(r'\W+', '', token)

        if token in unigrams:
            unigrams[token] += 1
        else:
            unigrams[token] = 1

        # Remove not valid tokens
        unigrams.pop('', unigrams)

        return unigrams

    def parse_text_file(self, filename: str, text_name=None) -> Dict:
        """ Create unigrams struct basing on the text """

        unigrams = {}
        filename_path = os.path.join(DANE_POZYTYWISTYCZNE_DIR_PATH,
                                     filename)

        with open(filename_path) as text:
            for line in text:
                for token in line.split():
                    unigrams = self.update_unigrams(unigrams, token)

        return Unigrams(unigrams, name=text_name)

    def count_mark(self, filename: str, mark: str) -> int:
        """ Count freq of sign in a given file """

        filename_path = os.path.join(DANE_POZYTYWISTYCZNE_DIR_PATH,
                                     filename)

        counter = 1

        with open(filename_path) as text:
            for line in text:
                for char in line:
                    if char == mark:
                        counter += 1

        return counter
