Coding Kata: Bank OCR
####################################################################

:date: 2013-12-23 14:40
:tags: python, katas, programming, practice
:author: Matthew Rich
:summary: A simple coding exercise

Alone in the office right before a holiday, and not having written any
interesting code in a couple of weeks, I decided to tackle a `coding kata`_
after remembering that they are a thing. Although as noted by the `Coding Horror
blog`_ years ago, katas are only one technique that a programmer should use to
practice their craft (and a relatively unimportant one at that), the fact is
that my fingers were itching to write some code after spending all of the
preceding week doing server and data center maintenance stuff, and with a long
holiday away from computers coming up.

The kata I chose is `KataBankOCR`_ and here is the first user story:
::

    User Story 1

    You work for a bank, which has recently purchased an ingenious machine to
    assist in reading letters and faxes sent in by branch offices. The machine
    scans the paper documents, and produces a file with a number of entries which
    each look like this:

      _  _     _  _  _  _  _
    | _| _||_||_ |_   ||_||_|
    ||_  _|  | _||_|  ||_| _| 
                           
    Each entry is 4 lines long, and each line has 27 characters. The first 3
    lines of each entry contain an account number written using pipes and
    underscores, and the fourth line is blank. Each account number should have
    9 digits, all of which should be in the range 0-9. A normal file contains
    around 500 entries.

    Your first task is to write a program that can take this file and parse it
    into actual account numbers.

I spent about two hours working out a solution to this problem using python.
What can I say, I'm slow and easily distracted. Here is the ``tests.py``:

.. sourcecode:: python

    import unittest
    import ocrkata

    class TestReadEntries(unittest.TestCase):

        def test_read_zeroes(self):
            input = " _  _  _  _  _  _  _  _  _ "\
                    "| || || || || || || || || |"\
                    "|_||_||_||_||_||_||_||_||_|"

            account_number = ocrkata.parse_account_number(input)
            self.assert_(account_number == (0,0,0,0,0,0,0,0,0))

        def test_read_ones(self):
            input = "                           "\
                    "  |  |  |  |  |  |  |  |  |"\
                    "  |  |  |  |  |  |  |  |  |"

            account_number = ocrkata.parse_account_number(input)
            self.assert_(account_number == (1,1,1,1,1,1,1,1,1))

        def test_get_lines(self):
            input = "                           "\
                    "  |  |  |  |  |  |  |  |  |"\
                    "  |  |  |  |  |  |  |  |  |"

            lines = ocrkata.get_lines(input)
            self.assert_(lines[0][0] == ' ')
            self.assert_(lines[1][1] == ' ')
            self.assert_(lines[2][2] == '|')

        def test_get_cells(self):
            input = " _  _  _  _  _  _  _  _  _ "\
                    "| || || || || || || || || |"\
                    "|_||_||_||_||_||_||_||_||_|"

            cells = ocrkata.get_cells(input)

            self.assert_(ocrkata.format_cell(cells[0]) == " _ \n| |\n|_|")

        def test_get_account_numbers_from_file(self):
            filename = 'entries.txt'
            account_numbers = ocrkata.get_account_numbers_from_file(filename)
            self.assert_(account_numbers[10] == (1,2,3,4,5,6,7,8,9))

    if __name__ == '__main__':
        unittest.main()

These are really more integration tests than unit tests -- only
``test_get_lines`` and ``test_get_cells`` could properly be called unit tests.
But the last test is the one that proves that we have solved the user story
with a file called `entries.txt <{filename}/extra/bank-ocr/entries.txt>`_
that conforms to the specification. 

And the implementation, ``ocrkata.py``:

.. sourcecode:: python

    #    _  _     _  _  _  _  _ 
    #  | _| _||_||_ |_   ||_||_|
    #  ||_  _|  | _||_|  ||_| _|

    # 3x3 cells "unrolled" into a single line
    CELL_VALUES = {
            ' _ | ||_|': 0,
            '     |  |': 1,
            ' _  _||_ ': 2,
            ' _  _| _|': 3,
            '   |_|  |': 4,
            ' _ |_  _|': 5,
            ' _ |_ |_|': 6,
            ' _   |  |': 7,
            ' _ |_||_|': 8,
            ' _ |_| _|': 9
    }

    def parse_account_number(input):
        # input has 9 3x3 "cells".
        # break it up into individual cells.

        cells = get_cells(input)
        cell_values = []
        for cell in cells:
            cell_values.append(get_cell_value(cell))

        return tuple(cell_values)

    def get_cells(input):
        cells = []

        # copy into lines
        lines = get_lines(input)

        for offset in range(0, 26, 3):
            # offset, 0 will be top left of cell
            # offset + 2, 2 will be bottom right
            cell = lines[0][offset:offset+3]
            cell += lines[1][offset:offset+3]
            cell += lines[2][offset:offset+3]

            cells.append(cell)

        return cells

    def get_lines(input):
        lines = ["","",""]
        offset = 0

        for char in input:
            lines[offset] += char
            if len(lines[offset]) == 27:
                offset += 1

        return lines

    def format_cell(cell):
        return "%s\n%s\n%s" % (cell[0:3],cell[3:6],cell[6:9])

    def get_cell_value(cell):
        return CELL_VALUES.get(cell, -1)

    def get_account_numbers_from_file(filename):
        """Returns all account numbers found in <filename>, as a list of tuples"""

        account_numbers = []

        linecount = 0
        numberlines = ''
        with open(filename, 'r') as f:
            for line in f:
                linecount += 1

                if (linecount % 4) == 0:
                    account_numbers.append(parse_account_number(numberlines))
                    numberlines = ''
                else:
                    # make sure to trim trailing newline
                    numberlines += line.rstrip('\n')

        return account_numbers

This is a pretty naive implementation. I used the technique that I expect most
people tackling this problem will use to translate the 3x3 cells of underscore
and pipe characters into base-10 digits; namely, a map. In this particular case
in the ``get_cells`` function I "unroll" the 3x3 cell of characters into a
single line and then use the ``CELL_VALUES`` dict defined at the top of the
file to look up values. The only other interesting thing is the way
``get_cells`` assumes its input will be a list containing 3 strings of at least
27-characters, and how ``get_account_numbers_from_file`` turns each 4-line
segment of the input file into a single string which is later turned back into
a 3-element list by ``get_lines``. Obviously some major refactoring is possible
there. Another thing that is missing is any sort of error handling at all.

But I wasn't going for elegance or efficiency here, just trying to write the
spec first according to the user story, and then write code as quickly as
possible to fulfill the spec. Only in going over it later do I see all the
little ways I could streamline the code and make it nicer to read.

I hope to turn this into a series of posts, where I first go about refactoring
this code before moving on to the other user stories in the kata, which involve
checksumming the account numbers and trying to handle ambiguous numbers.

.. _coding kata: http://en.wikipedia.org/wiki/Kata_(programming)
.. _Coding Horror blog: http://www.codinghorror.com/blog/2008/06/the-ultimate-code-kata.html
.. _KataBankOCR: http://codingdojo.org/cgi-bin/wiki.pl?KataBankOCR
