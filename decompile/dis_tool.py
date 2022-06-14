import dis


def panic(m):
    raise RuntimeError(m)


def token_index_at_offset(tokens, offset):
    for i in range(0, len(tokens)):
        if tokens[i].offset == offset:
            return i
    panic("cannot find token at offset " + str(offset))


def token_index_with_test(tokens, test, from_index=0):
    for i in range(from_index, len(tokens)):
        if test(tokens[i]):
            return i
    return None


def disassemble(co):
    out = []

    def receiver(token):
        out.append(token)

    _disassemble(co, receiver=receiver)
    return out


class Token:
    def __init__(self, offset, line, op, arg):
        """
        :param int offset:
        :param int|None line:
        :param str op:
        :param object arg:
        """
        self.offset = offset
        self.line = line
        self.op = op
        self.arg = arg

    def __str__(self):
        return '%s [%s]: %s %s' % (self.offset, self.line, self.op, self.arg)

    def arg_int(self):
        """
        :rtype: int
        """
        assert isinstance(self.arg, int)
        return self.arg


def _disassemble(co, receiver, lasti=-1):
    """Disassemble a code object."""
    code = co.co_code
    labels = dis.findlabels(code)
    linestarts = dict(dis.findlinestarts(co))
    n = len(code)
    i = 0
    extended_arg = 0
    free = None
    while i < n:
        c = code[i]
        op = ord(c)

        op_offset = i
        op_line = linestarts[i] if i in linestarts else None

        if i in linestarts:
            if i > 0:
                print
            print "%3d" % op_line,
        else:
            print '   ',

        if i == lasti:
            print '-->',
        else:
            print '   ',

        if i in labels:
            print '>>',
        else:
            print '  ',

        op_code = repr(i)
        print op_code.rjust(4),

        op_name = dis.opname[op]
        print op_name.ljust(20),

        op_arg = None
        i += 1
        if op >= dis.HAVE_ARGUMENT:
            op_arg = ord(code[i]) + ord(code[i + 1]) * 256 + extended_arg
            extended_arg = 0
            i = i + 2
            if op == dis.EXTENDED_ARG:
                extended_arg = op_arg * 65536L
            print repr(op_arg).rjust(5),
            if op in dis.hasconst:
                op_arg = co.co_consts[op_arg]
                print '(' + repr(op_arg) + ')',
            elif op in dis.hasname:
                op_arg = co.co_names[op_arg]
                print '(' + op_arg + ')',
            elif op in dis.hasjrel:
                op_arg = i + op_arg
                print '(to ' + repr(op_arg) + ')',
            elif op in dis.haslocal:
                op_arg = co.co_varnames[op_arg]
                print '(' + op_arg + ')',
            elif op in dis.hascompare:
                op_arg = dis.cmp_op[op_arg]
                print '(' + op_arg + ')',
            elif op in dis.hasfree:
                if free is None:
                    free = co.co_cellvars + co.co_freevars
                op_arg = free[op_arg]
                print '(' + op_arg + ')',
        print

        receiver(Token(op_offset, op_line, op_name, op_arg))
