import os
import shutil
import sys
import unittest
import main


class STestDeclaration(unittest.TestCase):
    """
    Testing the semantic analysis of declarations. Consists in multiple parts.

    1) Happy day scenario's: No errors should be generated.
    2) Wrong type initializer. (No implicit conversion yet)
    3) Re declaration of a simple type.
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.result_path = "test/test_results/semantic/declarations/"
        self.path = "C_files/semantic/Declaration/"

        if os.path.exists(self.result_path):
            shutil.rmtree(self.result_path)

    def run_analysis(self, filename, errors=0, warnings=0):
        orig_stdout = sys.stdout
        if not os.path.exists(self.result_path):
            os.makedirs(self.result_path)
        f = open(self.result_path + filename[:-2] + "_error.log", "w+")
        sys.stdout = f
        file_name = self.path + filename
        ast = main.create_ast(file_name)
        ast.semantic_analysis()
        f.close()
        sys.stdout = orig_stdout
        try:
            self.assertEqual(ast.error_count(), errors)
            self.assertEqual(ast.warning_count(), warnings)
        except Exception:
            main.generate_ast_visuals(ast, self.result_path + filename[:-2])
            raise


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

    def test_wrong_type_init_int(self):
        self.run_analysis("wrong_type_init_int.c", 0, 3)
