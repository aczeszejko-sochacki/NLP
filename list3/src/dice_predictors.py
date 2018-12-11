import numpy as np
from typing import Dict, Tuple


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


class HMMViterbiPredictor:
    """
    Predict a sequence of hidden states
    (dices) basing on created Hidden Markov Model
    """

    def compute_delta(self, act_state_ind: int, observation: any,
                      states: Tuple, delta: np.array, A: Dict,
                      B: Dict, delta_const: float) -> Tuple:
        """
        Given a_ij, b_ijo_t and delta_i(t),
        compute delta_i*a_ij*b_ijo_t
        """

        act_state = states[act_state_ind]

        deltas_with_predecesors = []

        for index, prev_state in enumerate(states):
            a_ij = A[prev_state][act_state]
            b_ijo_t = B[prev_state][observation]

            delta_i = delta[index]

            new_delta_cand = a_ij * b_ijo_t * delta_i * delta_const

            deltas_with_predecesors.append((new_delta_cand, index))

        # Return new delta and its predecesor
        return max(deltas_with_predecesors)

    def recompute_path(self, predecesors: np.array, states: Tuple,
                       last_state_ind: int) -> np.array:
        """
        Having found the best path,
        recompute the chosen states one by one,
        in reverse order
        """

        # Declare the result array of states
        results = [states[last_state_ind]]

        observation_range = range(len(predecesors)-1, 0, -1)

        last_state = last_state_ind

        # Iterate over the predecesors
        for obs_ind in observation_range:
            last_state = predecesors[obs_ind][last_state]

            results.insert(0, states[last_state])

        return results

    def predict(self, observations: np.array, A: Dict,
                B: Dict, start_states: np.array,
                delta_const: float = 6.) -> np.array:

        # Declare matrices for dynamic viterbi algorithm
        delta = np.zeros((len(observations), len(A)))
        predecesors = np.zeros((len(observations), len(A)), dtype=int)

        # Fill the start states
        delta[0] = start_states

        # Extract possible states from A
        states = tuple(A.keys())

        # Assume the order of states in A determines the order
        # of states in the delta
        observation_range = range(len(observations)-1)
        states_range = range(len(A))

        for obs_ind in observation_range:
            for act_state_ind in states_range:

                delta[obs_ind+1][act_state_ind], predecesors[obs_ind+1][act_state_ind] = \
                    self.compute_delta(act_state_ind, observations[obs_ind],
                                       states, delta[obs_ind], A, B,
                                       delta_const)

        # Choose the best path
        last_state_ind = np.argmax(delta[-1])

        return self.recompute_path(predecesors, states, last_state_ind)
