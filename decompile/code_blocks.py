# coding=utf-8

from code_statements import Constant, Import, StatementBase, FunctionDef, Map, For
from dis_tool import Token, token_index_at_offset, token_index_with_test


def panic(m):
    raise RuntimeError(m)


# noinspection PyClassHasNoInit
class BlockMachine:
    def tos_push(self, ob):
        """ push element to VM stack """
        panic('should override "tos_push" in ' + self.__class__.__name__)

    def tos_pop(self):
        """
        pop element from VM stack and return it
        :rtype: Any
        """
        panic('should override "tos_push" in ' + self.__class__.__name__)

    def generate_bytecode(self, co):
        """
        :param code co:
        :rtype: list of StatementBase
        """
        panic('should override "generate_block" in ' + self.__class__.__name__)

    def generate_slice(self, tokens):
        """
        :param list of Token tokens:
        :rtype: list of StatementBase
        """
        panic('should override "generate_block" in ' + self.__class__.__name__)


# noinspection PyClassHasNoInit
class Block:
    def generate_statements(self, generator):
        """
        :param BlockMachine generator: code generator to use
        :rtype: list of StatementBase
        """
        panic('should override "generate_statements" in ' + self.__class__.__name__)


class BlockFactory:
    def __init__(self): pass

    def find_start_token(self, tokens, block_start):
        """
        :param list of Token tokens: all available tokens
        :param int block_start:  index of block start token
        :rtype: int
        """
        return block_start

    def find_final_token(self, tokens, start_index):
        """
        :param list of Token tokens: all available tokens
        :param int start_index:  index of block start token
        :rtype: int
        """
        panic('should override "find_final_token" in ' + self.__class__.__name__)

    def generate_block(self, tokens):
        """
        :param list of Token tokens: block tokens
        :returns list of Token:
        :rtype: list of Token
        """
        panic('should override "generate_block" in ' + self.__class__.__name__)


class ImportBlock(Token, Block):
    def __init__(self, token, content_tokens):
        """
        :param Token token:
        :param list of Token content_tokens:
        """
        Token.__init__(self, token.offset, token.line, 'import', content_tokens)
        self.content_tokens = content_tokens

    def generate_statements(self, generator):
        statement = None
        for t in self.content_tokens:
            if t.op == 'LOAD_CONST':
                generator.tos_push(Constant(t.offset, t.line, t.arg))
            elif t.op == 'POP_TOP':
                generator.tos_pop()
            elif t.op == 'IMPORT_NAME':
                generator.tos_pop()  # fromlist
                generator.tos_pop()  # level
                statement = Import(self.offset, self.line, t.arg)
                generator.tos_push(statement)
            elif t.op == 'IMPORT_FROM':
                generator.tos_push(t.arg)
            elif t.op == 'IMPORT_STAR':
                generator.tos_pop()
                statement.add_import('*', '*')
            elif t.op == 'STORE_NAME':
                imported = generator.tos_pop()
                if isinstance(imported, str):
                    statement.add_import(imported, t.arg)
                else:
                    statement.store_name = t.arg
            else:
                panic('unknown op ' + t.op)
        return [statement]


class ImportBlockFactory(BlockFactory):
    def find_start_token(self, tokens, block_start):
        return block_start - 2

    def find_final_token(self, tokens, start_index):
        next_tokens = {'STORE_NAME', 'IMPORT_FROM', 'IMPORT_STAR'}
        end_index = start_index + 1
        end_with_pop_top = False
        while end_index < len(tokens) and tokens[end_index].op in next_tokens:
            end_with_pop_top |= tokens[end_index].op == 'IMPORT_FROM'
            end_index += 1

        if end_with_pop_top:
            assert tokens[end_index].op == 'POP_TOP'
            end_index += 1
        return end_index

    def generate_block(self, tokens):
        return [ImportBlock(tokens[0], tokens)]


class LoopBlock(Token, Block):
    def __init__(self, token, loop_block, else_block):
        """
        :param Token token:
        :param list of Token loop_block:
        :param list of Token else_block:
        """
        Token.__init__(self, token.offset, token.line, 'loop', None)
        self.loop_block = loop_block
        self.else_block = else_block

    def generate_statements(self, generator):
        looper_token = self.loop_block[-1]
        assert looper_token.op == 'JUMP_ABSOLUTE'

        body_token_start = token_index_at_offset(self.loop_block, looper_token.arg)
        head_tokens = self.loop_block[:body_token_start]
        body_tokens = self.loop_block[body_token_start:]

        if body_tokens[0].op == 'FOR_ITER':
            # это цикл for
            assert head_tokens[-1].op == 'GET_ITER'
            iterator_statements = generator.generate_slice(head_tokens[:-1])
            assert len(iterator_statements) == 0
            iterator = generator.tos_pop()

            statement = For(self.offset, self.line, iterator)
        else:
            # это цикл while
            pass

        pass


class LoopBlockFactory(BlockFactory):
    def find_final_token(self, tokens, start_index):
        return token_index_at_offset(tokens, tokens[start_index].arg)

    def generate_block(self, tokens):
        assert tokens[0].op == 'SETUP_LOOP'

        pop_block_index = token_index_with_test(tokens, lambda x: x.op == 'POP_BLOCK')
        assert pop_block_index is not None

        else_block = tokens[pop_block_index + 1:]
        loop_block = tokens[1:pop_block_index]

        return [LoopBlock(tokens[0], loop_block, else_block)]


class ClassBlock(Token, Block):
    def __init__(self, token, name):
        Token.__init__(self, token.offset, token.line, 'class', name)


class ClassBlockFactory(BlockFactory):
    def find_start_token(self, tokens, block_start):
        return block_start - 5

    def find_final_token(self, tokens, start_index):
        return start_index + 2

    def generate_block(self, tokens):
        assert tokens[-1].op == 'STORE_NAME'
        class_name = tokens[-1].arg
        return [ClassBlock(tokens[0], class_name)]


class FunctionBlock(Token, Block):
    def __init__(self, token, name, default_parameters):
        Token.__init__(self, token.offset, token.line, 'function', name)
        self.default_parameters = default_parameters
        self.name = name

    def generate_statements(self, generator):
        code_container = generator.tos_pop()
        assert code_container.value is not None

        params = self.default_parameters
        default_parameters = []
        while params > 0:
            default_parameters.append(generator.tos_pop())
            params -= 1

        body = generator.generate_bytecode(code_container.value)

        return [FunctionDef(self.offset, self.line, self.name, body)]


class FunctionBlockFactory(BlockFactory):
    def find_start_token(self, tokens, block_start):
        return block_start

    def find_final_token(self, tokens, start_index):
        return start_index + 2

    def generate_block(self, tokens):
        assert tokens[-2].op == 'MAKE_FUNCTION'
        default_parameters = tokens[-2].arg
        assert tokens[-1].op == 'STORE_NAME'
        function_name = tokens[-1].arg
        return [FunctionBlock(tokens[0], function_name, default_parameters)]


class MapBlock(Token, Block):
    def __init__(self, token, size, build_tokens):
        Token.__init__(self, token.offset, token.line, 'map', build_tokens)
        self.size = size
        self.body = build_tokens

    def generate_statements(self, generator):
        index = 0
        entries = {}
        while index < len(self.body):
            store_map_index = token_index_with_test(self.body, lambda x: x.op == 'STORE_MAP', index)
            assert store_map_index is not None

            block = self.body[index: store_map_index]
            generator.generate_slice(block)

            key = generator.tos_pop()
            value = generator.tos_pop()
            entries[key] = value

            index = store_map_index + 1

        assert len(entries) == self.size
        generator.tos_push(Map(self.offset, self.line, entries))

        return []


class MapBlockFactory(BlockFactory):
    def find_final_token(self, tokens, start_index):
        build_map_token = tokens[start_index]

        assert isinstance(build_map_token.arg, int)
        build_map_count = build_map_token.arg

        while build_map_count > 0:
            if tokens[start_index].op == 'STORE_MAP':
                build_map_count -= 1
            start_index += 1
        return start_index

    def generate_block(self, tokens):
        build_map = tokens[0]
        assert build_map.op == 'BUILD_MAP'
        return [MapBlock(tokens[0], build_map.arg, tokens[1:])]


ALL_GENERATORS = {
    "SETUP_LOOP": LoopBlockFactory(),
    "IMPORT_NAME": ImportBlockFactory(),
    "BUILD_CLASS": ClassBlockFactory(),
    "MAKE_FUNCTION": FunctionBlockFactory(),
    "BUILD_MAP": MapBlockFactory()
}
