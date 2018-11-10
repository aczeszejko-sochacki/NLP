import os
from typing import Dict, List, Type
from ..exceptions import TokenNotTagged, TagDoesNotExist
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

    def get_sentence_tags(self, sentence: str) -> str:
        sentence_tags = []

        for token in sentence.split():
            try:
                token_tag = self.get_token_tag(token)

                sentence_tags.append(token_tag)
            except TokenNotTagged:
                sentence_tags.append(None)  # TODO Tag unknown

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
