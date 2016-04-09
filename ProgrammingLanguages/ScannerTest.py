__author__ = 'Andrew'
import sys


# ParserTest.cpp
def print_token_list(tokens):
    index = 0

    while index < len(tokens):
        iterator = tokens[index]
        if type(iterator) == SymbolToken:
            print("symbol:       " + str(SymbolToken.get_value(iterator)) + "\n")
        elif type(iterator) == BooleanToken:
            if BooleanToken.get_value(iterator):
                print("boolean:       true" + "\n")
            else:
                print("boolean:       false" + "\n")
        elif type(iterator) == IntegerToken:
            print("integer:       " + str(IntegerToken.get_value(iterator)) + "\n")
        elif type(iterator) == RealToken:
            print("real:       " + str(RealToken.get_value(iterator)) + "\n")
        else:
            print("punctuation:       " + str(iterator.get_value()) + "\n")
        index += 1


def main():
    while True:
        scanner = Scanner([], -1, False, '', '')
        try:
            expr = input("SCHEME: ")
            if len(expr) == 0:
                break
        except EOFError:
            sys.exit(0)

        print(expr)
        try:
            tokens = Scanner.scan_expression(scanner, expr)
            print_token_list(tokens)
        except ScannerException:
            print("Scanner error: " + ScannerException.message + "\n")
    return 0


# scanner.cpp
class Scanner:
    tokens = []
    cursor = 0
    end_of_expr = False
    next_char = ''
    expr = ""

    def __init__(self, tokens, cursor, end_of_expr, next_char, expr):
        self.tokens = tokens
        self.cursor = cursor
        self.end_of_expr = end_of_expr
        self.next_char = next_char
        self.expr = expr

    def scan_expression(self, expression):
        self.tokens.clear()

        self.expr = expression
        self.end_of_expr = False
        self.cursor = -1

        self.advance_cursor()

        token = 0

        while token is not None:
            token = self.get_next_token()
            if token is not None:
                self.tokens.append(token)

        return self.tokens

    def get_next_token(self):
        self.skip_white_space()
        if self.end_of_expr is True:
            token = None
        elif self.is_punctuation(self.next_char):
            token = self.scan_punctuation()
        elif self.next_char == "#":
            token = self.scan_boolean()
        elif self.next_char.isalpha():
            token = self.scan_symbol()
        elif self.next_char.isnumeric() or self.next_char == '+' or self.next_char == '-' or self.next_char == '.':
            token = self.scan_number()
        else:
            ScannerException.message = "Invalid Character: " + str(self.next_char)
            raise ScannerException
        return token

    def skip_white_space(self):
        while not self.end_of_expr and self.is_white_space(self.next_char):
            self.advance_cursor()

    def advance_cursor(self):
        self.cursor += 1
        if self.cursor >= len(self.expr):
            self.end_of_expr = True
        else:
            self.next_char = self.expr[self.cursor]

    def scan_punctuation(self):
        token = PunctuationToken(self.next_char)
        self.advance_cursor()
        return token

    def scan_boolean(self):
        if self.next_char != '#':
            ScannerException.message = "badly formed boolean - expecting #"
            raise ScannerException
        self.advance_cursor()
        if self.next_char == 't':
            value = True
        elif self.next_char == 'f':
            value = False
        else:
            ScannerException.message = "badly formed boolean - expecting t or f"
            raise ScannerException
        self.advance_cursor()
        return BooleanToken(value)

    def scan_number(self):
        found_a_digit = False
        found_a_decimal_point = False
        whole_part = 0
        fraction_part = 0.0
        fraction_multiplier = 0.1
        sign = 1
        if self.next_char == '+':
            self.advance_cursor()
        elif self.next_char == '-':
            sign = -1
            self.advance_cursor()
        while not self.end_of_expr and ((self.next_char == '.') or self.next_char.isdigit()):
            if self.next_char == '.':
                if found_a_decimal_point:
                    ScannerException.message = "badly formed number - multiple decimal points"
                    raise ScannerException
                found_a_decimal_point = True
            else:
                found_a_digit = True
                if not found_a_decimal_point:
                    whole_part = whole_part * 10 + int(self.next_char) - int(ascii(0))
                else:
                    fraction_part += ((int(self.next_char) - int(ascii(0))) * fraction_multiplier)
                    fraction_multiplier /= 10
            self.advance_cursor()

        if not found_a_digit:
            ScannerException.message = "badly formed number - no digits"
            raise ScannerException
        if found_a_decimal_point:
            return RealToken(sign * (whole_part + fraction_part))
        else:
            return IntegerToken(sign * whole_part)

    def scan_symbol(self):
        symbol = ""
        if not self.end_of_expr and self.next_char.isalpha():
            symbol += self.next_char
            self.advance_cursor()
        else:
            ScannerException.message = "badly formed symbol - expecting initial letter"
            raise ScannerException
        while not self.end_of_expr and (self.next_char.isalpha() or self.next_char.isdigit()):
            symbol += self.next_char
            self.advance_cursor()
        return SymbolToken(symbol)

    def is_white_space(self, c):
        return c == ' ' or c == '\t' or c == '\n'

    def is_punctuation(self, c):
        return c == '(' or c == ')' or c == '\''


# Scanner.h
class ScannerException(Exception):
    pass
    message = "Unidentified scanner exception"


# Token.h
class Token:
    value = 0


class SymbolToken(Token):
    def __init__(self, _value):
        self.value = _value

    def get_value(self):
        return self.value


class BooleanToken(Token):
    def __init__(self, _value):
        self.value = _value

    def get_value(self):
        return self.value


class IntegerToken(Token):
    def __init__(self, _value):
        self.value = _value

    def get_value(self):
        return self.value


class RealToken(Token):
    def __init__(self, _value):
        self.value = _value

    def get_value(self):
        return self.value


class PunctuationToken(Token):
    def __init__(self, _value):
        self.value = _value

    def get_value(self):
        return self.value


class StringToken(Token):
    def __init__(self, _value):
        self.value = _value

    def get_value(self):
        return self.value


class CharacterToken(Token):
    def __init__(self, _value):
        self.value = _value

    def get_value(self):
        return self.value


if __name__ == '__main__':
    main()