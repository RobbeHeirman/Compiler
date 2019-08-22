"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from Nodes.AbstractNodes.ScopedNode import ScopedNode


class ForLoopNode(ScopedNode):
    label = "for"

    # Built-ins
    # ==================================================================================================================
    def __init__(self, parent_node, ctx):
        super().__init__(parent_node, ctx)

        self._init_clause = None
        self._cond_expression = None
        self._it_expression = None

        self.start_label = None
        self.end_label = None

    # Ast generation
    # ==================================================================================================================

    def add_init_clause(self):
        """
        Last node added was a init clause node
        :return:
        """
        self._init_clause = self._children[-1]

    def add_cond_expression(self):
        self._cond_expression = self._children[-1]

    def add_it_expression(self):
        self._it_expression = self._children[-1]

    # LLVM Generation
    # ==================================================================================================================
    def generate_llvm(self, c_comment: bool = True):
        nw_label = self.get_while_label()
        self.start_label = f'start_{nw_label}'
        self.end_label = f'end_{nw_label}'

        ret = self._init_clause.generate_llvm(c_comment)
        ret += self.llvm_comment(f'for({self._cond_expression})', c_comment)
        ret += f'{self.code_indent_string()}br label %{self.start_label}\n\n'

        ret += f'{self.code_indent_string()}{self.start_label}:\n'
        self.increase_code_indent()
        ret += self.llvm_comment(str(self._cond_expression), c_comment)
        ret += self._cond_expression.llvm_load()
        ret += f'{self.code_indent_string()}br i1 {self._cond_expression.llvm_value}, label %{nw_label}, '
        ret += f'label %{self.end_label}\n\n'
        self.decrease_code_indent()

        ret += f'{self.code_indent_string()}{nw_label}:\n'
        self.increase_code_indent()
        ret += self._children[-1].generate_llvm(c_comment)
        ret += self._it_expression.generate_llvm(c_comment)
        ret += f'{self.code_indent_string()}br label %{self.start_label}\n\n'

        self.decrease_code_indent()
        self.decrease_code_indent()
        ret += f'{self.code_indent_string()}{self.end_label}:\n'
        self.increase_code_indent()

        return ret

    # Mips Generation
    # ==================================================================================================================
    def generate_mips(self, c_comment: bool = True):
        nw_label = self.get_while_label()
        self.start_label = f'start_{nw_label}'
        self.end_label = f'end_{nw_label}'

        ret = self._init_clause.generate_mips(c_comment)

        # This is the same as while
        reg = self.mips_register_reserve()
        ret += f'{self.code_indent_string()}{self.start_label}:\n'
        self.increase_code_indent()

        ret += self.mips_comment(str(self._cond_expression), c_comment)
        if self._cond_expression:
            ret += self._cond_expression.mips_store_in_register(reg)
            ret += f'{self.code_indent_string()}beqz ${reg}, {self.end_label}\n\n'

        ret += self._children[-1].generate_mips(c_comment)
        ret += self._it_expression.generate_mips(c_comment)
        ret += f'{self.code_indent_string()}b {self.start_label}\n\n'
        self.decrease_code_indent()

        ret += f'{self.code_indent_string()}{self.end_label}:\n'
        self.mips_register_free(reg)
        return ret
