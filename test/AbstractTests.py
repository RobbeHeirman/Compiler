"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
import os
import subprocess
import unittest
import sys
from inspect import stack

import main


class TracePrints(object):
    def __init__(self):
        self.stdout = sys.stdout

    def write(self, s):
        if s != '\n':
            frame_info = stack()[1]
            type(frame_info)
            self.stdout.write(f'{frame_info[1]}:{frame_info[2]}: {s}\n')

    def flush(self):
        self.stdout.flush()


sys.stdout = TracePrints()


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
        slug = filename[: -2]  # - .c
        file_name = self.path + filename
        ast = main.create_ast(file_name)
        if ast.semantic_analysis():
            code = ast.generate_llvm()
            result_file = self.result_path + filename[:-2] + ".ll"
            with open(result_file, "w+") as file:
                file.write(code)

            return True
        else:
            self.assertTrue(False, 'Semantics are wrong in an excecution test')
            return False

    def _build_and_run_llvm(self, filename, exit_code_exec):

        slug = filename[: -2]  # - .c
        exec_name = self.result_path + slug + ".exe"

        if self._compile_llvm(filename):
            code = subprocess.call(["clang", "-Wno-override-module", self.result_path + slug + ".ll", "-o", exec_name])
            self.assertEqual(code, 0, "Did not compile ll to exec")
        else:
            return

        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        ret_code = subprocess.call([exec_name], startupinfo=si)
        self.assertEqual(ret_code, exit_code_exec)


class MipsAbstractTest(unittest.TestCase):
    """
    Base for the Mips tests
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.result_path = "test/test_results/MIPS/"
        self.path = "C_files/semantic/"

    def _build_and_run_mips(self, filename, exit_code):
        if not os.path.exists(self.result_path):
            os.makedirs(self.result_path)

        slug = filename[:-2]  # -c
        file_name = self.path + filename
        ast = main.create_ast(file_name)
        if ast.semantic_analysis():
            code = ast.generate_llvm()
            result_file = self.result_path + filename[:-2] + ".asm"
            with open(result_file, "w+") as file:
                file.write(code)

            main.generate_mips(ast, self.result_path + slug)
            code = subprocess.call(['java', '-jar', "Mars.jar", self.result_path + slug + ".asm", "nc"])
            self.assertEqual(code, exit_code, "Wrong exit code")

        else:
            self.assertTrue(False, 'Semantics are wrong in an excecution test')
            return False
