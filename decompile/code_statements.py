class StatementWriter():
    def __init__(self, line_offset=0):
        self.lines = []
        self.indent = 0
        self.line_offset = line_offset

    def text(self):
        """
        :rtype: unicode
        """
        return "\n".join(self.lines[1:])

    def _indent_text(self):
        return "\t" * self.indent

    def write_line(self, line, text, delimiter='; '):
        line += self.line_offset
        while len(self.lines) < line:
            self.lines.append(self._indent_text())
        if len(self.lines) > line:
            self.lines[line] += delimiter + text
        else:
            self.lines.append(self._indent_text() + text)

    def enter_block(self):
        self.indent += 1

    def leave_block(self):
        self.indent -= 1
        assert self.indent >= 0

    @staticmethod
    def write_statement(statement):
        """
        :param StatementBase statement:
        """
        writer = StatementWriter(line_offset=1 - statement.line)
        statement.write(writer)
        return writer.text()


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

    def write(self, writer):
        """
        :param StatementWriter writer: writer to write lines
        """
        raise NotImplementedError('should implement "write" in ' + self.__class__.__name__)


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

    def write(self, writer):
        """ :param StatementWriter writer: """
        writer.write_line(self.line, self.ref)


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
        """
        :param int offset:
        :param int line:
        :param StatementBase function:
        :param list of StatementBase positional_args:
        :param (str, StatementBase) keyword_args:
        """
        StatementBase.__init__(self, offset, line, 'func_call')
        self.function = function
        self.positional_args = positional_args
        self.keyword_args = keyword_args

    def write(self, writer):
        """ :param StatementWriter writer: """
        callee = StatementWriter.write_statement(self.function)
        writer.write_line(self.line, callee + '(' + ')')


class Import(StatementBase):
    def __init__(self, offset, line, name):
        StatementBase.__init__(self, offset, line, 'import')
        self.names = [name]
        self.imports = []

    def add_names(self, names):
        self.names.extend(names)

    def add_import(self, name, store_name):
        self.imports.append((name, store_name))

    def imports_all(self):
        return len(self.imports) == 0

    def _import_string(self, import_pair):
        if import_pair[0] == import_pair[1]:
            return import_pair[0]
        return import_pair[0] + ' as ' + import_pair[1]

    def write(self, writer):
        """ :param StatementWriter writer:  """
        names = ', '.join(self.names)
        imports = ', '.join(map(lambda x: self._import_string(x), self.imports))
        if len(imports) == 0:
            writer.write_line(self.line, 'import %s' % names)
        else:
            writer.write_line(self.line, 'from %s import %s' % (names, imports))


class FunctionDef(StatementBase):
    def __init__(self, offset, line, name, statements):
        """
        :param str name:  function name
        :param list of StatementBase statements:
        """
        StatementBase.__init__(self, offset, line, 'funcdef')
        self.name = name
        self.statements = statements

    def write(self, writer):
        """ :param StatementWriter writer:  """
        writer.write_line(self.line, 'def ' + self.name + '(' + '):')
        writer.enter_block()
        for s in self.statements:
            s.write(writer)
        else:
            writer.write_line(self.line, 'pass', delimiter=' ')
        writer.leave_block()


class For(StatementBase):
    def __init__(self, offset, line, iterator_expr):
        StatementBase.__init__(self, offset, line, 'for')
        self.iterator_expr = iterator_expr
