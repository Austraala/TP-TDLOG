""" File for the class "Domino"

   Jean-Loup Raymond & Benjamin Roulin
   ENPC - (c) 05/10/2020

"""

class Domino:
    #   We give the two numbers on both halves of the Domino
    right = None
    left = None
    #   We added another part to the Domino's attribute : the index
    index = None

    #   Special Methods

    #   Returns "Domino(X, Y)"
    def __repr__(self):

        return "Domino(" + str(self.left) + ", " + str(self.right) + ")"

    #   Returns the Domino's drawing, using the functions defined above
    def __str__(self):

        #   First, we define all functions needed
        def print_line():
            return "     +-----|-----+"

        def create_str_domino(number):
            if number == 0:
                line_1 = '     '
                line_2 = '     '
                line_3 = '     '
            elif number == 1:
                line_1 = '     '
                line_2 = '  *  '
                line_3 = '     '
            elif number == 2:
                line_1 = '*    '
                line_2 = '     '
                line_3 = '    *'
            elif number == 3:
                line_1 = '*    '
                line_2 = '  *  '
                line_3 = '    *'
            elif number == 4:
                line_1 = '*   *'
                line_2 = '     '
                line_3 = '*   *'
            elif number == 5:
                line_1 = '*   *'
                line_2 = '  *  '
                line_3 = '*   *'
            else:
                line_1 = '*   *'
                line_2 = '*   *'
                line_3 = '*   *'
            return line_1, line_2, line_3

        def print_one_domino(self_domino):
            # We generate the lines of the domino
            # This function gets a Domino object plugged in
            left_line_1, left_line_2, left_line_3 = create_str_domino(self_domino.left)
            right_line_1, right_line_2, right_line_3 = create_str_domino(self_domino.right)
            line_1 = '     |{0}|{1}|'.format(left_line_1, right_line_1)
            line_2 = '({0})  |{1}|{2}|'.format(self_domino.index, left_line_2, right_line_2)
            line_3 = '     |{0}|{1}|'.format(left_line_3, right_line_3)

            printed_lines = [line_1, line_2, line_3]

            return printed_lines

        #   Then, we use them to return the string we need
        return (print_line() + "\n" +
                print_one_domino(self)[0] + "\n" +
                print_one_domino(self)[1] + "\n" +
                print_one_domino(self)[2] + "\n" +
                print_line()
                )

    #   Other Special Methods
    def __eq__(self, other):
        #   First case : exact same
        if self.right == other.right and self.left == other.left:
            return True
        #   Second case : inverted, but still same
        elif self.right == other.left and self.left == other.right:
            return True
        else:
            return False

    def __ne__(self, other):
        return not(Domino.__eq__(self, other))
