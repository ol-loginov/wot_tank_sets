class StatementBase:
    def __init__(self, offset, line, label):
        self.offset = offset
        self.label = label
        self.line = line

    def __str__(self):
        return '[%s:%d] %s' % (self.line, self.offset, self.describe())

    def describe(self):
        """ get textual debug string """
        return self.label


class Constant(StatementBase):
    def __init__(self, offset, line, arg):
        StatementBase.__init__(self, offset, line, 'constant')
        self.value = arg


class List(StatementBase):
    def __init__(self, offset, line, values):
        StatementBase.__init__(self, offset, line, 'list')
        self.values = values


class Set(StatementBase):
    def __init__(self, offset, line, values):
        StatementBase.__init__(self, offset, line, 'set')
        self.values = values


class Map(StatementBase):
    def __init__(self, offset, line, entries):
        StatementBase.__init__(self, offset, line, 'map')
        self.entries = entries


class Reference(StatementBase):
    def __init__(self, offset, line, ref):
        StatementBase.__init__(self, offset, line, 'reference')
        self.ref = ref


class Assign(StatementBase):
    def __init__(self, offset, line, name, expr):
        StatementBase.__init__(self, offset, line, 'assign')
        self.name = name
        self.expr = expr


class Returns(StatementBase):
    def __init__(self, offset, line, expr):
        StatementBase.__init__(self, offset, line, 'return')
        self.expr = expr


class FunctionCall(StatementBase):
    def __init__(self, offset, line, function, positional_args, keyword_args):
        StatementBase.__init__(self, offset, line, 'func_call')
        self.function = function
        self.positional_args = positional_args
        self.keyword_args = keyword_args


class ImportStatement(StatementBase):
    def __init__(self, offset, line, name):
        StatementBase.__init__(self, offset, line, 'import')
        self.name = name
        self.imports = []

    def add_import(self, name, store_name):
        self.imports.append((name, store_name))


class FunctionDef(StatementBase):
    def __init__(self, offset, line, name, statements):
        StatementBase.__init__(self, offset, line, 'funcdef')
        self.name = name
        self.statements = statements


class UnpackSequence(StatementBase):
    def __init__(self, offset, line, count, expr):
        StatementBase.__init__(self, offset, line, 'unpack')
        self.count = count
        self.expr = expr
        self.stores = None

    def store(self, stores):
        self.stores = stores


class For(StatementBase):
    def __init__(self, offset, line, iterator_expr):
        StatementBase.__init__(self, offset, line, 'for')
        self.iterator_expr = iterator_expr
