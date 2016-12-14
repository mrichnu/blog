import re

class StringCalculator(object):

    def Add(self, numbers_str):
        if numbers_str == "":
            return 0

        if numbers_str[0:2] == "//":
            numbers_str = self._handle_alternate_delimiter(numbers_str)

        # replace newline chars with commas
        numbers_str = numbers_str.replace("\n", ",")

        # split on commas
        numbers = [int(n) for n in numbers_str.split(",")]

        # find negatives
        negatives = self._find_negatives(numbers)
        if len(negatives):
            raise Exception("Negatives not allowed: %s" %
                (','.join([str(n) for n in negatives])))

        s = 0
        for n in numbers:
            if n > 1000:
                continue
            s += n

        return s

    def _handle_alternate_delimiter(self, numbers):
        if numbers[2] == "[":
            delims = re.findall("\[([^][]+)\]", numbers)
        else:
            delims = [numbers[2]]

        num_list_begin = numbers.find("\n") + 1
        numbers = numbers[num_list_begin:]

        for delim in delims:
            numbers = numbers.replace(delim,",")

        return numbers

    def _find_negatives(self, numbers):
        negatives = []
        for n in numbers:
            if n < 0:
                negatives.append(n)

        return negatives
            
