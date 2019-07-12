import shutil
import os

from test.AbstractTests import SAbstractTest, LLVMAbstractTest


class STestDeclaration(SAbstractTest):
    """
    Testing the semantic analysis of declarations. Consists in multiple parts.

    1) Happy day scenario's: No errors should be generated.
    2) Wrong type initializer. (No implicit conversion yet)
    3) Re declaration of a simple type.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.result_path += "declaration/"
        self.path += "GlobalDeclaration/"

        if os.path.exists(self.result_path):
            shutil.rmtree(self.result_path)

    def test_integer_happy_day(self):
        """
        Happy day test integer init
        """
        self._run_analysis("Happy_day_int.c")

    def test_char_happy_day(self):
        self._run_analysis("happy_day_char.c")

    def test_float_happy_day(self):
        self._run_analysis("happy_day_float.c")

    def test_ptr_happy_day(self):
        self._run_analysis("happy_day_ptr.c")

    def test_wrong_type_init_int(self):
        self._run_analysis("wrong_type_init_int.c", 1, 2)

    def test_redeclaration(self):
        self._run_analysis("redeclaration_init.c", 0, 0)

    def test_redefinition(self):
        self._run_analysis("redefinition.c", 4, 2)


class LLVMTestDeclaration(LLVMAbstractTest):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result_path += "declarations/"
        self.path += "GlobalDeclaration/"

        if not os.path.exists(self.result_path):
            os.makedirs(self.result_path)

    def test_ll_happy_day_int(self):
        self._run_llvm("happy_day_int.c")

    def test_char_happy_day(self):
        self._run_llvm("happy_day_char.c")

    def test_float_happy_day(self):
        self._run_llvm("happy_day_float.c")

    def test_ptr_happy_day(self):
        self._run_llvm("happy_day_ptr.c")
