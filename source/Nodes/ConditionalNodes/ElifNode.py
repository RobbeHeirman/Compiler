"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from Nodes.ConditionalNodes import IfNode


class ElseIfNode(IfNode.IfNode):
    label = "else if"

    def __init__(self, parent_node, ctx):
        super().__init__(parent_node, ctx)

        self.labels_needed = 2

    # LLVM Code Generation
    # ==================================================================================================================
    def generate_llvm(self, c_comment: bool = True):
        ret = self.llvm_comment("ELIF", c_comment)
        nw_br_label = self._parent_node.assign_label()
        ret += self.code_indent_string() + nw_br_label + ":\n"

        ret += IfNode.IfNode.generate_llvm(self, c_comment)
        return ret

    # Mips Code Generation
    # ==================================================================================================================
    def generate_mips(self, c_comment: bool = True):
        nw_br_label = self._parent_node.assign_label()
        ret = self.mips_comment("Else if", c_comment)
        ret += self.code_indent_string() + nw_br_label + ":\n"
        ret += super().generate_mips(c_comment)
        return ret
