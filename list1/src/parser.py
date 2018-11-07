import os
from typing import Dict, List


class Parser:

    """
    Reads the input from poleval files
    and finds all possible successors
    of first word of each line in the file
    """

    def __init__(self, filename: str):
        self._tokens_successors = dict()
        self.filename = filename

    @property
    def get_ngrams_file_path(self) -> str:
        """ Path to the file with ngrams data """

        ngrams_path = os.path.join(os.path.dirname(
                                       os.path.abspath(__file__)
                                   ),
                                   '..', 'data', self.filename)

        return ngrams_path

    @property
    def tokens_successors(self) -> Dict:
        """ Get token successors """

        return self._tokens_successors

    def tokens_successors_append(self, tokens: List[str], k: int = 2) -> None:
        """ Handle next row of the file """

        # Split line of tokens and frequency for furter processing
        frequency, predecessors, successor = \
            tokens[0], ' '.join(tokens[1:-1]), tokens[-1]

        # Handle new tokens
        if int(frequency) >= k:
            if predecessors in self.tokens_successors:
                self.tokens_successors[predecessors].append((successor,
                                                             frequency))
            else:
                self.tokens_successors[predecessors] = [(successor,
                                                         frequency)]

    def parse_poleval_file(self, k: int = 2) -> Dict:
        """ Create predecessors-successors structure """

        with open(self.get_ngrams_file_path) as poleval:

            # Tokenize each line
            for line in poleval:
                self.tokens_successors_append(line.split(), k=k)
