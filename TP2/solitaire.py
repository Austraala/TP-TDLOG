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
            if self.is_game_lost_aux(domino_sum_hand_recursive, target - domino_sum):
                return False
                # We use a recursive algorithm to check for every combination,
                # to see if the player is stuck with an unplayable hand
        return True


class InteractiveSolitaire(Solitaire):
    """
    This class extends the class Solitaire and defines methods to make it playable
    """

    def __init__(self):
        """
        We simply call the Solitaire init function
        """
        super().__init__()

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
            domino_sum_to_discard = [self.hand[i - 1].left + self.hand[i - 1].right for i in list_to_discard]
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


class AutoPlaySolitaire(Solitaire):
    """
    This class extends Solitaire to check for a potential solution
    """

    def __init__(self):
        """
        We simply call the Solitaire init function
        """
        super().__init__()

    def find_legal_turns(self):
        legal_turns = []
        domino_sum_index_hand = [[domino_in_hand.left + domino_in_hand.right, i]
                                 for i, domino_in_hand in enumerate(self.hand)]
        return self.find_legal_turns_aux(domino_sum_index_hand, TARGET, legal_turns, [])

    def find_legal_turns_aux(self, domino_sum_index_hand, target, legal_turns, current_turn):
        for sum_index in domino_sum_index_hand:
            if sum_index[0] == target:
                legal_turns.append(current_turn + [sum_index[1] + 1])
        for (domino_sum, index) in domino_sum_index_hand:
            domino_sum_index_hand_recursive = [domino_sum_index_recursive for domino_sum_index_recursive
                                               in domino_sum_index_hand if domino_sum_index_recursive[1] != index]
            self.find_legal_turns_aux(domino_sum_index_hand_recursive, target - domino_sum, legal_turns,
                                      current_turn + [index + 1])
        return list(set([tuple(set(turn)) for turn in legal_turns]))

    def find_solution(self):
        return self.find_solution_aux(self.hand, self._deck)

    def find_solution_aux(self, hand, deck):
        solitaire = AutoPlaySolitaire()
        solitaire.hand = hand
        solitaire._deck = deck
        if solitaire.is_game_won():
            print('There is a solution')
            return True
        legal_turns = solitaire.find_legal_turns()
        print(hand)
        for turn in legal_turns:
            hand_copy = [domino for domino in hand]
            deck_copy = [domino for domino in deck]
            list_turn = list(turn)
            list_turn.sort(reverse=True)
            for i in list_turn:
                if list_turn:
                    hand_copy.pop(i - 1)
            while len(hand_copy) < 7 and deck_copy:
                hand_copy.append(deck_copy.pop())
            if self.find_solution_aux(hand_copy, deck_copy):
                return True
        return False
