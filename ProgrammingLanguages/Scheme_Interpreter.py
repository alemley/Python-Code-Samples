__author__ = 'Andrew'
import sys


# SymbolTable.h
class ScopeBlock:
    table = {}

    def define(self, symbol, definition):
        iter = self.table(symbol)
        if iter:
            self.table.pop(iter)
        self.table.update(symbol, definition.clone())

    def lookup(self, symbol):
        # iter = self.table(symbol)
        return self.table.get(symbol).clone()


class SymbolTable:
    def __init__(self, _global_scope, _scope_stack):
        self.global_scope = _global_scope
        self.scope_stack = _scope_stack

# make scope stack a list that can be pushed and popped. Get scope block working
    # lookup is just fetching the value, use get instead
    def delete_symbol_table(self):
        EvaluatorException.message = "delete symbol table"
        raise EvaluatorException

    def define_local(self, symbol, definition):
        if self.scope_stack.empty():
            self.global_scope.define(symbol, definition)

    def define_global(self, symbol, definition):
        self.global_scope.define(symbol, definition)

    def lookup(self, symbol):
        _def = None
        i = (len(str(self.scope_stack)) - 1)
        while i >= 0:
            _def = self.scope_stack[i].lookup(symbol)
            if _def is not None:
                break
            i = i - 1

        if _def is None:
            _def = self.global_scope.lookup(symbol)

        return _def

    def push_scope(self):
        self.scope_stack.append(ScopeBlock)
        # add elem to end

    def pop_scope(self):
        self.scope_stack.pop()
        # remove last elem


# Interpreter.cpp
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
        evaluator = Evaluator()
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
        try:
            result = evaluator.evaluate_expression(parse_tree)
        except EvaluatorException:
            print("Evaluator error: " + EvaluatorException.message)
            continue
        print("Parser Result as Scheme expression:")
        print_scheme_expression(parse_tree)
        print("\n")
        print("Result expression:")
        print_scheme_expression(result)
        print("\n")
    return 0


# Evaluator.cpp
class Evaluator:
    symtable = SymbolTable(0, 0)

    def delete_evaluator(self):
        EvaluatorException.message = "delete evaluator"
        raise EvaluatorException

    def evaluate_expression(self, _expression):
        if _expression is None:
            return None

        elif type(_expression) == BooleanAtom \
                or type(_expression) == Function \
                or type(_expression) == IntegerAtom \
                or type(_expression) == RealAtom \
                or type(_expression) == EmptyList:
            return _expression

        elif type(_expression) == SymbolAtom:
            symb_value = self.symtable.lookup(_expression.get_value())
            if symb_value is None:
                EvaluatorException.message = "undefined symbol cannot be evaluated"
                raise EvaluatorException
            return symb_value

        elif type(_expression) == Pair:
            pair = _expression
            form_or_function = pair.get_car()

            if pair.get_cdr() is None:
                arguments = None
            elif type(pair.get_cdr()) == Pair:
                arguments = pair.get_cdr()
            else:
                EvaluatorException.message = "expression has badly formed arguments"
                raise EvaluatorException

            if type(form_or_function) == SymbolAtom:
                name = form_or_function.get_value()
                if name == "define":
                    return self.evaluate_define_form(arguments)
                if name == "quote":
                    return self.evaluate_quote_form(arguments)
                if name == "let":
                    return self.evaluate_let_form(arguments)
                if name == "if":
                    return self.evaluate_if_form(arguments)

                evaluated_arguments = self.evaluate_list_elements(arguments)

                if name == "plus":
                    return self.apply_plus(evaluated_arguments)
                if name == "lessthan":
                    return self.apply_less_than(evaluated_arguments)
                if name == "car":
                    return self.apply_car(evaluated_arguments)
                if name == "cdr":
                    return self.apply_cdr(evaluated_arguments)
                if name == "cons":
                    return self.apply_cons(evaluated_arguments)
                if name == "isnull":
                    return self.apply_is_null(evaluated_arguments)

                function = self.symtable.lookup(name)

                if function is not None and type(function) == Function:
                    return self.apply_function(function, evaluated_arguments)
                else:
                    EvaluatorException.message = "expression does not start with a function"
                    raise EvaluatorException

            else:
                if type(form_or_function) != Pair:
                    EvaluatorException.message = "expected lambda expression, got something else"
                    raise EvaluatorException
                lambda_function = self.evaluate_expression(form_or_function)
                if lambda_function is None or type(lambda_function) != Function:
                    EvaluatorException.message = "expected a lambda expression, got something else"
                    raise EvaluatorException
                return self.apply_function(lambda_function, arguments)

        EvaluatorException.message = "attempt to evaluate unknown object type (this should never happen!)"
        raise EvaluatorException

    def all_integers(self, _list):
        arg = _list
        while arg is not None:
            if type(arg.get_car()) != IntegerAtom:
                return False
            arg = arg.get_cdr()
        return True

    def evaluate_list_elements(self, _list):
        if _list is None:
            return None

        new_pair = Pair(None, None)
        new_pair.set_car(self.evaluate_expression(_list.get_car()))

        rest = _list.get_cdr()
        if rest is not None and type(rest) != Pair:
            EvaluatorException.message = "badly formed argument list"
            raise EvaluatorException
        new_pair.set_cdr(self.evaluate_list_elements(rest))

        return new_pair

    def evaluate_let_form(self, _arguments):
        if _arguments.length() != 2:
            EvaluatorException.message = "incorrect number of arguments to let"
            raise EvaluatorException

        SchemeObject.car = _arguments.get_car()
        SchemeObject.cdr = _arguments.get_cdr()
        binding_list = SchemeObject.car
        if type(SchemeObject.cdr) != Pair:
            EvaluatorException.message = "bad parameter list to let"
            raise EvaluatorException
        rest = SchemeObject.cdr
        SchemeObject.car = rest.get_car()
        SchemeObject.cdr = rest.get_cdr()

        body = SchemeObject.car

        self.symtable.push_scope()

        if type(binding_list) != Pair:
            EvaluatorException.message = "bad parameter list to let"
            raise EvaluatorException
        binding_iter = binding_list

        while True:
            binding = binding_iter.get_car()

            if type(binding) != Pair:
                EvaluatorException.message = "bad parameter list to let"
                raise EvaluatorException
            if binding.length() != 2:
                EvaluatorException.message = "invalid binding given to let"
                raise EvaluatorException
            b_symbol = binding.get_car()
            b_expr = binding.get_cdr()

            if type(b_symbol) != SymbolAtom:
                EvaluatorException.message = "bad parameter list to let"
                raise EvaluatorException
            if type(b_expr) != Pair:
                EvaluatorException.message = "bad parameter list to let"
                raise EvaluatorException

            b_value = self.evaluate_expression(b_expr.get_car())
            self.symtable.define_local(b_symbol.get_value(), b_value)

            next_binding = binding_iter.get_cdr()

            if next_binding is None:
                break
            if type(next_binding) != Pair:
                EvaluatorException.message = "bad parameter list to let"
                raise EvaluatorException

            binding_iter = next_binding

        result = self.evaluate_expression(body)
        self.symtable.pop_scope()
        return result

    def evaluate_define_form(self, _arguments):
        if _arguments.length() != 2:
            EvaluatorException.message = "incorrect number of arguments to define"
            raise EvaluatorException

        arg1 = _arguments.get_car()
        rest = _arguments.get_cdr()

        if type(arg1) != SymbolAtom:
            EvaluatorException.message = "bad argument to define"
            raise EvaluatorException
        if type(rest) != Pair:
            EvaluatorException.message = "bad argument to define"
            raise EvaluatorException

        symb_name = arg1.get_value()
        arg2 = rest.get_car()
        value = self.evaluate_expression(arg2)
        self.symtable.define_global(symb_name, value)
        return None

    def evaluate_quote_form(self, _arguments):
        if _arguments.length() != 1:
            EvaluatorException.message = "incorrect number of arguments to quote"
            raise EvaluatorException
        return _arguments.get_car()

    def evaluate_if_form(self, _arguments):
        if _arguments.length() != 3:
            EvaluatorException.message = "incorrect number of arguments to if"
            raise EvaluatorException

        test = _arguments.get_car()
        rest = _arguments.get_cdr()
        consequent = rest.get_car()
        rest = rest.get_cdr()
        alternate = rest.get_cdr()

        condition = self.evaluate_expression(test)
        if condition is None:
            EvaluatorException.message = "error evaluating test condition in if form"
            raise EvaluatorException
        if type(condition) == BooleanAtom and condition.get_value is False:
            return self.evaluate_expression(alternate)
        else:
            return self.evaluate_expression(consequent)

    def evaluate_lambda_form(self, _arguments):
        if _arguments.length() != 2:
            EvaluatorException.message = "incorrect number of arguments to lambda"
            raise EvaluatorException
        if _arguments.get_car() is None or type(_arguments.get_car()) != Pair:
            EvaluatorException.message = "invalid parameter list to lambda"
            raise EvaluatorException
        formal_parameters = _arguments.get_car()
        SchemeObject.cdr = _arguments.get_cdr()

        if SchemeObject.cdr is None:
            EvaluatorException.message = "bad parameter list to lambda"
            raise EvaluatorException
        if type(SchemeObject.cdr) != Pair:
            EvaluatorException.message = "bad parameter list to lambda"
            raise EvaluatorException

        body = SchemeObject.cdr.get_car()

        arg = formal_parameters
        while arg is not None:
            if type(arg.get_car()) != SymbolAtom:
                EvaluatorException.message = "invalid parameter list to lambda"
                raise EvaluatorException
            if arg.get_cdr() is None:
                break
            if type(arg.get_cdr()) != Pair:
                EvaluatorException.message = "invalid parameter list to lambda"
                raise EvaluatorException
            arg = arg.get_cdr()
        return Function(formal_parameters.clone(), body.clone())

    def apply_plus(self, _arguments):
        if self.all_integers(_arguments):
            arg = _arguments
            result = 0
            while arg is not None:
                SchemeObject.car = arg.get_car()
                result = result + SchemeObject.car.get_value()
                arg = arg.get_cdr()
            return IntegerAtom(result)

        else:
            arg = _arguments
            result = 0.0
            while arg is not None:
                p = 0.0
                SchemeObject.car = arg.get_car()
                if type(SchemeObject.car) == IntegerAtom:
                    p = SchemeObject.car.get_value()
                elif type(SchemeObject.car) == RealAtom:
                    p = SchemeObject.car.get_value()
                else:
                    EvaluatorException.message = "invalid parameter to plus"
                    raise EvaluatorException
                result = result + p
                arg = arg.get_cdr()
            return RealAtom(result)

    def apply_less_than(self, _arguments):
        if _arguments.length() != 2:
            EvaluatorException.message = "incorrect number of arguments to lessthan"
            raise EvaluatorException
        arg1 = _arguments.get_car()
        arg2 = _arguments.get_cdr().get_car()

        if (type(arg1) != IntegerAtom and type(arg1) != RealAtom) \
                or (type(arg2) != IntegerAtom and type(arg2) != RealAtom):
            EvaluatorException.message = "invalid argument types to lessthan"
            raise EvaluatorException

        v1 = arg1.get_value()
        v2 = arg2.get_value()

        return BooleanAtom(v1 < v2)

    def apply_car(self, _arguments):
        if _arguments.length() != 1:
            EvaluatorException.message = "incorrect number of arguments to car"
            raise EvaluatorException

        arg1 = _arguments.get_car()

        if type(arg1) != Pair:
            EvaluatorException.message = "invalid argument type to car"
            raise EvaluatorException

        return arg1.get_car().clone()

    def apply_cdr(self, _arguments):
        if _arguments.length() != 1:
            EvaluatorException.message = "incorrect number of arguments to cdr"
            raise EvaluatorException

        arg1 = _arguments.get_car()

        print(type(arg1))
        if type(arg1) != Pair:
            EvaluatorException.message = "invalid argument type to cdr"
            raise EvaluatorException

        cdr = arg1.get_cdr()
        if cdr is None:
            return EmptyList()
        return cdr.clone()

    def apply_cons(self, _arguments):
        if _arguments.length() != 2:
            EvaluatorException.message = "incorrect number of arguments to cons"
            raise EvaluatorException

        arg1 = _arguments.get_car()
        arg2 = _arguments.get_cdr().get_car()

        if type(arg2) == Pair:
            return Pair(arg1.clone(), arg2.clone())
        elif type(arg2) == EmptyList:
            return Pair(arg1.clone(), None)
        else:
            EvaluatorException.message = "invalid argument types to cons"
            raise EvaluatorException

    def apply_is_null(self, _arguments):
        print(_arguments)
        print(type(_arguments))
        if _arguments.length() != 1:
            EvaluatorException.message = "incorrect number of arguments to isnull"
            raise EvaluatorException
        arg1 = _arguments.get_car()
        return BooleanAtom(arg1.object_type == "EMPTY_LIST")

    def apply_function(self, _func, _arguments):
        parameters = _func.get_parameters()
        if parameters.length() != _arguments.length():
            EvaluatorException.message = "argument list length does not match parameter list length"
            raise EvaluatorException
        self.symtable.push_scope()

        p = parameters
        a = _arguments
        while p is not None:
            name = p.get_car().get_value()
            value = a.get_car()
            self.symtable.define_local(name, value)
            p = p.get_cdr()
            a = a.get_cdr()

        result = self.evaluate_expression(_func.get_body())

        self.symtable.pop_scope()

        return result


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


# Evaluator.h
class EvaluatorException(Exception):
    pass
    message = "Unidentified evaluator exception"


# SchemeObjects.h
class SchemeObject:
    value = 0


class EmptyList(SchemeObject):
    object_type = "EMPTY_LIST"

    def clone(self):
        return EmptyList()


class Pair(SchemeObject):
    def __init__(self, _car, _cdr):
        self.car = _car
        self.cdr = _cdr

    object_type = "PAIR"

    def delete_pair(self):
        if self.car is not None:
            del self.car
        if self.cdr is not None:
            del self.cdr

    def clone(self):
        c = Pair(None, None)
        if self.car is not None:
            c.car = self.car.clone()
        if self.cdr is not None:
            c.cdr = self.cdr.clone()
        return c

    def set_car(self, _car):
        self.car = _car

    def set_cdr(self, _cdr):
        self.cdr = _cdr

    def get_car(self):
        return self.car

    def get_cdr(self):
        return self.cdr

    def length(self):
        if self.cdr is None:
            return 1
        if type(self.cdr) != Pair:
            return 1
        return 1+(self.cdr.length())


class Function(SchemeObject):
    parameters = None
    body = None

    def __init__(self, _params=None, _body=None):
        self.parameters = _params
        self.body = _body

    def delete_function(self):
        c = Function()
        if self.parameters is not None:
            c.parameters = self.parameters.clone()
        if self.body is not None:
            c.body = self.body.clone()
        return c

    object_type = "FUNCTION"

    def set_parameters(self, _params):
        self.parameters = _params

    def set_body(self, _body):
        self.body = _body

    def get_parameters(self):
        return self.parameters

    def get_body(self):
        return self.body


class SymbolAtom(SchemeObject):
    def __init__(self, _value):
        self.value = _value

    def clone(self):
        return SymbolAtom(self.value)

    def get_value(self):
        return self.value


class BooleanAtom(SchemeObject):
    def __init__(self, _value):
        self.value = _value

    def clone(self):
        return BooleanAtom(self.value)

    def get_value(self):
        return self.value


class IntegerAtom(SchemeObject):
    def __init__(self, _value):
        self.value = _value

    def clone(self):
        return IntegerAtom(self.value)

    def get_value(self):
        return self.value


class RealAtom(SchemeObject):
    def __init__(self, _value):
        self.value = _value

    def clone(self):
        return RealAtom(self.value)

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