from typing import List, Tuple
from .parsers.unigram_parser import Unigrams
from .parsers.bigram_parser import Bigrams
from .parsers.token_parser import TokenParser
import numpy as np


class ViterbiRevTextPred:

    def compute_delta(self, tokens: List, probs: List, unigrams: Unigrams,
                      bigrams: Bigrams, act_token: str) -> Tuple:

        new_delta_cands = []

        for ind, rev_token in enumerate(tokens):
            rev_prob = np.log(unigrams.get(act_token, 0) + 0.0001) +\
                       np.log(bigrams.get((rev_token, act_token), 0) +\
                              0.0001) + probs[ind]

            new_delta_cands.append((rev_prob, ind))

        # Return a new delta and its predecesor
        return max(new_delta_cands)

    def gen_poss_sent(self, sent_tokens: List, token_parser: TokenParser,
                      with_cap: bool = False) -> List:
        """ Create space of possible sentences """

        all_pos_rev = list(map(token_parser.gen_poss_rev_tokens,
                               sent_tokens))

        # Generate tokens with cap letters too
        if with_cap:
            all_pos_rev_copy = all_pos_rev.copy()

            for ind, revs in enumerate(all_pos_rev_copy):
                all_pos_rev[ind].extend(
                    list(map(lambda x: x.capitalize(), revs)))

        return all_pos_rev

    def reconstruct_sent(self, all_pos_rev: List, predecesors: List,
                         last_token: int, with_cap: bool = False) -> str:
        """
        Visit all the predecesor of the last token
        to reconstruct the path
        """

        tokens = []
        for token_ind in range(len(all_pos_rev)-1, -1, -1):
            tokens.append(all_pos_rev[token_ind][last_token])

            last_token = predecesors[token_ind][last_token]

        tokens.reverse()
        return ' '.join(tokens)

    def predict(self, sent_tokens: List, unigrams: Unigrams,
                bigrams: Bigrams, token_parser: TokenParser,
                with_cap: bool = False) -> List:

        all_pos_rev = self.gen_poss_sent(sent_tokens, token_parser)

        probs, predecesors = [[]], [[]]

        # Fill the first possible tokens with unigram stats
        # and the first predecesors to respect the dims
        for token in all_pos_rev[0]:
            probs[0].append(np.log(unigrams.get(token, 0) + 0.0001))
            predecesors[0].append('whatever')

        # Fill the rest with the Viterbi algorithm
        for tokens_ind, tokens in enumerate(all_pos_rev[1:]):
            probs.append([])
            predecesors.append([])

            for token in tokens:

                new_prob, new_pred =\
                    self.compute_delta(all_pos_rev[tokens_ind], probs[-2],
                                       unigrams, bigrams, token)

                probs[-1].append(new_prob)
                predecesors[-1].append(new_pred)

        # Choose the best path
        last_token = np.argmax(probs[-1])

        # Visit all the predecesors in the best path                
        final_sent = self.reconstruct_sent(all_pos_rev, predecesors,
                                           last_token, with_cap)

        return final_sent
