""" File for the class "Solitaire"

   Jean-Loup Raymond & Benjamin Roulin
   ENPC - (c) 05/10/2020

"""

import random


TARGET = 12


class Solitaire:
    """
    We define a class for the game
    it contains 2 lists of lists with 2 elements
    a deck, and a hand
    """
    def __init__(self):
        self._deck = ([[i, j] for i in range(7) for j in range(i + 1)])
        random.shuffle(self._deck)
        self.hand = []
        while len(self.hand) < 7 and self._deck:
            self.hand.append(self._deck.pop())

    def is_game_won(self):
        return len(self.hand) + len(self._deck) == 0

    def is_game_lost(self):
        domino_sum_hand = [domino[0] + domino[1] for domino in self.hand]
        return self.is_game_lost_aux(domino_sum_hand, TARGET)

    def is_game_lost_aux(self, domino_sum_hand, target):
        for domino_sum in domino_sum_hand:
            if domino_sum == target:
                # Objective is 12 with the current rule-set, but it can be changed easily
                return False
        for i, domino_sum in enumerate(domino_sum_hand):
            domino_sum_hand_recursive = [domino_sum_recursive for j, domino_sum_recursive
                                         in enumerate(domino_sum_hand) if j != i]
            if self.is_game_lost_aux(domino_sum_hand_recursive, target):
                return False
                # We use a recursive algorithm to check for every combination,
                # to see if the player is stuck with an unplayable hand
        return True

    def turn(self):

        for domino in self.hand:
            print(domino.__str__())

        string_to_discard = input()

        if not string_to_discard.isnumeric():
            print("You must only input numbers !")
            return self

        list_to_discard = list(set(string_to_discard))

        if max(list_to_discard) >= (len(self.hand) + 1) or min(list_to_discard) <= 0:
            print("That's not a valid index (you have only ", len(self.hand), " cards in hand)!")
            return self

        sum_score = 0

        for index_domino_to_discard in list_to_discard:
            sum_score += (self.hand[int(index_domino_to_discard) - 1][0] +
                          self.hand[int(index_domino_to_discard) - 1][1])
            self.hand[int(index_domino_to_discard) - 1] = None

        if sum_score != TARGET:
            print("The sum must be : ", TARGET)
            return self
        self.hand = [domino for domino in self.hand if domino is not None]

        print("Discarded !")
        print("There are ", len(self._deck), " cards in your deck !")
        print("Drawing a new hand...")

        while len(self.hand) < 7 and self._deck:
            self.hand.append(self._deck.pop())

        return self

    def play(self):

        while not self.is_game_won():
            self.turn()
            if self.is_game_lost():
                print('You lost')
        print('You won')
