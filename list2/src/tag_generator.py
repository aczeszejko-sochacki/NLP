import numpy as np
from .parsers.tag_parser import TagParser, TaggedTokens, TagSets
from typing import List, Tuple, Dict
from .exceptions import TokenNotTagged, NoContinuation, TagDoesNotExist
from .parsers.token_parser import TokenParser
from .parsers.unigram_parser import Unigrams
from .parsers.bigram_parser import Bigrams


class TagGenerator:
    """
    A class inherited by the generators basing on
    tags and ngrams
    """

    def __init__(self):
        self.token_parser = TokenParser()

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

    def rand_token_tag_unigrams(self, tag: str, unigrams: Unigrams,
                                tag_sets: TagSets,
                                n_syllables: int = None,
                                suffix: str = None,
                                skip: str = None) -> str:
        """
        Return drawn token from the list
        satisfying the schema (token, freq).
        Probs directly proportional to the freqs
        """

        unigrams = unigrams.unigrams
        tag_tokens = tag_sets.get_tag_tokens(tag)

        freq_tag_tokens = [(token, unigrams[token])
                           for token in tag_tokens if token in unigrams]

        # Optional: filter possible conts by #syl
        if n_syllables is not None:
            freq_tag_tokens = [(token, freq) for token, freq in freq_tag_tokens
                               if self.token_parser.count_syllables(token) == \
                               n_syllables]

        # Optional: filter possible conts by a suffix
        if suffix is not None:
            freq_tag_tokens = [(token, freq) for token, freq in
                               freq_tag_tokens
                               if token.endswith(suffix)]

        # Optional: exclude trivial rhymes
        if skip is not None and skip in freq_tag_tokens:
            freq_tag_tokens.remove(skip)

        rand_token = self.rand_by_freqs(freq_tag_tokens)
        return rand_token

    def rand_token_tag_bigrams(self, tag: str, predecessor: str,
                               bigrams: Bigrams, tag_sets: TagSets,
                               continuations: int,
                               n_syllables: int = None) -> str:
        """
        Return drawn token from the intersection
        of the set of similarly tagged tokens
        and predecessor's successors (bigrams stats)
        """

        tag_tokens = tag_sets.get_tag_tokens(tag)

        conts_with_freqs = bigrams.get_predecessor_conts(predecessor)

        bigrams = bigrams.bigrams

        conts_correct_tag = [(token, freq) for token, freq in
                             conts_with_freqs if token in tag_tokens]

        conts_with_further_cont = [(token, freq) for token, freq in
                                   conts_correct_tag if token in bigrams
                                   if len(bigrams[token]) >= continuations]

        # Optional: filter possible conts by #syl
        if n_syllables is not None:
            conts_with_further_cont = [(token, freq) for token, freq
                                       in conts_with_further_cont if
                                       self.token_parser.count_syllables(token)
                                       == n_syllables]

        rand_token = self.rand_by_freqs(conts_with_further_cont)
        return rand_token


class TagGeneratorUni(TagGenerator):
    """
    A class generating sentences basing on tags and unigrams
    """

    def gen_sent_coresponding_tags(self, sentence: str,
                                   tagged_tokens: TaggedTokens,
                                   unigrams: Unigrams,
                                   tag_sets: TagSets,
                                   syl_stats: List = None) -> Tuple:
        """
        Generate sentence with tokens having the same tags
        as the given sentence (maintaining the same order).
        """

        sentence_tokens = sentence.split()
        sentence_tags = tagged_tokens.get_sentence_tags(sentence)
        new_sentence = []
        new_sentence_meta = []
        syl_stats = syl_stats or [None] * len(sentence_tokens)

        for index, (tag, source) in enumerate(sentence_tags):
            n_syl = syl_stats[index]

            try:
                new_token = self.rand_token_tag_unigrams(tag, unigrams,
                                                         tag_sets,
                                                         n_syllables=n_syl)

                new_sentence.append(new_token)
                new_sentence_meta.append(source)

            except (TagDoesNotExist, NoContinuation):
                new_sentence.append(sentence_tokens[index])
                new_sentence_meta.append('not_replaced')

        return new_sentence, new_sentence_meta


class TagGeneratorBi(TagGenerator):
    """
    A class generating sentences basing on tags and bigrams
    """

    def gen_sent_coresponding_tags(self, sentence: str,
                                   tagged_tokens: TaggedTokens,
                                   unigrams: Unigrams,
                                   bigrams: Bigrams,
                                   tag_sets: TagSets,
                                   continuations: int = 1,
                                   syl_stats: List = None) -> Tuple:
        """
        Generate sentence with tokens having the same tags
        as the given sentence (maintaining the same order).
        Draw the tokens using bigram stats
        """

        sentence_tokens = sentence.split()
        sentence_tags = tagged_tokens.get_sentence_tags(sentence)
        new_sentence = []
        new_sentence_meta = []
        syl_stats = syl_stats or [None] * len(sentence_tokens)

        # First token can be drawn from the unigrams
        first_tag, first_source = sentence_tags.pop(0)
        first_n_syl = syl_stats.pop(0)
        try:
            new_token = self.rand_token_tag_unigrams(first_tag, unigrams,
                                                     tag_sets,
                                                     n_syllables=first_n_syl)

            new_sentence.append(new_token)
            new_sentence_meta.append(first_source)

        except (TagDoesNotExist, NoContinuation):
            new_sentence.append(sentence_tokens.pop(0))
            new_sentence_meta.append('not_replaced')

        # The rest should be drawn - if possible - using bigrams stats
        for index, (tag, source) in enumerate(sentence_tags):
            predecessor = new_sentence[-1]
            n_syl = syl_stats[index]

            try:
                new_token = self.rand_token_tag_bigrams(tag, predecessor,
                                                        bigrams, tag_sets,
                                                        continuations,
                                                        n_syllables=n_syl)

                new_sentence.append(new_token)
                new_sentence_meta.append(source)
            except TagDoesNotExist:
                new_sentence.append(sentence_tokens[index])
                new_sentence_meta.append('not_replaced')

            except NoContinuation:
                new_sentence_meta.append('|')

                try:
                    new_token = self.rand_token_tag_unigrams(tag, unigrams,
                                                             tag_sets,
                                                             n_syllables=n_syl)

                    new_sentence.append(new_token)
                    new_sentence_meta.append(source)

                except (TagDoesNotExist, NoContinuation):
                    new_sentence.append(sentence_tokens[index])
                    new_sentence_meta.append('not_replaced')

        return new_sentence, new_sentence_meta
