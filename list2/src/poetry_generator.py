from .tag_generator import TagGeneratorBi
from .parsers.sentence_parser import SentenceParser
from .parsers.tag_parser import TagParser, TaggedTokens, TagSets
from typing import Tuple, List
from .exceptions import NoRhyme, NoContinuation, TagDoesNotExist
from .parsers.unigram_parser import Unigrams
from .parsers.bigram_parser import Bigrams


class PoetryGenerator(TagGeneratorBi):
    """ Generate poem-like couples of sentences """

    def __init__(self):
        super().__init__()
        self.sentence_parser = SentenceParser()

    def generate_rhyme(self, token_1: str, token_2: str,
                       tagged_tokens: TaggedTokens, unigrams: Unigrams,
                       tag_sets: TagSets, n_syllables_1: int = None,
                       n_syllables_2: int = None) -> Tuple:
        """ Try to generate a rhyme """

        tag_1, source_1 = tagged_tokens.get_sentence_tags(token_1)[0]
        tag_2, source_2 = tagged_tokens.get_sentence_tags(token_2)[0]

        try:
            new_token_1 = \
                self.rand_token_tag_unigrams(tag_1, unigrams, tag_sets,
                                             n_syllables=n_syllables_1)

            rhyme = self.token_parser.get_token_end_for_a_rhyme(new_token_1)

            new_token_2 = \
                self.rand_token_tag_unigrams(tag_2, unigrams, tag_sets,
                                             n_syllables=n_syllables_2,
                                             suffix=rhyme,
                                             skip=new_token_1)
        except (TagDoesNotExist, NoContinuation):
            raise NoRhyme

        return (new_token_1, source_1), (new_token_2, source_2)

    def generate_rhymed_sentences(self, sentence_1: str,
                                  sentence_2: str,
                                  tagged_tokens: TaggedTokens,
                                  unigrams: Unigrams,
                                  bigrams: Bigrams,
                                  tag_sets: TagSets,
                                  continuations: int = 1):
        """
        Generate two verses poetry-style
        """

        # Required data
        syl_stats_1 = self.sentence_parser.get_sentence_syll_stats(sentence_1)
        syl_stats_2 = self.sentence_parser.get_sentence_syll_stats(sentence_2)
        sent_1_tokens = self.sentence_parser.delete_interpunction(sentence_1)
        sent_2_tokens = self.sentence_parser.delete_interpunction(sentence_2)
        new_sent_1 = []
        new_sent_2 = []
        new_sent_1_meta = []
        new_sent_2_meta = []

        # Split the data to proper pieces
        syl_1_begin, syl_1_end = syl_stats_1[:-1], syl_stats_1[-1]

        syl_2_begin, syl_2_end = syl_stats_2[:-1], syl_stats_2[-1]

        sent_1_begin, sent_1_rhyme = \
            ' '.join(sent_1_tokens[:-1]), sent_1_tokens[-1]

        sent_2_begin, sent_2_rhyme = \
            ' '.join(sent_2_tokens[:-1]), sent_2_tokens[-1]

        # Generate new sentences from all but two tags
        new_sent_1_begin , new_sent_1_begin_meta = \
            self.gen_sent_coresponding_tags(sent_1_begin, tagged_tokens,
                                            unigrams, bigrams, tag_sets,
                                            syl_stats=syl_1_begin)

        new_sent_2_begin, new_sent_2_begin_meta = \
            self.gen_sent_coresponding_tags(sent_2_begin, tagged_tokens,
                                            unigrams, bigrams, tag_sets,
                                            syl_stats=syl_2_begin)

        # Try to generate a rhyme
        for _ in range(100):
            try:
                rhyme = self.generate_rhyme(sent_1_rhyme, sent_2_rhyme,
                                            tagged_tokens, unigrams, tag_sets,
                                            n_syllables_1=syl_1_end,
                                            n_syllables_2=syl_2_end)

                new_sent_1_rhyme, new_sent_1_rhyme_meta = rhyme[0]
                new_sent_2_rhyme, new_sent_2_rhyme_meta = rhyme[1]
                # If success, break
                break
            except NoRhyme:
                # If not, we try to draw three times
                # If no success three times, return the old rhyme
                new_sent_1_rhyme, new_sent_1_rhyme_meta = \
                    sent_1_rhyme, 'not_replaced'
                new_sent_2_rhyme, new_sent_2_rhyme_meta = \
                    sent_2_rhyme, 'not_replaced'

        sentences = new_sent_1_begin + [new_sent_1_rhyme] + ['\n'] + \
                    new_sent_2_begin + [new_sent_2_rhyme]

        sentences_meta = new_sent_1_begin_meta + [new_sent_1_rhyme_meta] + \
                         ['\n'] + new_sent_2_begin_meta + \
                         [new_sent_2_rhyme_meta]

        # Format output
        sentences = ' '.join(sentences).capitalize()
        sentences_meta = ' '.join(sentences_meta)

        return sentences, sentences_meta

    def generate_frag_of_poetry(self, frag: str, tagged_tokens: TaggedTokens,
                                unigrams: Unigrams, bigrams: Bigrams,
                                tag_sets: TagSets, continuations: int = 1):
        """
        Apply generate_rhymed_sentences to a consistent part
        of a real poetry, like Pan Tadeusz book
        """

        # Create list of double verses
        frag_sent = frag.splitlines()
        frag_sent_even, frag_sent_odd = frag_sent[0::2], frag_sent[1::2]
        double_verses = list(zip(frag_sent_even, frag_sent_odd))

        new_verses = \
            [self.generate_rhymed_sentences(*verses, tagged_tokens,
                                            unigrams, bigrams, tag_sets,
                                            continuations=continuations)
             for verses in double_verses]

        # Format output
        text, meta = list(zip(*new_verses))

        text, meta = '\n'.join(text), '\n'.join(meta)

        return text, meta
