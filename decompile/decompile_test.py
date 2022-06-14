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
        expected = read_file(os.path.join(test_folder, str(id) + '.txt'))
        self.assertEqual(actual, expected)

    def test_000(self): self.run_single_test('000-import')

    def test_001(self): self.run_single_test('001-def')

    def test_999(self): self.run_single_test('999-all')


if __name__ == '__main__':
    unittest.main()
