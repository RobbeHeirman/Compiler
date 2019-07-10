import subprocess
import shutil
import sys
import unittest
import main
import os


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
        self.run_analysis("wrong_type_init_int.c", 1, 3)


class LLVMTestDeclaration(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result_path = "test/test_results/llvm/declarations/"
        self.path = "C_files/semantic/Declaration/"

        if not os.path.exists(self.result_path):
            os.makedirs(self.result_path)

    def _run_llvm(self, filename):
        file_name = self.path + filename
        ast = main.create_ast(file_name)
        if ast.semantic_analysis():
            code = ast.generate_llvm()
            result_file = self.result_path + filename[:-2] + ".ll"
            with open(result_file, "w+") as file:
                file.write(code)

            ret = subprocess.call(["clang", result_file])

            if ret == 1:
                main.generate_ast_visuals(ast, self.result_path + filename[:-2])

            self.assertEqual(ret, 0)

    def test_ll_happy_day_int(self):
        self._run_llvm("happy_day_int.c")
