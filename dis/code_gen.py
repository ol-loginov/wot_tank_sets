def not_implemented(m):
    raise NotImplementedError(m)


class _Statement:
    pass


class _Named:
    def __init__(self, name=None):
        self.name = name

    def store(self, name):
        self.name = name


class _LineStatement(_Named, _Statement):
    def __init__(self, start_line=None):
        _Named.__init__(self)
        self.start_line = start_line


class ImportName(_Named):
    pass


class Import(_LineStatement):
    def __init__(self, fromlist, level, **kwargs):
        _LineStatement.__init__(self, **kwargs)
        self.fromlist = fromlist
        self.level = level
        self.imports = []

    def add_import(self, source):
        named = _Named()
        named.source = source
        self.imports.append(named)
        return named


class MakeFunction():
    def __init__(self, co):
        self.co = co


class Loop(_LineStatement):
    def __init__(self, iterator, **kwargs):
        _LineStatement.__init__(self, **kwargs)
        self.iterator = iterator


class Iterator(_LineStatement):
    def __init__(self, expression):
        _LineStatement.__init__(self)
        self.expression = expression


class Reference:
    def __init__(self, source):
        self.source = source


class Operation(_LineStatement):
    def __init__(self, action, operands):
        _LineStatement.__init__(self)
        self.action = action
        self.operands = operands


class Compare(_LineStatement):
    def __init__(self, action, operands):
        _LineStatement.__init__(self)
        self.action = action
        self.operands = operands


class CallFunction(_LineStatement):
    def __init__(self, function, positional_args, keyword_args):
        _LineStatement.__init__(self)
        self.function = function
        self.positional_args = positional_args
        self.keyword_args = keyword_args


class Assign(_LineStatement):
    def __init__(self, name, expression):
        _LineStatement.__init__(self)
        self.name = name
        self.expression = expression


class ListInstance(_LineStatement):
    def __init__(self, content):
        _LineStatement.__init__(self)
        self.content = content


class CodeGenerator:
    def __init__(self):
        self.lines = []
        self.line = 0
        self.statements = []
        self.tos = []
        self.blocks = []

    def generate(self, tokens):
        self._visit(tokens)

    def tos_push(self, ob):
        if isinstance(ob, _Statement):
            self.statement_register(ob)
        self.tos.append(ob)

    def tos_pop_list(self, count):
        return list(map(lambda x: self.tos.pop(), range(0, count)))

    def tos_pop(self):
        return self.tos.pop()

    def tos_peek(self):
        return self.tos[-1]

    def statement_register(self, statement):
        if statement not in self.statements:
            statement.start_line = self.line
            self.statements.append(statement)

    def _visit(self, tokens):
        def forget_statement_one(statement):
            if statement in self.statements:
                self.statements.remove(statement)

        def forget_statement(*args):
            for statement in args:
                forget_statement_one(statement)
            return args[0]

        def forget_statement_list(*args):
            for statement_list in args:
                for statement in statement_list:
                    forget_statement_one(statement)
            return args[0]

        def offset_index(offset, start_from=0):
            index = start_from
            while index < len(tokens):
                if tokens[index].offset == offset:
                    return index
                index += 1
            not_implemented('cannot find token for offset ' + offset)

        i = 0

        while i < len(tokens):
            token = tokens[i]
            if token.line is not None:
                self.line = token.line
            if token.op == 'LOAD_CONST':
                self.tos_push(token.arg)
            elif token.op == 'IMPORT_NAME':
                self.tos_push(Import(self.tos_pop(), self.tos_pop()))
            elif token.op == 'IMPORT_FROM':
                op = self.tos_peek().add_import(token.arg)
                self.tos_push(op)
            elif token.op == 'STORE_NAME':
                source = self.tos_pop()
                if hasattr(source, 'store'):
                    source.store(token.arg)
                else:
                    self.statement_register(Assign(token.arg, source))
            elif token.op == 'POP_TOP':
                self.tos_pop()
            elif token.op == 'BUILD_LIST':
                arg = list(map(lambda x: self.tos_pop(), range(0, token.arg)))
                forget_statement_list(arg)
                self.tos_push(ListInstance(arg))
            elif token.op == 'MAKE_FUNCTION':
                function = forget_statement(self.tos_pop())
                self.tos_push(MakeFunction(function))
            elif token.op == 'SETUP_LOOP':
                loop_end = offset_index(token.arg, i)
                loop_code = tokens[i + 1:loop_end]
                self.blocks.append(loop_code)
                self._visit(loop_code)
                i = loop_end
            elif token.op == 'GET_ITER':
                iterable = forget_statement(self.tos_pop())
                self.tos_push(Iterator(iterable))
            elif token.op == 'FOR_ITER':
                iter_end = offset_index(token.arg, i)
                iter_code = tokens[i + 1:iter_end]
                self.tos_push(self.tos_peek())
                self._visit(iter_code)
                self.tos_pop()
                i = iter_end
            elif token.op == 'LOAD_NAME':
                self.tos_push(Reference(token.arg))
            elif token.op == 'BINARY_ADD':
                self.tos_push(Operation('+', self.tos_pop_list(2)))
            elif token.op == 'CALL_FUNCTION':
                positional_args = self.tos_pop_list(token.arg & 0xFF)
                keyword_args = self.tos_pop_list((token.arg >> 8) & 0xFF)
                forget_statement_list(positional_args, keyword_args)
                func_reference = self.tos_pop()
                forget_statement(func_reference)
                self.tos_push(CallFunction(func_reference, positional_args, keyword_args))
            elif token.op == 'COMPARE_OP':
                compare_args = self.tos_pop_list(2)
                forget_statement_list(compare_args)
                self.tos_push(Compare(token.arg, compare_args))
            elif token.op == 'POP_JUMP_IF_FALSE':
                op = self.tos_pop()
            else:
                not_implemented('Unexpected op ' + token.op)

            i += 1
