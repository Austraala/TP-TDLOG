#!/usr/bin/env python
"""TDLOG TP1 - Mathieu Bernard"""

import random


###############################################################################
# TP part 1
###############################################################################


_LIMIT = '+-----|-----+'
"""The top and bottom lines of a domino representation"""


_DOTS = [
    ['     ', '     ', '     '],
    ['     ', '  *  ', '     '],
    ['*    ', '     ', '    *'],
    ['*    ', '  *  ', '    *'],
    ['*   *', '     ', '*   *'],
    ['*   *', '  *  ', '*   *'],
    ['* * *', '     ', '* * *']]
"""The dots lines of a domino representation"""


def print_domino(index, domino):
    """Prints a domino representation to stdout

    Parameters
    ----------
    index: The domino index
    domino: A pair of integers in [0, 6]

    Raises
    ------
    ValueError if the domino `value` is not correct

    """
    # retrieve the left and right domino values, ensure it is valid
    if len(domino) != 2:
        raise ValueError('invalid domino')

    left, right = domino

    if not 0 <= left <= 6 or not 0 <= right <= 6:
        raise ValueError('invalid domino')

    # build the domino representation line by line
    index = str(index)
    prefix = ' ' * (len(index) + 3)
    result = '\n'.join([
        prefix + _LIMIT,
        prefix + '|' + _DOTS[left][0] + '|' + _DOTS[right][0] + '|',
        f'({index}) |' + _DOTS[left][1] + '|' + _DOTS[right][1] + '|',
        prefix + '|' + _DOTS[left][2] + '|' + _DOTS[right][2] + '|',
        prefix + _LIMIT]) + '\n'

    print(result)


def print_dominos(dominos):
    """Prints a list of `dominos` to stdout

    Parameters
    ----------
    dominos: A list of pairs of integers in [0, 6], each pair representing a
        single domino

    Raises
    ------
    ValueError if one of the dominos value is not correct

    """
    for index, domino in enumerate(dominos):
        print_domino(index + 1, domino)

###############################################################################
# TP part 2
###############################################################################


DOMINOS_SET = [(left, right) for left in range(7) for right in range(left + 1)]
"""The 28 dominos in the game"""


HAND_SIZE = 7
"""Number of dominos in the hand"""


TARGET = 12
"""Number of points on dominos to discard them"""


def play():
    """The game main loop

    Returns
    -------
    True if the game is won. Note: the defeat conditions are not tested.

    """
    # shuffle the dominos set
    pile = random.sample(DOMINOS_SET, k=len(DOMINOS_SET))
    hand = []

    while True:
        # fill the hand with HAND_SIZE dominos until the pile is empty
        while len(hand) != HAND_SIZE and pile:
            hand.append(pile.pop())

        # check if the game is won (the hand and the pile are empty)
        if not hand:
            print('You win!')
            return True

        # print the dominos hand and ask the player to play
        print_dominos(hand)
        indexes = input(f'pile size = {len(pile)}, dominos to discard?')

        # count the sum of the selected dominos
        try:
            indexes = sorted(
                {int(idx) - 1 for idx in indexes}, reverse=True)
            total = sum(hand[idx][0] + hand[idx][1] for idx in indexes)
        except (ValueError, IndexError):
            print('invalid indexes')
            continue

        # If the total is correct, discard the selected dominos
        if total != TARGET:
            print(f'invalid total ({total} but expected {TARGET})')
        else:
            for idx in indexes:
                hand.pop(idx)


def main():
    """Entry point of the program, run a domino game"""
    play()


if __name__ == '__main__':
    main()
