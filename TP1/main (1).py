# This is the domino game
#
#   Jean-Loup Raymond & Benjamin Roulin
#   ENPC - (c) 03/10/2020
#
#

####
# Note : 4
# - vous n'étiez pas loin du 5, il y a cependant trop de complexité et trop de
#   petits défauts. Voir mes remarques dans le code
# - pas tout à fait conforme au sujet : il manque la fonction pour print un
#   seul domino comme demandé
# - le time.sleep n'est pas vraiment utile
####

# Imports
#### Mauvaise pratique de faire des "import *" ! Source de bugs et rend le code
#### confus
from random import *
import time


def print_line():
    print("     +-----|-----+")


def create_str_domino(n):
    if n == 0:
        line_1 = '     '
        line_2 = '     '
        line_3 = '     '
    elif n == 1:
        line_1 = '     '
        line_2 = '  *  '
        line_3 = '     '
    elif n == 2:
        line_1 = '*    '
        line_2 = '     '
        line_3 = '    *'
    elif n == 3:
        line_1 = '*    '
        line_2 = '  *  '
        line_3 = '    *'
    elif n == 4:
        line_1 = '*   *'
        line_2 = '     '
        line_3 = '*   *'
    elif n == 5:
        line_1 = '*   *'
        line_2 = '  *  '
        line_3 = '*   *'
    else:
        line_1 = '*   *'
        line_2 = '*   *'
        line_3 = '*   *'
    return line_1, line_2, line_3


def print_domino(domino_list):
    #### can be refactored as:
    #### for index, domino in enumerate(domino_list):
    for i in range(len(domino_list)):
        # We generate the lines of the domino
        left_line_1, left_line_2, left_line_3 = create_str_domino(domino_list[i][0])
        right_line_1, right_line_2, right_line_3 = create_str_domino(domino_list[i][1])

        #### '{0}'.format(toto) peut s'écrire plus simplement en f'{toto}'
        line_1 = '     |{0}|{1}|'.format(left_line_1, right_line_1)
        line_2 = '({0})  |{1}|{2}|'.format(i + 1, left_line_2, right_line_2)
        line_3 = '     |{0}|{1}|'.format(left_line_3, right_line_3)

        # We print the domino
        print_line()
        print(line_1)
        print(line_2)
        print(line_3)
        print_line()


def create_deck():
    deck = [[i, j] for i in range(7) for j in range(i + 1)]
    # We generate the deck in order
    #### Beacoup mieux d'utiliser random.shuffle
    shuffle(deck)
    # We shuffle it afterwards in a random order
    return deck


def draw(hand, deck):
    ####
    # Fusionner les 2 conditions en un test :
    # while len(hand) < 7 and deck:
    #     hand.append(deck.pop())
    ####
    # First condition : hand mustn't have space in it (upper limite of 7)
    while len(hand) < 7:
        # Second condition : the deck must be empty
        if len(deck) > 0:
            #### variable draw à le même nom que la fonction !!
            draw = deck.pop()
            hand.append(draw)
        else:
            break


def check_index_input(string_to_discard, hand):
    # Check that the whole input is only composed of numbers
    ### Bien le isnumeric !
    if not string_to_discard.isnumeric():
        print("You must only input numbers !")
        time.sleep(1)
        return False

    # Check that the index is valid (not out of bounds for the hand
    ####
    # ou bien array_string_to_discard = [int(s) for s in string_to_discard]
    # plus explicite que list(map())
    ####
    array_string_to_discard = list(map(int, string_to_discard))
    if max(array_string_to_discard) >= (len(hand)+1) or min(array_string_to_discard) <= 0:
        print("That's not a valid index (you have only ", len(hand), " cards in hand)!")
        time.sleep(1)
        return False

    return True


#### compléxité non nécessaire, pour enlever les doublons d'une liste, il
#### suffit d'en construire un set
def check_duplicates(string_to_discard):
    seen, yields = set(), set()
    for number in string_to_discard:
        if number in seen:
            if number not in yields:
                yield number
                yields.add(number)
            else:
                yields.add(number)
        else:
            seen.add(number)


#### cette fonction part d'une très bonne idée (vérifier la validité de l'input
#### du joueur)mais est trop complexe. Pourquoi hand_copy ?
def discard(string_to_discard, hand, objective, deck):
    sum_score = 0   # This variable is used to check the score of the chosen dominoes
    hand_copy = hand.copy()

    # You can't put letters or invalid numbers
    if not check_index_input(string_to_discard, hand):
        time.sleep(1)
        return hand_copy

    #### il aurait suffit d'ignorer les doublons (voir remarque ci-dessus)
    # You can't discard the same domino multiple times
    if len(list(check_duplicates(string_to_discard))) != 0:
        print("You can't discard the same domino multiple times!")
        time.sleep(2)
        return hand_copy

    # If all's good, the discard is done, and the player is informed of the situation
    #### use enumerate()
    #### declare sum_score just here
    for i in range(len(string_to_discard)):
        #### simplification : index = int(string_to_discard[i])-1
        sum_score += (hand[int(string_to_discard[i])-1][0] + hand[int(string_to_discard[i])-1][1])
        hand_copy[int(string_to_discard[i])-1] = None

    # The score must be 12 to allow the discard, otherwise nothing happens
    if sum_score != 12:
        print("The sum must be : ", objective)
        time.sleep(2)
        return hand

    new_hand = [domino for domino in hand_copy if (domino is not None)]

    print("Discarded !")
    time.sleep(0.5)
    print("There are ", len(deck), " cards in your deck !")
    time.sleep(1)
    print("Drawing a new hand...")
    time.sleep(1)

    return new_hand


def create_sum_domino_hand(hand):
    sum_domino_hand = [domino[0]+domino[1] for domino in hand]
    return sum_domino_hand


def check_defeat(sum_domino_hand, objective):
    for sum_domino in sum_domino_hand:
        if sum_domino == objective:
            # Objective is 12 with the current ruleset, but it can be changed easily
            return True

    for i in range(len(sum_domino_hand)):
        objective_temp = objective
        #### use enumerate
        sum_domino_hand_recursive = [sum_domino_hand[j] for j in range(len(sum_domino_hand)) if (j != i)]
        if check_defeat(sum_domino_hand_recursive, objective_temp-sum_domino_hand[i]):
            return True
            # We use recursivity to check for every combination,
            # to see if the player is stuck with an unplayable hand

    return False


# Press the green button in the gutter to run the script.
#### if __name__ == '__main__':
if 'main':

    objective = 12  # The score for discarding (can be changed)

    # We create the deck and the initial hand
    deck = create_deck()
    hand = []
    draw(hand, deck)

    # We create the game

    #### parenthèses superflues
    while (len(deck)+len(hand)) > 0:    # As long as there are dominoes that aren't discarded
        # Loop
        print_domino(hand)  # Every turn, the player must see their hand
        string_to_discard = input()     # We ask the player for the string
        hand = discard(string_to_discard, hand, objective, deck)
        # The discarding only occurs if the condition is met

        draw(hand, deck)
        # Check for defeat
        sum_domino_hand = create_sum_domino_hand(hand)
        if not check_defeat(sum_domino_hand, objective):
            print_domino(hand)
            print('You just lost !')    # The game tells you you lost
            break

    # Check for Victory
    if (len(deck)+len(hand)) == 0:
        print('You win')
