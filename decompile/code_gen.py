# coding=utf-8

from code_blocks import Block, BlockFactory, BlockMachine, ALL_GENERATORS
from code_statements import Import, Constant, Reference, Assign, FunctionCall, Returns, StatementBase, List, Set, CodeWriter, Tuple, UnpackOperation, UnpackReceiver, StoreReceiver, CodeMerge
from dis_tool import Token, disassemble


def not_implemented(m):
    raise NotImplementedError(m)


def panic(m):
    raise RuntimeError(m)


class CodeGenerator(BlockMachine):
    def __init__(self):
        self.tos = []

    def tos_push(self, ob):
        self.tos.append(ob)

    def tos_peek(self):
        return self.tos[-1]

    def tos_push_all(self, ob_list):
        self.tos.extend(ob_list)

    def tos_pop(self):
        assert len(self.tos) > 0
        return self.tos.pop()

    def generate_bytecode(self, co):
        co_tokens = disassemble(co)
        generator = CodeGenerator()
        return generator.generate_program(co_tokens, ignore_last_return=False)

    def generate_program(self, tokens, ignore_last_return=True):
        statements = self.generate_slice(tokens)
        assert len(self.tos) == 0
        if ignore_last_return and len(statements) > 0 and isinstance(statements[-1], Returns):
            statements = statements[:-1]
        statements = simplify_statements(statements)
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

        def op_store_name(t):
            rexp = self.tos_pop()
            if isinstance(rexp, StoreReceiver):
                rexp.store(t.arg)
            else:
                statements.append(Assign(t.offset, line, Reference(t.offset, line, t.arg), rexp))

        def op_pop_top(_):
            last = self.tos_pop()
            if isinstance(last, StatementBase):
                statements.append(last)

        def op_build_list(t):
            length = t.arg_int()
            values = [self.tos_pop() for x in range(0, length)]
            values.reverse()
            self.tos_push(List(t.offset, line, values))

        def op_build_tuple(t):
            length = t.arg_int()
            values = [self.tos_pop() for _ in range(0, length)]
            values.reverse()
            self.tos_push(Tuple(t.offset, line, values))

        def op_build_set(t):
            length = t.arg_int()
            values = [self.tos_pop() for x in range(0, length)]
            values.reverse()
            self.tos_push(Set(t.offset, line, values))

        def op_unpack_sequence(t):
            source = self.tos_pop()
            if isinstance(source, UnpackReceiver):
                unpack = source
            else:
                unpack = UnpackOperation(i, line, source)
                statements.append(unpack)
            self.tos_push_all(unpack.create_receivers(t.arg_int()))

        def op_call_function(t):
            argument_count = t.arg_int()
            positional_args = [self.tos_pop() for _ in range(0, argument_count & 0xFF)]
            keyword_args = [(self.tos_pop(), self.tos_pop()) for _ in range(0, (argument_count >> 8) & 0xFF)]
            function = self.tos_pop()
            self.tos_push(FunctionCall(t.offset, line, function, positional_args, keyword_args))

        def op_rot_three(t):
            [a, b, c] = [self.tos_pop(), self.tos_pop(), self.tos_pop()]
            self.tos_push_all([a, c, b])

        def op_rot_two(t):
            [a, b] = [self.tos_pop(), self.tos_pop()]
            self.tos_push_all([a, b])

        op_processors = {
            'LOAD_CONST': lambda t: self.tos_push(Constant(t.offset, line, t.arg)),
            'LOAD_GLOBAL': lambda t: self.tos_push(Reference(t.offset, line, t.arg)),
            'LOAD_NAME': lambda t: self.tos_push(Reference(t.offset, line, t.arg)),
            'STORE_NAME': op_store_name,
            'POP_TOP': op_pop_top,
            'BUILD_LIST': op_build_list,
            'BUILD_TUPLE': op_build_tuple,
            'BUILD_SET': op_build_set,
            'RETURN_VALUE': lambda t: statements.append(Returns(t.offset, line, self.tos_pop())),
            'UNPACK_SEQUENCE': op_unpack_sequence,
            'CALL_FUNCTION': op_call_function,
            'ROT_THREE': op_rot_three,
            'ROT_TWO': op_rot_two,
        }

        try:
            while i < len(tokens):
                token = tokens[i]
                i += 1

                op = token.op
                line = token.line if token.line is not None else line
                # uppercase op - это операция bytecode
                # lowercase op - это операция блока
                if op.islower():
                    assert isinstance(token, Block)
                    block_statements = token.generate_statements(self)
                    statements.extend(block_statements)
                    continue

                if op not in op_processors:
                    not_implemented('unknown token ' + op)

                op_processors[op](token)
        except Exception as error:
            error.args = error.args + ({'line': line, 'bytecode_offset': i},)
            raise

            # и ответ
        return statements

    @staticmethod
    def statements_text(statements):
        """
        :param list of StatementBase statements: statements to render
        :rtype: str
        """
        writer = CodeWriter()
        for i, statement in enumerate(statements):
            writer.add_writer(statement.write(), CodeMerge.semicolon(i))

        return writer.text()


def simplify_statements(statements):
    def cast(o, clazz):
        return isinstance(o, clazz)

    ## multiple import might be joined if imports without specification
    i = 0
    while i < len(statements):
        a = statements[i]
        if cast(a, Import) and i < len(statements) - 1:
            b = statements[i + 1]
            if cast(b, Import) and a.imports_all() and b.imports_all() and a.line == b.line:
                a.add_names(b.names)
                statements.remove(b)
        i += 1
    return statements
