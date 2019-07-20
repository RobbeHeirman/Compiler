"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
import os
import subprocess
import traceback
import unittest

import main


# class TracePrints(object):
#   def __init__(self):
#     self.stdout = sys.stdout
#   def write(self, s):
#     self.stdout.write("Writing %r\n" % s)
#     traceback.print_stack(file=self.stdout)
#
# sys.stdout = TracePrints()

class SAbstractTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.result_path = "test/test_results/semantic/"
        self.path = "C_files/semantic/"

    def _run_analysis(self, filename, errors=0, warnings=0):
        if not os.path.exists(self.result_path):
            os.makedirs(self.result_path)
        f = open(self.result_path + filename[:-2] + "_error.log", "w+")
        file_name = self.path + filename
        ast = main.create_ast(file_name, f)
        ast.semantic_analysis()
        f.close()
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


class LLVMAbstractExecTest(LLVMAbstractTest):

    def _compile_llvm(self, filename):
        file_name = self.path + filename
        ast = main.create_ast(file_name)
        if ast.semantic_analysis():
            code = ast.generate_llvm()
            result_file = self.result_path + filename[:-2] + ".ll"
            with open(result_file, "w+") as file:
                file.write(code)

            ret = subprocess.call(["clang", "-S", "-emit-llvm", file_name])
            # Should compile with exit code 0
            self.assertEqual(ret, 0)
            return True if ret is 0 else False

    def _build_and_run_llvm(self, filename, exit_code_exec):

        slug = filename[: -2]  # - .c
        exec_name = self.result_path + slug + ".exe"

        if self._compile_llvm(filename):
            subprocess.call(["clang", "-Wno-override-module", self.result_path + slug + ".ll", "-o", exec_name])
        else:
            return

        ret_code = subprocess.call([exec_name])
        self.assertEqual(ret_code, exit_code_exec)
