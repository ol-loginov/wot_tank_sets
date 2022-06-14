#!/usr/bin/env python2.7

import dis, sys
import marshal
import dis_tool
import code_gen

input_file = sys.argv[1]


def uncompile_file(pyc_file):
    with open(pyc_file, 'rb') as f:
        f.seek(8)
        co_bytes = marshal.load(f)
    co_tokens = dis_tool.disassemble(co_bytes)

    code_generator = code_gen.CodeGenerator()
    statements = code_generator.generate_program(co_tokens)
    for l in statements:
        print l


uncompile_file(input_file)
