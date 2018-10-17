import numpy as np
from typing import Set


class ShuffleSentence:

    def __init__(self, basic_sentence: str):
        self.basic_sentence = basic_sentence

    def shuffle_sentence(self) -> str:
        """ Returns one shuffled examle of the sentence """

        # Need to copy basic sentence, because
        # shuffling alters it
        copy_sentence = self.basic_sentence

        tokens = np.array(copy_sentence.split())

        np.random.shuffle(tokens)

        new_sentence = ' '.join(list(tokens))

        return new_sentence

    def get_new_sentences(self, n_sentences: int = 3) -> Set:
        """ Returns n shuffled examples of the sentence """
        sentences = []

        for _ in range(n_sentences):
            sentences.append(self.shuffle_sentence())

        return set(sentences)
