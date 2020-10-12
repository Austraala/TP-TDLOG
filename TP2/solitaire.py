""" File for the class "Solitaire"

   Jean-Loup Raymond & Benjamin Roulin
   ENPC - (c) 05/10/2020

"""

# Imports
import random
from domino import Domino
from exception import MyError

TARGET = 12


class Solitaire:
    """
    We define a class for the game
    it contains 2 lists of lists with 2 elements
    a deck, and a hand
    """

    def __init__(self):

        #   Generate a deck full of dominoes using the init method from Class Domino
        self._deck = [Domino(i, j) for i in range(7) for j in range(i + 1)]

        #   Shuffle the deck afterwards
        random.shuffle(self._deck)

        #   Create an empty hand
        self.hand = []

        #   Draw a domino from the top of the deck
        while len(self.hand) < 7 and self._deck:
            self.hand.append(self._deck.pop())

    def is_game_won(self):
        """
        We check if the game is won.
        The game is won if the hand AND the deck are empty
        """
        return len(self.hand) + len(self._deck) == 0

    def is_game_lost(self):
        """
        We check if the game is lost.
        It is lost if no combination of dominoes can make the target
        """
        #   We use a recursive function to check if there's a way to play
        domino_sum_hand = [domino_in_hand.left + domino_in_hand.right
                           for domino_in_hand in self.hand]
        return self.is_game_lost_aux(domino_sum_hand, TARGET)

    def is_game_lost_aux(self, domino_sum_hand, target):
        """
        This function is only called by the previous one
        during the recursive process
        """
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
        """
        This function calls everything needed to make a full turn of the game
        """
        #    We print the dominoes.
        for domino in self.hand:
            index = self.hand.index(domino) + 1
            domino.index = index
            print(domino.__str__())

        #   We wait for the discard.
        string_to_discard = input()

        try:
            list_to_discard = list(map(int, set(string_to_discard)))
            list_to_discard.sort(reverse=True)
            domino_sum_to_discard = [self.hand[i-1].left + self.hand[i-1].right for i in list_to_discard]
            if sum(domino_sum_to_discard) != TARGET:
                raise MyError()
        except ValueError:
            #   We check if there are only numbers in the input.
            print("You must only input numbers !")
        except IndexError:
            #  We check that the Domino the player is trying to discard is effectively in your hand
            print("That's not a valid index (you have only ", len(self.hand), " cards in hand)!")
        except MyError:
            #   This sum_score is used to calculate if the sum of the points on the dominoes
            #   to be discarded are 12 (or TARGET).
            print("Your sum is {0}, it should be {1}"
                  .format(sum([domino.left + domino.right
                               for i, domino in enumerate(self.hand)
                               if i + 1 in list_to_discard]), TARGET))
        else:
            for i in list_to_discard:
                self.hand.pop(i - 1)
            while len(self.hand) < 7 and self._deck:
                self.hand.append(self._deck.pop())
            print("Discarded !")
            print("There are ", len(self._deck), " cards in your deck !")
            print("Drawing a new hand...")

        return self

    def play(self):
        """
        This function does turns until the game is whether lost or won
        """
        while not self.is_game_won():
            self.turn()
            if self.is_game_lost():
                print('You lost')
                break
        print('You won')
