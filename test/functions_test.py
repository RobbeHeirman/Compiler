"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
import os

from test.AbstractTests import SAbstractTest, LLVMAbstractExecTest, MipsAbstractTest


class SFunctionTest(SAbstractTest):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path += "Function/"
        self.result_path += "function/"

    def test_main_happy_day(self):
        self._run_analysis("main_happy_day.c")

    def test_happy_day_regres(self):
        return self._run_analysis("happy_day_regres.c")

    def test_redeclaration_func(self):
        return self._run_analysis("redeclaration_func.c", errors=1)

    def test_redefinition(self):
        return self._run_analysis("redefinition.c", 1, 0)

    def test_return_conflict(self):
        return self._run_analysis("return_conflict.c", 1)

    def test_signature_call(self):
        return self._run_analysis("signature_call_conflict.c", 2)

    def test_call_non_function(self):
        return self._run_analysis('call_non_function.c', 1)


class LLVMFunctionTest(LLVMAbstractExecTest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path += "Function/"
        self.result_path += "function/"

        if not os.path.exists(self.result_path):
            os.makedirs(self.result_path)

    def test_main_happy_day_llvm(self):
        return self._build_and_run_llvm("main_happy_day.c", 0)

    def test_return_constant(self):
        return self._build_and_run_llvm("return_constant.c", 42)

    def test_return_variable(self):
        return self._build_and_run_llvm("return_variable.c", 44)

    def test_return_stored_variable(self):
        return self._build_and_run_llvm("return_stored_var.c", 48)

    def test_call_with_constant(self):
        return self._build_and_run_llvm("call_with_constants.c", 91)

    def test_call_with_variables(self):
        return self._build_and_run_llvm("call_with_variables.c", 80)

    def test_mixed_calls(self):
        return self._build_and_run_llvm("call_mixed.c", 88)

    def test_main_happy_day_regres_llvm(self):
        return self._build_and_run_llvm("happy_day_regres.c", 44)


class MipsFunctionTest(MipsAbstractTest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path += "Function/"
        self.result_path += "function/"

    def test_main_happy_day(self):
        return self._build_and_run_mips("main_happy_day.c", 0)

    def test_return_constant(self):
        return self._build_and_run_mips("return_constant.c", 42)

    def test_return_variable(self):
        return self._build_and_run_mips("return_variable.c", 44)

    def test_return_stored_variable(self):
        return self._build_and_run_mips("return_stored_var.c", 48)

    def test_call_with_constant(self):
        return self._build_and_run_mips("call_with_constants.c", 91)

    def test_call_with_variables(self):
        return self._build_and_run_mips("call_with_variables.c", 80)

    def test_mixed_calls(self):
        return self._build_and_run_mips("call_mixed.c", 88)

    def test_main_happy_day_regres(self):
        return self._build_and_run_mips("happy_day_regres.c", 44)
