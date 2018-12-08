import numpy as np
from typing import Tuple, List


class DiceRollsGenerator:

    def roll_dice(self, distr: Tuple) -> int:
        """
        Return random roll of a dice with
        the given distribution
        """

        roll = np.random.choice(np.arange(1, 7), 1, p=distr)[0]

        return roll

    def draw_dice(self, last_dice: str, p_fair_to_cheat: float,
                  p_cheat_to_fair: float) -> str:
        """
        Return the name of a drawn dice. There are
        two dices — fair ('u') and cheat — ('n')
        """

        # Establish probs depending on the last dice
        if last_dice == 'u':
            probs = [1-p_fair_to_cheat, p_fair_to_cheat]
        else:
            probs = [p_cheat_to_fair, 1-p_cheat_to_fair]

        new_dice = np.random.choice(['u', 'n'], 1, p=probs)[0]

        return new_dice

    def generate_rolls(self, fair_distr: Tuple, cheat_distr: Tuple,
                       p_fair_to_cheat: float, p_cheat_to_fair: float,
                       n_rolls: int) -> Tuple:
        """
        Generate a sequence of rolls
        described as pairs (value, fair/cheat).
        u — fair, n — unfair
        """

        # First roll is fair
        rolls, dices = [self.roll_dice(fair_distr)], ['u']

        # Then before each roll draw the dice
        for roll in range(n_rolls):
            dice = self.draw_dice(dices[-1], p_fair_to_cheat, p_cheat_to_fair)
            dices.append(dice)

            distr = fair_distr if dice == 'u' else cheat_distr
            rolls.append(self.roll_dice(distr))

        return np.array(rolls), np.array(dices)
