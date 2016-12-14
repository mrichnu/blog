import unittest
from StringCalculatorKata import StringCalculator

class StringCalculatorTestCase(unittest.TestCase):

    def setUp(self):
        self.calc = StringCalculator()

    def test_empty_string_returns_0(self):
        self.assert_(self.calc.Add("") == 0)

    def test_1_returns_1(self):
        self.assert_(self.calc.Add("1") == 1)

    def test_1_2_returns_3(self):
        self.assert_(self.calc.Add("1,2") == 3)

    def test_1_2_returns_3(self):
        self.assert_(self.calc.Add("1,2") == 3)
    
    def test_4_5_returns_9(self):
        self.assert_(self.calc.Add("4,5") == 9)

    def test_1_2_3_4_5_returns_15(self):
        self.assert_(self.calc.Add("1,2,3,4,5") == 15)

    def test_1_newline_2_returns_3(self):
        self.assert_(self.calc.Add("1\n2") == 3)

    def test_alternate_delimiter(self):
        self.assert_(self.calc.Add("//;\n1;2") == 3)

    def test_handles_one_negative(self):
        with self.assertRaises(Exception) as cm:
            self.calc.Add("-1,2")

        print cm.exception.message
        self.assert_(cm.exception.message == "Negatives not allowed: -1")

    def test_handles_two_negatives(self):
        with self.assertRaises(Exception) as cm:
            self.calc.Add("2,-4,3,-5")

        print cm.exception.message
        self.assert_(cm.exception.message == "Negatives not allowed: -4,-5")

    def test_ignores_greater_than_1000(self):
        self.assert_(self.calc.Add("1001,2") == 2)

    def test_handle_any_delimiter(self):
        self.assert_(self.calc.Add("//[***]\n1***2***3") == 6)

    def test_handle_multiple_delimiters_of_any_length(self):
        self.assert_(self.calc.Add("//[*][%%]\n1*2%%3") == 6)

