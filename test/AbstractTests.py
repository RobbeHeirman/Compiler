"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
import os
import subprocess
import sys
import unittest

import main


class SAbstractTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.result_path = "test/test_results/semantic/"
        self.path = "C_files/semantic/"

    def _run_analysis(self, filename, errors=0, warnings=0):
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


# noinspection PyBroadException
class LLVMAbstractTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.result_path = "test/test_results/llvm/"
        self.path = "C_files/semantic/"

    def _run_llvm(self, filename, silence_output=True):
        file_name = self.path + filename
        ast = main.create_ast(file_name)
        if ast.semantic_analysis():
            code = ast.generate_llvm()
            result_file = self.result_path + filename[:-2] + ".ll"
            with open(result_file, "w+") as file:
                file.write(code)

            if silence_output:
                ret = subprocess.call(["clang", result_file], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            else:
                ret = subprocess.call(["clang", result_file])

            if ret == 1:
                main.generate_ast_visuals(ast, self.result_path + filename[:-2])

            # We cannot define function's at this stage of the project.
            # 1561 is the error thrown that we lack an entry point, witch is okay
            try:
                self.assertEqual(ret, 1561)

            except Exception:
                subprocess.call(["clang", "-S", "-emit-llvm", file_name])
