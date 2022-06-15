TAB = "\t"
BLOCK_START = ': '
STATEMENT_DELIMITER = '; '


def panic(m):
    raise RuntimeError(m)


def empty(iterable):
    return len(iterable) == 0


def join_delim(index, delimiter):
    return '' if index == 0 else delimiter


def endswith(string, tail):
    """
    :param str string:
    :param str tail:
    :rtype: bool
    """
    return string[-len(tail):] == tail


class CodeMerge():
    def __init__(self, line_indent='', join_delimiter=''):
        """
        :param str line_indent: indent new line
        :param str join_delimiter: delimiter between existing text in line
        """
        self.line_indent = line_indent
        self.join_delimiter = join_delimiter

    @staticmethod
    def comma(i):
        return CodeMerge() if i == 0 else CodeMerge(join_delimiter=', ')

    @staticmethod
    def comma_tab(i):
        return CodeMerge(line_indent=TAB) if i == 0 else CodeMerge(join_delimiter=', ', line_indent=TAB)

    @staticmethod
    def semicolon(i):
        return CodeMerge() if i == 0 else CodeMerge(join_delimiter='; ')

    @staticmethod
    def semicolon_tab(i):
        return CodeMerge(line_indent=TAB) if i == 0 else CodeMerge(join_delimiter='; ', line_indent=TAB)

    @staticmethod
    def tab():
        return CodeMerge(line_indent=TAB)


class CodeWriter():
    def __init__(self, line_base=0, expression=None):
        """
        :param int line_base:
        :param str|None expression:
        """
        self.line_base = line_base
        self.lines = [expression] if expression is not None else []

    def text(self, offset=1):
        def clean(string):
            """
            :param str string:
            :rtype: str
            """
            return string.rstrip()

        lines = self.lines[offset:]
        lines = list(map(lambda x: clean(x), lines))
        return "\n".join(lines)

    def _append(self, line, text, delimiter='; '):
        if line == len(self.lines) - 1:
            self.lines[line] += delimiter + text
        else:
            self.lines.append(text)

    def _ensure_line(self, line):
        while len(self.lines) < line:
            self.lines.append('')

    def prepend_first(self, prefix):
        """
        :rtype: CodeWriter
        """
        assert not empty(self.lines)
        self.lines[0] = prefix + self.lines[0]
        return self

    def append_last(self, suffix):
        """
        :rtype: CodeWriter
        """
        assert not empty(self.lines)
        self.lines[-1] += suffix
        return self

    def add_statement(self, line, statement):
        """
        :rtype: CodeWriter
        """
        assert isinstance(statement, str)

        line -= self.line_base
        self._ensure_line(line)
        self._append(line, statement)
        return self

    def add_writer(self, writer, merge_options=CodeMerge()):
        """
        :param CodeWriter writer:
        :param CodeMerge merge_options: indent new line
        :rtype: CodeWriter
        """
        join_delimiter = merge_options.join_delimiter
        line_indent = merge_options.line_indent

        for i in range(0, len(writer.lines)):
            body_line_index = writer.line_base + i - self.line_base
            body_line = writer.lines[i]
            self._ensure_line(body_line_index)
            if body_line_index == len(self.lines) - 1:
                candidate = self.lines[body_line_index]
                if endswith(candidate, BLOCK_START):
                    candidate += body_line
                else:
                    candidate = candidate + join_delimiter + body_line
                self.lines[body_line_index] = candidate
            else:
                self.lines.append(line_indent + body_line)
        return self


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

    def write(self):
        """
        :return: writer with content
        :rtype: CodeWriter
        """
        raise NotImplementedError('should implement "write" in ' + self.__class__.__name__)


class StoreReceiver:
    def __init__(self):
        pass

    def store(self, name):
        raise NotImplementedError('should implement "write" in ' + self.__class__.__name__)


class Pass(StatementBase):
    def __init__(self, offset, line):
        StatementBase.__init__(self, offset, line, 'pass')

    def write(self):
        return CodeWriter(self.line, 'pass')


class Constant(StatementBase):
    def __init__(self, offset, line, arg):
        StatementBase.__init__(self, offset, line, 'constant')
        self.value = arg

    def write(self):
        return CodeWriter(self.line, str(self.value))


class List(StatementBase):
    def __init__(self, offset, line, values):
        """
        :param int offset:
        :param int line:
        :param list of StatementBase values:
        """
        StatementBase.__init__(self, offset, line, 'list')
        self.values = values

    def write(self):
        code = CodeWriter(self.line, '[')

        for i, value in enumerate(self.values):
            code.add_writer(value.write(), CodeMerge.comma(i))
        return code.append_last(']')


class Tuple(StatementBase):
    def __init__(self, offset, line, values):
        """
        :param int offset:
        :param int line:
        :param list of StatementBase values:
        """
        StatementBase.__init__(self, offset, line, 'tuple')
        self.values = values

    def write(self):
        body = CodeWriter(self.line, '(')
        for i, expr in enumerate(self.values):
            body.add_writer(expr.write(), CodeMerge.comma_tab(i))
        body.append_last(')')
        return body


class Set(StatementBase):
    def __init__(self, offset, line, values):
        StatementBase.__init__(self, offset, line, 'set')
        self.values = values

    def write(self):
        body = CodeWriter(self.line, '{')
        for i, expr in enumerate(self.values):
            body.add_writer(expr.write(), CodeMerge.comma_tab(i))
            body.append_last('}')
        return body


class Map(StatementBase):
    def __init__(self, offset, line, entries):
        StatementBase.__init__(self, offset, line, 'map')
        self.entries = entries


class Reference(StatementBase):
    def __init__(self, offset, line, ref):
        StatementBase.__init__(self, offset, line, 'reference')
        self.ref = ref

    def write(self):
        return CodeWriter(self.line, self.ref)


class Assign(StatementBase):
    def __init__(self, offset, line, l_expr, r_expr):
        """
        :param int offset:
        :param int line:
        :param StatementBase l_expr:
        :param StatementBase r_expr:
        """
        StatementBase.__init__(self, offset, line, 'assign')
        self.l_expr = l_expr
        self.r_expr = r_expr
        self.operator = ' = '

    def write(self):
        code = CodeWriter(self.line)
        code.add_writer(self.l_expr.write())
        code.append_last(self.operator)
        code.add_writer(self.r_expr.write())
        return code


class Returns(StatementBase):
    def __init__(self, offset, line, expr):
        """
        :param int offset:
        :param int line:
        :param StatementBase expr:
        """
        StatementBase.__init__(self, offset, line, 'return')
        self.expr = expr

    def write(self):
        body = CodeWriter(self.line, 'return ')
        body.add_writer(self.expr.write(), CodeMerge.tab())
        return body


class FunctionCall(StatementBase):
    def __init__(self, offset, line, function, positional_args, keyword_args):
        """
        :param int offset:
        :param int line:
        :param StatementBase function:
        :param list of StatementBase positional_args:
        :param list of (str, StatementBase) keyword_args:
        """
        StatementBase.__init__(self, offset, line, 'func_call')
        self.function = function
        self.positional_args = positional_args
        self.keyword_args = keyword_args

    def write(self):
        body = CodeWriter(self.line)
        body.add_writer(self.function.write())

        parameters = []
        for a in self.positional_args:
            parameters.append(a.write())
        for k in self.keyword_args:
            parameters.append(k[1].write().prepend_first(k[0] + ' ='))

        body.append_last('(')
        for i, parameter in enumerate(parameters):
            body.add_writer(parameter, CodeMerge.comma_tab(i))
        body.append_last(')')

        return body


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

    def write(self):
        def _import_string(import_pair):
            if import_pair[0] == import_pair[1]:
                return import_pair[0]
            return import_pair[0] + ' as ' + import_pair[1]

        names = ', '.join(self.names)
        imports = ', '.join(map(lambda x: _import_string(x), self.imports))

        writer = CodeWriter(self.line)
        if len(imports) == 0:
            writer.add_statement(self.line, 'import %s' % names)
        else:
            writer.add_statement(self.line, 'from %s import %s' % (names, imports))
        return writer


class FunctionDef(StatementBase):
    def __init__(self, offset, line, name, statements):
        """
        :param str name:  function name
        :param list of StatementBase statements:
        """
        StatementBase.__init__(self, offset, line, 'funcdef')
        self.name = name
        self.statements = statements

    def write(self):
        writer = CodeWriter(self.line)

        head = "def %s(): " % (self.name,)
        writer.add_statement(self.line, head)

        for i, body_statement in enumerate(self.statements):
            writer.add_writer(body_statement.write(), CodeMerge.semicolon_tab(i))

        return writer


class For(StatementBase):
    def __init__(self, offset, line, iterator_expr, body_statements):
        """
        :param int offset:
        :param int line:
        :param StatementBase iterator_expr:
        :param list of StatementBase body_statements:
        """
        StatementBase.__init__(self, offset, line, 'for')

        if isinstance(iterator_expr, Assign) or isinstance(iterator_expr, UnpackOperation):
            iterator_expr.operator = ' in '
        else:
            panic('invalid assign expression, expect Assign or Unpack, got ' + iterator_expr.__class__.__name__)

        self.iterator_expr = iterator_expr
        self.body_statements = body_statements

    def write(self):
        code = CodeWriter(self.line, 'for ')
        code.add_writer(self.iterator_expr.write(), CodeMerge.tab())
        code.append_last(': ')

        for i, statement in enumerate(self.body_statements):
            code.add_writer(statement.write(), CodeMerge.semicolon_tab(i))

        return code


class UnpackOperation(StatementBase):
    def __init__(self, offset, line, expr):
        StatementBase.__init__(self, offset, line, 'unpack')
        self.expr = expr
        self.assigns = []
        self.assign_delimiter = ' = '

    def create_receivers(self, count):
        return [UnpackReceiver(self, 0) for i in range(0, count)]

    def add_assign(self, name, depth):
        def add_to_list(tpl, current_depth):
            if current_depth == depth:
                return tpl + [name]

            if empty(tpl) or not isinstance(tpl[-1], list):
                tpl.append([])
            tpl[-1] = add_to_list(tpl[-1], current_depth + 1)
            return tpl

        self.assigns = add_to_list(self.assigns, 0)

    def write(self):
        def render_tuple(tpl):
            out = ''
            for t in tpl:
                append = t if not isinstance(t, list) else render_tuple(t)
                out += ', ' + append
            return '(' + out[2:] + ')'

        writer = CodeWriter(self.line, render_tuple(self.assigns) + self.assign_delimiter)
        writer.add_writer(self.expr.write(), CodeMerge.tab())
        return writer


class UnpackReceiver(StoreReceiver):
    def __init__(self, target, depth):
        StoreReceiver.__init__(self)
        self.target = target
        self.depth = depth

    def get_unpack(self):
        """
        :rtype: UnpackOperation
        """
        if isinstance(self.target, UnpackOperation): return self.target
        if isinstance(self.target, UnpackReceiver): return self.target.get_unpack()
        panic("unpack is not available")

    def store(self, name):
        self.get_unpack().add_assign(name, self.depth)

    def create_receivers(self, count):
        return [UnpackReceiver(self, self.depth + 1) for i in range(0, count)]
