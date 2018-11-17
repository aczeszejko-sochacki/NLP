from .token_parser import TokenParser
from typing import Tuple, List


class SentenceParser:
    """ A class implementing operations on sentences """

    def __init__(self):
        self.token_parser = TokenParser()

    def get_sentence_syll_stats(self, sentence: str) -> List:
        """ Return tuple of token's sylls stats """

        syll_stats = [self.token_parser.count_syllables(token)
                      for token in sentence.split()]

        return syll_stats

    def delete_interpunction(self, sentence: str) -> List:

        int_marks = ('.', '?', '!', ',', '...', ':')
        # deleted_interpunction = []

        deleted_interpunction = [token[:-1] if token.endswith(int_marks)
                                 else token for token in sentence.split()]

        return deleted_interpunction
