
from Nodes.ConditionalNodes.IfNode import IfNode


class WhileNode(IfNode):
    label = "While"
    def generate_llvm(self, c_comment: bool = True):

        nw_label = self.get_while_label()
        st_cond = f'start_{nw_label}'
        end_lbl = f'end_{nw_label}'

        ret = f'{self.code_indent_string()}br label %{st_cond}\n\n'

        ret += f'{self.code_indent_string()}{st_cond}:\n'
        self.increase_code_indent()
        ret += self._condition_node.llvm_load()
        ret += f'{self.code_indent_string()}br i1 {self._condition_node.llvm_value}, label %{nw_label}, '
        ret += f'label %{end_lbl}\n\n'
        self.decrease_code_indent()

        ret += f'{self.code_indent_string()}{nw_label}:\n'
        self.increase_code_indent()
        ret += self._statements_node.generate_llvm(c_comment)
        ret += f'{self.code_indent_string()}br label %{st_cond}\n\n'

        self.decrease_code_indent()
        ret += f'{self.code_indent_string()}{end_lbl}:\n'

        return ret

    def generate_mips(self, c_comment: bool = True):
        nw_label = self.get_while_label()
        st_cond = f'start_{nw_label}'
        end_lbl = f'end_{nw_label}'

        reg = self.mips_register_reserve()
        ret = f'{self.code_indent_string()}{st_cond}:\n'
        self.increase_code_indent()
        ret += self._condition_node.mips_store_in_register(reg)
        ret += f'{self.code_indent_string()}beqz ${reg}, {end_lbl}\n'
        ret += self._statements_node.generate_mips(c_comment)
        ret += f'{self.code_indent_string()}b {st_cond}\n'
        self.decrease_code_indent()

        ret += f'{self.code_indent_string()}{end_lbl}:\n'
        self.mips_register_free(reg)
        return ret
