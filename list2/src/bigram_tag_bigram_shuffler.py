import numpy as np
from .parsers.bigram_parser import SimpleBigrams
from .parsers.tag_bigram_parser import TagBigrams
from typing import List
from itertools import permutations
from .parsers.tag_parser import TaggedTokens
from .exceptions import TokenNotTagged
from operator import itemgetter


class BigramTagBigramShuffler:
    """
    A class shuffling sentence tokens and choosing
    the best permutation basing on bigrams
    and tag-bigrams
    """

    def get_all_sentence_permutations(self, sentence: str) -> List:

        # Sentence can be passed as a str or as splitted tokens
        if isinstance(sentence, str):
            sentence = sentence.split()

        perms = list(permutations(sentence))

        return perms

    def measure_perm_naturalness_bigrams(self, perm_bigrams: List,
                                         bigrams: SimpleBigrams) -> float:
        naturalness = 0.

        for bigram in perm_bigrams:

            # Shrink the values by tanh function
            bigram_freq = bigrams.bigrams.get(bigram, 0.)
            bigram_naturalness = np.tanh(float(bigram_freq))

            naturalness += bigram_naturalness

        return naturalness

    def measure_perm_naturalness_tag_bigrams(self, perm_bigrams: List,
                                             tag_bigrams: TagBigrams,
                                             tagged_tokens: TaggedTokens
                                            ) -> float:
        naturalness = 0.

        for bigram in perm_bigrams:

            # Need to get tags for tag_bigrams
            try:
                tag_1 = tagged_tokens.get_token_tag(bigram[0])
                tag_2 = tagged_tokens.get_token_tag(bigram[1])

                tags = (tag_1, tag_2)
            except TokenNotTagged:
                tags = None

            tag_bigram_freq = tag_bigrams.tag_bigrams.get(tags, 0.)
            tag_bigram_naturalness = np.tanh(float(tag_bigram_freq))

            naturalness += tag_bigram_naturalness

        return naturalness

    def get_the_best_perm_bigram(self, sentence: str,
                                 bigrams: SimpleBigrams) -> List:
        """
        The higher naturalness, the higher possition in the array
        (towards zero)
        """

        sentence_perms = self.get_all_sentence_permutations(sentence)

        perms_with_naturalness = []

        for sentence_perm in sentence_perms:

            # Need to extract bigrams from the perm
            predecesors = ['<BOS>'] + list(sentence_perm)
            successors = list(sentence_perm) + ['<EOS>']
            perm_bigrams = tuple(zip(predecesors, successors))

            perms_with_naturalness.append((
                sentence_perm,
                self.measure_perm_naturalness_bigrams(perm_bigrams,
                                                      bigrams)
            ))

        perms_with_naturalness.sort(key=itemgetter(1))

        # Concat the best sentence
        best_perm = (
            ' '.join(perms_with_naturalness[0][0]),
            perms_with_naturalness[0][1],
        )

        return best_perm

    def get_the_best_perm_tag_bigram(self, sentence: str,
                                     tag_bigrams: TagBigrams,
                                     tagged_tokens: TaggedTokens) -> List:
        """
        The higher naturalness, the higher possition in the array
        (towards zero)
        """

        sentence_perms = self.get_all_sentence_permutations(sentence)

        perms_with_naturalness = []

        for sentence_perm in sentence_perms:

            # Need to extract bigrams from the perm
            predecesors = ['<BOS>'] + list(sentence_perm)
            successors = list(sentence_perm) + ['<EOS>']
            perm_bigrams = tuple(zip(predecesors, successors))

            perms_with_naturalness.append((
                sentence_perm,
                self.measure_perm_naturalness_tag_bigrams(perm_bigrams,
                                                          tag_bigrams,
                                                          tagged_tokens)
            ))

        perms_with_naturalness.sort(key=itemgetter(1))

        # Concat the best sentence
        best_perm = (
            ' '.join(perms_with_naturalness[0][0]),
            perms_with_naturalness[0][1],
        )

        return best_perm
