import os
import unittest

from decompile import decompile_pyc
from py_compile import compile

test_folder = os.path.join(os.path.dirname(__file__), 'tests')


def read_file(path):
    with open(os.path.join(path), 'r') as f:
        return f.read()


class TestDecompile(unittest.TestCase):
    def run_single_test(self, id):
        source = os.path.join(test_folder, id + '.py')
        target = os.path.join(test_folder, id + '.pyc')
        if os.path.exists(target):
            os.remove(target)
        compile(source, doraise=True)

        actual = decompile_pyc(target)
        actual = actual.replace("\r", "")
        expected = read_file(os.path.join(test_folder, str(id) + '.txt'))
        expected = expected.replace("\r", "")
        self.assertEqual(expected, actual)

    def test_import_000(self): self.run_single_test('import-000')

    def test_def_001(self): self.run_single_test('def-001')

    def test_def_002(self): self.run_single_test('def-002')

    def test_def_003(self): self.run_single_test('def-003')

    def test_def_004(self): self.run_single_test('def-004')

    def test_unpack_001(self): self.run_single_test('unpack-001')

    def test_unpack_002(self): self.run_single_test('unpack-002')

    def test_for_001(self): self.run_single_test('for-001')

    def test_for_002(self): self.run_single_test('for-002')

    def test_999(self): self.run_single_test('999')


if __name__ == '__main__':
    unittest.main()
