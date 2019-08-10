import test.AbstractTests as AbstractTest


class LLVMConditionalTest(AbstractTest.LLVMAbstractExecTest):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path += "Conditionals/"
        self.result_path += "conditional/"

    def test_happy_day(self):
        return self._build_and_run_llvm("Fibb_simple.c", 5)


class MipsConditionalTest(AbstractTest.MipsAbstractTest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path += "Conditionals/"
        self.result_path += "conditional/"

    def test_happy_day(self):
        return self._build_and_run_mips("Fibb_simple.c", 5)
