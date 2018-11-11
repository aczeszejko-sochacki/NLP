import numpy as np
from .parsers.tag_parser import TagParser, TaggedTokens, TagSets
from typing import List, Tuple, Dict
from .exceptions import TokenNotTagged, NoContinuation, TagDoesNotExist


class TagGenerator:
    """
    A class inherited by the generators basing on
    tags and ngrams
    """

    def rand_by_freqs(self, tokens_with_freqs: List) -> str:
        """
        Return random token drawn with probs
        directly proportional to the freqs
        """

        # Can draw continuation only from unempty list
        if not tokens_with_freqs:
            raise NoContinuation

        tokens, freqs = list(zip(*tokens_with_freqs))

        # Need to normalize freqs to get probs
        all_freq = sum(freqs)
        probs = [freq / all_freq for freq in freqs]

        rand_token = np.random.choice(tokens, p=probs)

        return rand_token

    def rand_token_tag_unigrams(self, tag: str, unigrams: Dict,
                                tag_sets: TagSets) -> str:
        """
        Return drawn token from the list
        satisfying the schema (token, freq).
        Probs directly proportional to the freqs
        """

        tag_tokens = tag_sets.get_tag_tokens(tag)

        freq_tag_tokens = [(token, unigrams[token])
                           for token in tag_tokens if token in unigrams]

        rand_token = self.rand_by_freqs(freq_tag_tokens)
        return rand_token

    def rand_token_tag_bigrams(self, tag: str, predecessor: str,
                               bigrams: Dict, tag_sets: TagSets,
                               continuations: int) -> str:
        """
        Return drawn token from the intersection
        of the set of similarly tagged tokens
        and predecessor's successors (bigrams stats)
        """

        tag_tokens = tag_sets.get_tag_tokens(tag)

        continuations_with_freqs = bigrams[predecessor]

        continuations_correct_tag = [(token, freq) for token, freq in
                                     continuations_with_freqs
                                     if token in tag_tokens]

        continuations_with_further_continuation = [(token, freq)
                                                   for token, freq in
                                                   continuations_correct_tag
                                                   if token in bigrams
                                                   if len(bigrams[token])
                                                   >= continuations]

        rand_token = self.rand_by_freqs(continuations_correct_tag)
        return rand_token


class TagGeneratorUni(TagGenerator):
    """
    A class generating sentences basing on tags and unigrams
    """

    def generate_sentence_coresponding_tags(self, sentence: str,
                                            tagged_tokens: TaggedTokens,
                                            unigrams: Dict,
                                            tag_sets: TagSets) -> str:
        """
        Generate sentence with tokens having the same tags
        as the given sentence (maintaining the same order)
        """

        sentence_tags = tagged_tokens.get_sentence_tags(sentence)
        new_sentence = []

        for tag in sentence_tags:
            try:
                new_sentence.append(self.rand_token_tag_unigrams(tag,
                                                                 unigrams,
                                                                 tag_sets))
            except (TagDoesNotExist, NoContinuation):
                new_sentence.append('?')     # TODO

        return ' '.join(new_sentence).capitalize()


class TagGeneratorBi(TagGenerator):
    """
    A class generating sentences basing on tags and bigrams
    """

    def generate_sentence_coresponding_tags(self, sentence: str,
                                            tagged_tokens: TaggedTokens,
                                            unigrams: Dict,
                                            bigrams: Dict,
                                            tag_sets: TagSets,
                                            continuations: int = 1) -> str:
        """
        Generate sentence with tokens having the same tags
        as the given sentence (maintaining the same order).
        Draw the tokens using bigram stats
        """

        sentence_tags = tagged_tokens.get_sentence_tags(sentence)
        new_sentence = []

        # First token can be drawn from the unigrams
        first_token = sentence_tags.pop(0)
        try:
            new_sentence.append(self.rand_token_tag_unigrams(first_token,
                                                             unigrams,
                                                             tag_sets))
        except (TagDoesNotExist, NoContinuation):
            new_sentence.append('?')

        # The rest should be drawn - if possible - using bigrams stats
        for tag in sentence_tags:
            predecessor = new_sentence[-1]

            try:
                new_sentence.append(self.rand_token_tag_bigrams(tag,
                                                                predecessor,
                                                                bigrams,
                                                                tag_sets,
                                                                continuations))
            except TagDoesNotExist:
                new_sentence.append('?')
            except NoContinuation:
                new_sentence.append(' | ')

                try:
                    new_sentence.append(self.rand_token_tag_unigrams(tag,
                                                                     unigrams,
                                                                     tag_sets))
                except TagDoesNotExist:
                    new_sentence.append('dupa')     # TODO

        return ' '.join(new_sentence).capitalize()
