import unittest
import main


class STestDeclaration(unittest.TestCase):

    def setUp(self):
        self.path = "C_files/semantic/Declaration/"

    def run_analysis(self, filename):
        file_name = self.path + filename
        ast = main.create_ast(file_name)
        self.assertTrue(ast.semantic_analysis())

    def test_integer_happy_day(self):
        """
        Happy day test integer init
        """
        self.run_analysis("Happy_day_int.c")

    def test_char_happy_day(self):
        self.run_analysis("happy_day_char.c")

    def test_float_happy_day(self):
        self.run_analysis("happy_day_float.c")

    def test_ptr_happy_day(self):
        self.run_analysis("happy_day_ptr.c")
