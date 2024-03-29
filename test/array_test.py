"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
import test.AbstractTests as AbstractTest


class SArrayTest(AbstractTest.SAbstractTest):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path += "Array/"
        self.result_path += "array/"

    def test_happy_day(self):
        return self._run_analysis("happy_day.c")

    def test_non_integer(self):
        return self._run_analysis('non_integer_init.c', 3)

    def test_subscript_non_array(self):
        return self._run_analysis("subscript_non_array.c", 2)

    def test_subscript_no_expression(self):
        return self._run_analysis("subs_n_expr.c", 1)

    def test_expr_sub_not_int(self):
        return self._run_analysis('expr_sub_not_int.c', 2)

# class LLVMWhileTest(AbstractTest.LLVMAbstractExecTest):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.path += "Array/"
#         self.result_path += "array/"
#
#     def test_happy_day(self):
#         return self._build_and_run_llvm("happy_day.c", 5)
#
#
# class MipsConditionalTest(AbstractTest.MipsAbstractTest):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.path += "while/"
#         self.result_path += "while/"
#
#     def test_happy_day(self):
#         return self._build_and_run_mips("happy_day.c", 5)
