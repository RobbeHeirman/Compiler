from Nodes.ConditionalNodes.IfNode import IfNode


class WhileNode(IfNode):
    label = "While"

    # Built-ins
    # ==================================================================================================================
    def __init__(self, parent_node, ctx):
        super().__init__(parent_node, ctx)
        self.end_label = ""
        self.start_label = ""

    # Semantic Analysis
    # ==================================================================================================================
    def find_while_sw_node(self):
        return self

    # LLVM-Code
    # ==================================================================================================================
    def generate_llvm(self, c_comment: bool = True):
        nw_label = self.get_while_label()
        self.start_label = f'start_{nw_label}'
        self.end_label = f'end_{nw_label}'

        ret = self.llvm_comment(f'while({self._condition_node})', c_comment)
        ret += f'{self.code_indent_string()}br label %{self.start_label}\n\n'

        ret += f'{self.code_indent_string()}{self.start_label}:\n'
        self.increase_code_indent()
        ret += self.llvm_comment(str(self._condition_node), c_comment)
        ret += self._condition_node.llvm_load()
        ret += f'{self.code_indent_string()}br i1 {self._condition_node.llvm_value}, label %{nw_label}, '
        ret += f'label %{self.end_label}\n\n'
        self.decrease_code_indent()

        ret += f'{self.code_indent_string()}{nw_label}:\n'
        self.increase_code_indent()
        ret += self._statements_node.generate_llvm(c_comment)
        ret += f'{self.code_indent_string()}br label %{self.start_label}\n\n'

        self.decrease_code_indent()
        self.decrease_code_indent()
        ret += f'{self.code_indent_string()}{self.end_label}:\n'
        self.increase_code_indent()

        return ret

    # Mips-Code
    # ==================================================================================================================
    def generate_mips(self, c_comment: bool = True):
        nw_label = self.get_while_label()
        self.start_label = f'start_{nw_label}'
        self.end_label = f'end_{nw_label}'

        reg = self.mips_register_reserve()
        ret = f'{self.code_indent_string()}{self.start_label}:\n'
        self.increase_code_indent()

        ret += self.mips_comment(str(self._condition_node), c_comment)
        ret += self._condition_node.mips_store_in_register(reg)
        ret += f'{self.code_indent_string()}beqz ${reg}, {self.end_label}\n\n'
        ret += self._statements_node.generate_mips(c_comment)
        ret += f'{self.code_indent_string()}b {self.start_label}\n\n'
        self.decrease_code_indent()

        ret += f'{self.code_indent_string()}{self.end_label}:\n'
        self.mips_register_free(reg)
        return ret
