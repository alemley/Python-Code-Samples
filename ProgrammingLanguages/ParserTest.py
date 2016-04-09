__author__ = 'Andrew'
import sys


# ParserTest.cpp
def print_token_list(tokens):
    index = 0

    while index < len(tokens):
        iterator = tokens[index]
        if type(iterator) == SymbolToken:
            print("symbol:       " + str(SymbolToken.get_value(iterator)))
        elif type(iterator) == BooleanToken:
            if BooleanToken.get_value(iterator):
                print("boolean:       true")
            else:
                print("boolean:       false")
        elif type(iterator) == IntegerToken:
            print("integer:       " + str(IntegerToken.get_value(iterator)))
        elif type(iterator) == RealToken:
            print("real:       " + str(RealToken.get_value(iterator)))
        else:
            print("punctuation:       " + str(iterator.get_value()))
        index += 1


def print_spaces(spaces):
    for i in range(spaces):
        print(" ")
        i += 1


def print_parse_tree(root, spaces=0):
    if root is None:
        print_spaces(spaces)
        print("NULL")
    elif type(root) == SymbolAtom:
        print_spaces(spaces)
        print("Symbol: " + str(SymbolAtom.get_value(root)))
    elif type(root) == BooleanAtom:
        print_spaces(spaces)
        print("Boolean: ")
        if BooleanAtom.get_value(root):
            print("true")
        else:
            print("false")
    elif type(root) == IntegerAtom:
        print_spaces(spaces)
        print("Integer: " + str(IntegerAtom.get_value(root)))
    elif type(root) == RealAtom:
        print_spaces(spaces)
        print("Real: " + str(RealAtom.get_value(root)))
    elif root.object_type == "EMPTY_LIST":
        print_spaces(spaces)
        print("EmptyList:()")
    elif type(root) == Pair:
        pair = root
        print_spaces(spaces)
        print("Pair[" + str(pair) + "].car:   ")
        print_parse_tree(pair.get_car(), spaces+2)
        print("\n")
        print_spaces(spaces)
        print("Pair[" + str(pair) + "].cdr:   ")
        print_parse_tree(pair.get_cdr(), spaces+2)
        print("\n")


def print_parse_tree_as_list(root, was_car=True):
    if root is None:
        return
    elif type(root) == SymbolAtom:
        print("Symbol:" + str(SymbolAtom.get_value(root)), end='')
    elif type(root) == BooleanAtom:
        print("Boolean:", end='')
        if BooleanAtom.get_value(root):
            print("true", end='')
        else:
            print("false", end='')
    elif type(root) == IntegerAtom:
        print("Integer:" + str(IntegerAtom.get_value(root)), end='')
    elif type(root) == RealAtom:
        print("Real:" + str(RealAtom.get_value(root)), end='')
    elif root.object_type == "EMPTY_LIST":
        print("EmptyList:()", end='')
    elif type(root) == Pair:
        pair = root
        if was_car:
            print("(", end='')
        print_parse_tree_as_list(pair.get_car())
        if pair.get_cdr() is not None:
            print(" ", end='')
            print_parse_tree_as_list(pair.get_cdr(), False)
        if was_car:
            print(")", end='')


def print_scheme_expression(root, was_car=True):
    if root is None:
        return
    elif type(root) == SymbolAtom:
        print(str(SymbolAtom.get_value(root)), end='')
    elif type(root) == BooleanAtom:
        if BooleanAtom.get_value(root):
            print("#t", end='')
        else:
            print("#f", end='')
    elif type(root) == IntegerAtom:
        print(str(IntegerAtom.get_value(root)), end='')
    elif type(root) == RealAtom:
        print(str(RealAtom.get_value(root)), end='')
    elif root.object_type == "EMPTY_LIST":
        print("()")
    elif type(root) == Pair:
        pair = root
        if was_car:
            print("(", end='')
        print_scheme_expression(pair.get_car())
        if pair.get_cdr() is not None:
            print(" ", end='')
            print_scheme_expression(pair.get_cdr(), False)
        if was_car:
            print(")", end='')


def main():
    while True:
        scanner = Scanner([], -1, False, '', '')
        parser = Parser([], 0, 0)
        try:
            expr = input("SCHEME: ")
            if len(expr) == 0:
                break
        except EOFError:
            sys.exit(0)

        print(expr)
        try:
            tokens = Scanner.scan_expression(scanner, expr)
            print("Scanner Result:")
            print_token_list(tokens)
            print("\n")
        except ScannerException:
            print("Scanner error: " + ScannerException.message + "\n")
            continue
        try:
            parse_tree = Parser.initialize_parse_expression(parser, tokens)
            print("Parser Result in tree form:")
            print_parse_tree(parse_tree)
            print("Parser Result in list form:")
            print_parse_tree_as_list(parse_tree)
            print("\n")
        except ParserException:
            print("Parser error: " + ParserException.message)
            continue

        print("Parser Result as Scheme expression:")
        print_scheme_expression(parse_tree)
        print("\n")
    return 0


# Parser.cpp
class Parser:

    def __init__(self, _tokens, _token_iter, _curr_token):
        self.tokens = _tokens
        self.token_iter = _token_iter
        self. curr_token = _curr_token

    def parse(self, _tokens):
        self.token_iter = 0
        self.tokens = _tokens
        self.curr_token = self.tokens[self.token_iter]
        etree = self.parse_expression()
        if self.curr_token is not None:
            ParserException.message = "unconsumed tokens at end of expression"
            raise ParserException
        return etree

    def initialize_parse_expression(self, _tokens):
        return self.parse(_tokens)

    def parse_expression(self):
        if type(self.curr_token) == PunctuationToken and PunctuationToken.get_value(self.curr_token) == '\'':
            self.consume_token()
            return Pair((SymbolAtom("quote")), Pair(self.parse_expression(), None))
        if type(self.curr_token) == PunctuationToken and self.curr_token.value == '(':
            self.consume_token()
            if self.curr_token is None:
                ParserException.message = "Unclosed List"
                raise ParserException
            if type(self.curr_token) == PunctuationToken and self.curr_token.value == ')':
                self.consume_token()
                return EmptyList

            front_pair = None
            back_pair = None
            while type(self.curr_token) != PunctuationToken or self.curr_token.value != ')':
                next_expr = self.parse_expression()
                this_pair = Pair(next_expr, None)
                if front_pair is None:
                    front_pair = this_pair
                if back_pair is not None:
                    back_pair.set_cdr(this_pair)
                back_pair = this_pair

                if self.curr_token is None:
                    ParserException.message = "Unclosed List"
                    raise ParserException
            self.consume_token()
            return front_pair
        else:
            return self.parse_atom()

    def parse_atom(self):
        if type(self.curr_token) == SymbolToken:
            s = self.curr_token.value
            this_node = SymbolAtom(s)
            self.consume_token()
            return this_node
        elif type(self.curr_token) == BooleanToken:
            n = self.curr_token.value
            this_node = BooleanAtom(n)
            self.consume_token()
            return this_node
        elif type(self.curr_token) == IntegerToken:
            n = self.curr_token.value
            this_node = IntegerAtom(n)
            self.consume_token()
            return this_node
        elif type(self.curr_token) == RealToken:
            n = self.curr_token.value
            this_node = RealAtom(n)
            self.consume_token()
            return this_node
        else:
            ParserException.message = "Invalid Atom"
            raise ParserException

    def consume_token(self):
        if self.token_iter < (len(self.tokens) - 1):
            self.token_iter += 1
            self.curr_token = self.tokens[self.token_iter]
        elif self.token_iter == (len(self.tokens) - 1):
            self.curr_token = None


# Scanner.cpp
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

    @staticmethod
    def is_white_space(c):
        return c == ' ' or c == '\t' or c == '\n'

    @staticmethod
    def is_punctuation(c):
        return c == '(' or c == ')' or c == '\''


# Parser.h
class ParserException(Exception):
    pass
    message = "Unidentified parser exception"


# Scanner.h
class ScannerException(Exception):
    pass
    message = "Unidentified scanner exception"


# SchemeObjects.h
class SchemeObject:
    value = 0


class EmptyList(SchemeObject):
    object_type = "EMPTY_LIST"


class Pair(SchemeObject):
    def __init__(self, _car, _cdr):
        self.car = _car
        self.cdr = _cdr

    object_type = "PAIR"

    def set_car(self, _car):
        self.car = _car

    def set_cdr(self, _cdr):
        self.cdr = _cdr

    def get_car(self):
        return self.car

    def get_cdr(self):
        return self.cdr


class SymbolAtom(SchemeObject):
    def __init__(self, _value):
        self.value = _value

    def get_value(self):
        return self.value


class BooleanAtom(SchemeObject):
    def __init__(self, _value):
        self.value = _value

    def get_value(self):
        return self.value


class IntegerAtom(SchemeObject):
    def __init__(self, _value):
        self.value = _value

    def get_value(self):
        return self.value


class RealAtom(SchemeObject):
    def __init__(self, _value):
        self.value = _value

    def get_value(self):
        return self.value


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