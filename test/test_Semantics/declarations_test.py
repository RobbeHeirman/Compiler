import unittest
import main


class STestDeclaration(unittest.TestCase):

    def setUp(self):
        self.path = "C_files/semantic/Declaration/"

    def test_integer_happy_day(self):
        """
        Happy day test integer init
        :return:
        """

        file_name = self.path + "Happy_day_int.c"
        ast = main.create_ast(file_name)
        self.assertTrue(ast.semantic_analysis())
