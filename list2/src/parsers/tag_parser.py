import os
from operator import itemgetter
from typing import Dict, List, Type
from ..exceptions import (TokenNotTagged, TagDoesNotExist,
                          CannotPredictTokenTag)
from .paths import SUPERTAGS_PATH


class TaggedTokens:
    """ A class representing tag: token pairs """

    def __init__(self, tagged_tokens: Dict):
        self.tagged_tokens = tagged_tokens

    def get_token_tag(self, token: str) -> str:
        try:
            return self.tagged_tokens[token]
        except KeyError:
            raise TokenNotTagged

    def get_predicted_token_tag(self, token: str) -> str:
        """
        If the token is not tagged, try to make a prediction
        based on the tokens with the same suffix of length 3
        """

        token_suffix = token[-3:]

        token_possible_tags = {}

        # Find possible tags
        for token in self.tagged_tokens:
            if token.endswith(token_suffix):
                if self.tagged_tokens[token] in token_possible_tags:

                    # Vote for this tag
                    token_possible_tags[self.tagged_tokens[token]] += 1
                else:

                    # Add a tag to possibilities
                    token_possible_tags[self.tagged_tokens[token]] = 1

        # Return the most frequent one
        predicted_tag = max(token_possible_tags.items(),
                            key=itemgetter(1))[0]

        return predicted_tag

    def get_sentence_tags(self, sentence: str) -> str:
        sentence_tags = []

        # The first capital letter is (with a high probability)
        # a result of beginning the sentence
        sentence = sentence[0].lower() + sentence[1:]

        for token in sentence.split():
            try:
                token_tag = self.get_token_tag(token)

                sentence_tags.append((token_tag, 'tagged'))
            except TokenNotTagged:
                try:
                    token_tag = self.get_predicted_token_tag(token)

                    sentence_tags.append((token_tag, 'predicted'))
                except CannotPredictTokenTag:

                    # Hope it will not be raised anytime
                    sentence_tags.append((None, None))

        return sentence_tags


class TagSets:
    """ A class representing pairs tag: tokens """

    def __init__(self, tag_sets: Dict):
        self.tag_sets = tag_sets

    def get_tag_tokens(self, tag: str) -> List:
        try:
            return self.tag_sets[tag]
        except KeyError:
            raise TagDoesNotExist


class TagParser:
    """
    A class creating helpful structures of
    the tags from the data/supertags.txt file
    """

    def __init__(self):
        self.tagged_tokens = {}
        self.tag_sets = {}

    def create_tag_token_pairs(self) -> Type[TaggedTokens]:
        """ Store the content of supertags file in a dict """

        with open(SUPERTAGS_PATH) as supertags:
            for line in supertags:
                token, tag = line.split()

                self.tagged_tokens[token] = tag

        return TaggedTokens(self.tagged_tokens)

    def assign_token_to_tag(self, token: str,  tag: str) -> None:
        """ Append list of the tag representants"""

        if tag in self.tag_sets:
            self.tag_sets[tag].append(token)
        else:
            self.tag_sets[tag] = [token]

    def create_tags_struct(self) -> Type[TagSets]:
        """ Read the file and create tag-representants structure """

        with open(SUPERTAGS_PATH) as supertags:
            for line in supertags:
                new_token, tag = line.split()

                self.assign_token_to_tag(new_token, tag)

        return TagSets(self.tag_sets)
