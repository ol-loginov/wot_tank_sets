# coding=utf-8

from code_blocks import Block, BlockFactory, BlockMachine, ALL_GENERATORS
from code_statements import Constant, Reference, Assign, FunctionCall, Returns, StatementBase, List, Set, UnpackSequence
from dis_tool import Token, disassemble


def not_implemented(m):
    raise NotImplementedError(m)


class CodeGenerator(BlockMachine):
    def __init__(self):
        self.tos = []

    def tos_push(self, ob):
        self.tos.append(ob)

    def tos_pop(self):
        return self.tos.pop()

    def generate_bytecode(self, co):
        co_tokens = disassemble(co)
        generator = CodeGenerator()
        return generator.generate_program(co_tokens)

    def generate_program(self, tokens):
        statements = self.generate_slice(tokens)
        assert len(self.tos) == 0
        return statements

    def generate_slice(self, tokens):
        """
        :param list of Token tokens: list of tokens
        """
        # re-enumerate lines
        for i in range(1, len(tokens)):
            token = tokens[i]
            token.line = token.line if token.line is not None else tokens[i - 1].line

        return self._generate_execute_statements(tokens)

    @staticmethod
    def _generate_blocks(tokens):
        """
        :param list of Token tokens: list of tokens
        """

        # сначала обработаем все "блоки", начиная с самого последнего
        block_ops = set(ALL_GENERATORS.keys())
        i = len(tokens) - 1
        while i >= 0:
            token = tokens[i]
            if isinstance(token.op, str) and token.op in block_ops:
                generator = ALL_GENERATORS[token.op]  # type: BlockFactory

                # get list of block tokens
                block_start = generator.find_start_token(tokens, i)
                block_end = generator.find_final_token(tokens, i)
                block_tokens = tokens[block_start:block_end]

                # replace block with one expression
                tokens = tokens[:block_start] + generator.generate_block(block_tokens) + tokens[block_end:]
                i = block_start
            i -= 1
        return tokens

    def _generate_execute_statements(self, tokens):
        """
        :param list of Token tokens:
        :rtype: list of StatementBase
        """
        # это будет нашей ответкой
        statements = []
        # сначала схлопнем блоки
        tokens = self._generate_blocks(tokens)

        # теперь можно пройтись виртуальной машиной
        line = 0
        i = 0
        while i < len(tokens):
            token = tokens[i]
            i += 1

            op = token.op
            line = token.line if token.line is not None else line
            # uppercase op - это железная операция
            # lowercase op - это блок
            if op.islower():
                assert isinstance(token, Block)
                block_statements = token.generate_statements(self)
                statements.extend(block_statements)
                continue

            if op == 'LOAD_CONST':
                self.tos_push(Constant(token.offset, line, token.arg))
            elif op == 'LOAD_NAME':
                self.tos_push(Reference(token.offset, line, token.arg))
            elif op == 'STORE_NAME':
                statements.append(Assign(token.offset, line, token.arg, self.tos_pop()))
            elif op == 'POP_TOP':
                last = self.tos_pop()
                if isinstance(last, StatementBase):
                    statements.append(last)
            elif op == 'BUILD_LIST':
                length = token.arg_int()
                values = [self.tos_pop() for x in range(0, length)]
                self.tos_push(List(token.offset, line, values))
            elif op == 'BUILD_SET':
                length = token.arg_int()
                values = [self.tos_pop() for x in range(0, length)]
                self.tos_push(Set(token.offset, line, values))
            elif op == 'RETURN_VALUE':
                statements.append(Returns(token.offset, line, self.tos_pop()))
            elif op == 'UNPACK_SEQUENCE':
                (i, unpack) = self.generate_execute_unpack(tokens, i - 1)
                statements.append(unpack)
            elif op == 'CALL_FUNCTION':
                argument_count = token.arg_int()
                positional_args = [self.tos_pop() for _ in range(0, argument_count & 0xFF)]
                keyword_args = [(self.tos_pop(), self.tos_pop()) for _ in range(0, (argument_count >> 8) & 0xFF)]
                function = self.tos_pop()
                self.tos_push(FunctionCall(token.offset, line, function, positional_args, keyword_args))
            else:
                not_implemented('unknown token ' + op)

        # и ответ
        return statements

    def generate_execute_unpack(self, tokens, at):
        """
        :param list of Token tokens: token list
        :param int at: position with UNPACK_SEQUENCE token
        :return: index after unpack operations and unpack statement
        :rtype: (int, UnpackSequence)
        """

        WRITE NEW UNPACK

        while at < len(tokens) and tokens[at].op == 'UNPACK_SEQUENCE':
            token = tokens[at]
            expr = self.tos_pop()
            self.tos_push(UnpackSequence(token.offset, token.line, token.arg, expr))
            at += 1
            count += token.arg if not isinstance(expr, UnpackSequence) else token.arg_int() - 1

        stores = []
        while at < len(tokens) and tokens[at].op == 'STORE_NAME' and len(stores) < count:
            stores.append(tokens[at].arg)
            at += 1

        assert len(stores) == count
        unpack = self.tos_pop()
        unpack.store(stores)

        return at, unpack
