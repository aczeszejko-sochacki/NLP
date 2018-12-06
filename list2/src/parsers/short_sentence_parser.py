from .paths import POLEVAL_SENTENCES_PATH
from typing import List


class ShortSentenceParser:
    """
    A class extracting short sentences
    from the task3_train file
    """

    def extract_sentences(self, threshold: int = 8) -> List:
        """
        Extract sentences not longer (according to the number
        of tokens) than the threshold
        """

        with open(POLEVAL_SENTENCES_PATH) as poleval:
            short_sentences = [sentence for sentence in poleval
                               if len(sentence.split()) <= threshold]

        return short_sentences
