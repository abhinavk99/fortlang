from enum import Enum

class Tokenization(Enum):
    """Token types"""
    INTEGER = 'INTEGER'
    EOF = 'EOF'
    ADD = 'join'
    SUBTRACT = 'leave'
    MULTIPLY = 'group'
    DIVIDE = 'split'


class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, or EOF in Tokenization Enum
        self.type = type
        # token value: integer or operation
        self.value = value

    def __str__(self):
        """String representation of Token instance.

        Examples:
            Token(INTEGER, 3)
            Token(ADD, 'join')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Interpreter(object):
    def __init__(self, text):
        # input, e.g. "3 join 5"
        self.text = text
        # index into self.text
        self.index = 0
        # current token instance
        self.curr_token = None

    def throw_error(self):
        raise Exception('Error parsing input: ', self.text)

    def get_next_token(self):
        """Lexer to split lines into tokens"""
        text = self.text

        # return Tokenization.EOF when at end of line
        if self.index > len(text) - 1:
            return Token(Tokenization.EOF, None)

        # get current character from the input, skipping one white space char
        if text[self.index].isspace():
            self.index += 1
        curr_char = text[self.index]

        # return integer token if current character is a digit
        if curr_char.isdigit():
            start_index = self.index
            while self.index < len(text) and text[self.index].isdigit():
                self.index += 1
            token = Token(Tokenization.INTEGER, int(text[start_index:self.index]))
            return token

        # return token if current character is an operation
        # operation token must be surrounded by spaces
        if curr_char in ('j', 'l', 'g', 's') and text[self.index - 1].isspace():
            sliced_4 = text[self.index:self.index + 4]
            sliced_5 = text[self.index:self.index + 5]
            # Token is 'join'
            if self.is_add_op_token(curr_char, text[self.index + 4], sliced_4):
                token = Token(Tokenization.ADD, sliced_4)
                self.index += 4
                return token
            # Token is 'leave', 'group', or 'split'
            if self.is_other_op_token(curr_char, text[self.index + 5], sliced_5):
                token = Token(self.get_token_enum(sliced_5), sliced_5)
                self.index += 5
                return token

        self.throw_error()

    def parse_expression(self):
        # set current token to the first token in input
        self.curr_token = self.get_next_token()

        # current token should be an integer
        res = self.curr_token.value
        self.validate_token(Tokenization.INTEGER)

        if self.curr_token.type in (Tokenization.ADD, Tokenization.SUBTRACT):
            return self.parse_arithmetic(res, Tokenization.ADD, Tokenization.SUBTRACT)
        else:
            return self.parse_arithmetic(res, Tokenization.MULTIPLY, Tokenization.DIVIDE)

        return res

    def parse_arithmetic(self, res, op_1, op_2):
        while self.curr_token.type in (op_1, op_2):
            op = self.curr_token
            self.validate_token(op_1, op_2)
            term = self.curr_token.value
            self.validate_token(Tokenization.INTEGER)
            res = self.evaluate_expression(res, op, term)
        return res

    def validate_token(self, *token_types):
        if self.curr_token.type not in token_types:
            self.throw_error()
        self.curr_token = self.get_next_token()

    def is_add_op_token(self, start, end, token):
        return end.isspace() and start == 'j' and token == Tokenization.ADD.value

    def is_other_op_token(self, start, end, token):
        return (
            end.isspace() and
            (start == 'l' and token == Tokenization.SUBTRACT.value) or
            (start == 'g' and token == Tokenization.MULTIPLY.value) or
            (start == 's' and token == Tokenization.DIVIDE.value)
        )

    def get_token_enum(self, token):
        """Get the Tokenization Enum that matches the operation value"""
        if token == Tokenization.SUBTRACT.value:
            return Tokenization.SUBTRACT
        elif token == Tokenization.MULTIPLY.value:
            return Tokenization.MULTIPLY
        else:
            return Tokenization.DIVIDE

    def evaluate_expression(self, left, op, right):
        """Evaluate expression based on operation"""
        if op.type == Tokenization.ADD:
            return left + right
        elif op.type == Tokenization.SUBTRACT:
            return left - right
        elif op.type == Tokenization.MULTIPLY:
            return left * right
        else:
            return left / right


def main():
    while True:
        try:
            text = input('input> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        res = interpreter.parse_expression()
        print(res)


if __name__ == '__main__':
    main()
