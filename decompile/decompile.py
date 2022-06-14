#!/usr/bin/env python2.7

import marshal
import dis_tool
import code_gen


def decompile_pyc(pyc_file):
    """
    Decompiles bytecode from "*.pyc" file to source code
    :param str pyc_file: path to ".pyc" file
    :rtype: str
    :return: content for ".py" file
    """
    with open(pyc_file, 'rb') as f:
        f.seek(8)
        co_bytes = marshal.load(f)
    co_tokens = dis_tool.disassemble(co_bytes)

    code_generator = code_gen.CodeGenerator()
    statements = code_generator.generate_program(co_tokens)
    return code_generator.statements_text(statements)
