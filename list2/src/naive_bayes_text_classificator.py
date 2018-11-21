import numpy as np
import pandas as pd
from .parsers.unigram_parser import Unigrams
from typing import Tuple, Set, List


class NaiveBayesText:
    """
    Given a tuple of the unigrams of each class
    try to predict a test text class
    """

    def __init__(self, unigrams_all_targets: Tuple):
        self.unigrams_all_targets = unigrams_all_targets
        self.target_names = self.get_target_names()

    def create_set_of_all_tokens(self) -> Set:
        all_tokens = set()
        for target in self.unigrams_all_targets:
            all_tokens.update(target.unigrams.keys())

        return all_tokens

    def get_target_names(self) -> List:
        target_names = [target.name for target in self.unigrams_all_targets]

        return target_names

    def fit(self, new_features: Tuple = None) -> pd.DataFrame:

        # Find tokens space
        all_tokens = self.create_set_of_all_tokens()

        # Build model
        model = pd.DataFrame(columns=self.target_names, index=all_tokens)

        # Add optional additional features
        if new_features is not None:
            for feature_name, feature_values in new_features:
                model = self.add_new_feature_to_model(model,
                                                      feature_name,
                                                      feature_values)

        # Set all values to zero by default
        model.fillna(0, inplace=True)

        for target in self.unigrams_all_targets:
            for token in target.unigrams:
                model[target.name][token] = target.unigrams[token]

        # Normalize values to a probability distribution
        model_norm = model.divide(model.values.sum(0) * \
                     len(self.target_names))

        return model_norm

    def add_new_feature_to_model(self, model: pd.DataFrame,
                                 feature_name: str,
                                 feature_values: Tuple) -> pd.DataFrame:
        """
        By default the model is based on the tokens,
        but we can add another feature
        """
        model.loc[feature_name] = feature_values

        return model

    def predict(self, model: pd.DataFrame,
                unigrams_test: Unigrams) -> int:
        """
        Predict a class of the text
        basing on the given text unigrams
        """

        # Declare results series
        results = pd.Series(0.0, index=self.target_names)

        denominator = model.values.sum(0)[0]

        for token in unigrams_test.unigrams:
            if token in model.index:
                # As the values are normalized,
                # denominator is the same in all cases
                results += np.log(model.loc[token] + 0.000001 / denominator)

        return results.idxmax()
