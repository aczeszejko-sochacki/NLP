import numpy as np


class HeuristicPredictor:
    """
    Predict a sequence of hidden states
    (dices) basing on the 6s density
    """

    def predict(self, rolls: np.array, p_cheat_to_fair: float,
                min_six_subset_ratio: float = 1/3) -> np.array:
        """
        Cheat sequences are of length at least 2
        and with 6s ratio at least 1/2
        """

        n_rolls = len(rolls)
        dices_predict = np.full_like(rolls, 'u', dtype='<U1')

        # Assume the cheat subset should not be longer
        # than 1 / p_cheat_to_fair
        cheat_max_length = int(1 / p_cheat_to_fair)

        start_subset = 0

        while start_subset < n_rolls:
            # Declare number of 6 values in the subset
            n_six = 0

            for end_subset in range(start_subset,
                                    start_subset + cheat_max_length):

                # Assume every 6 is from cheat distr
                if rolls[end_subset] == 6:
                    n_six += 1

                # Break if there are too less 6 in the subset
                six_subset_ratio = n_six / (end_subset - start_subset + 1)

                if six_subset_ratio  < min_six_subset_ratio:
                    start_subset = end_subset + 1
                    break

                # If we exceed minimium ratio, classify as cheat
                dices_predict[end_subset] = 'n'

                # Break if we have the subset of max length
                if end_subset == start_subset + cheat_max_length - 1:
                    start_subset = end_subset + 1
                    break

                # End if we run out the rolls
                if end_subset == n_rolls-1:
                    return dices_predict

        return dices_predict
