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

        #   Get the Domino method from domino.py
        from domino import Domino

        #   Generate a deck full of Dominos using the init method from Class Domino
        self._deck = ([Domino(i, j) for i in range(7) for j in range(i + 1)])

        #   Shuffle the deck afterwards
        random.shuffle(self._deck)

        #   Creat an empty hand
        self.hand = []

        #   Draw a domino from the top of the deck
        while len(self.hand) < 7 and self._deck:
            self.hand.append(self._deck.pop())

    def is_game_won(self):
        #   The game is won if the hand AND the deck are empty
        return len(self.hand) + len(self._deck) == 0

    def is_game_lost(self):
        #   We use a recursive function to check if there's a way to play
        domino_sum_hand = [domino_in_hand.left + domino_in_hand.right for domino_in_hand in self.hand]
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

        #    We print the dominoes.
        for domino in self.hand:
            #   Because we need to show the index of each individual domino, we need to update the index attribute of
            #       the domino
            index = self.hand.index(domino) + 1
            domino.index = index
            #   We print the domino using the __str__ method
            print(domino.__str__())

        #   We wait for the discard input.
        string_to_discard = input()

        #   We check if there are only numbers in the input
        if not string_to_discard.isnumeric():
            print("You must only input numbers !")
            return self

        #   We're sure the input is only numbers, so we can transform it into a list of integers
        list_to_discard = list(set(string_to_discard))

        #   We check that the Domino the player is trying to discard is effectively in your hand
        if max(list_to_discard) >= (len(self.hand) + 1) or min(list_to_discard) <= 0:
            print("That's not a valid index (you have only ", len(self.hand), " cards in hand)!")
            return self

        #   This sum_score is used to calculate if the sum of the points on the dominoes
        #       to be discarded are 12 (or TARGET).
        sum_score = 0

        for index_domino_to_discard in list_to_discard:
            #   We calculate sum_score by summing the right and the left index
            sum_score += (self.hand[int(index_domino_to_discard) - 1][0] +
                          self.hand[int(index_domino_to_discard) - 1][1])
            self.hand[int(index_domino_to_discard) - 1] = None

        #   If the score is not TARGET, the discad is stopped
        if sum_score != TARGET:
            print("The sum must be : ", TARGET)
            return self
        self.hand = [domino for domino in self.hand if domino is not None]

        #   We print information for the player
        print("Discarded !")
        print("There are ", len(self._deck), " cards in your deck !")
        print("Drawing a new hand...")

        while len(self.hand) < 7 and self._deck:
            #   We draw again
            self.hand.append(self._deck.pop())

        return self

    def play(self):

        while not self.is_game_won():
            self.turn()
            if self.is_game_lost():
                print('You lost')
        print('You won')
