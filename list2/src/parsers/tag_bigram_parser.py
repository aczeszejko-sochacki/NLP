import os
from .paths import BIGRAMS_PATH
from .tag_parser import TaggedTokens
from typing import Dict
from ..exceptions import TokenNotTagged


class TagBigrams:

    def __init__(self, tag_bigrams: Dict):
        self.tag_bigrams = tag_bigrams


class TagBigramParser:
    """ Create tag bigrams struct """

    def create_tag_bigrams_dict(self, tagged_tokens: TaggedTokens,
                                k: int = 3) -> Dict:
        """ Create {(tag_1, tag_2): freq, } struct """

        tag_bigrams = {}

        with open(BIGRAMS_PATH) as poleval:
            for line in poleval:
                freq, predecesor, successor = line.split()

                # Get token tags
                try:
                    new_tag_bigram = (
                        tagged_tokens.get_token_tag(predecesor),
                        tagged_tokens.get_token_tag(successor)
                    )

                    # Update dict
                    if int(freq) >= k:
                        if new_tag_bigram in tag_bigrams:
                            tag_bigrams[new_tag_bigram] += int(freq)
                        else:
                            tag_bigrams[new_tag_bigram] = int(freq)

                except TokenNotTagged:
                    pass

        return TagBigrams(tag_bigrams)
