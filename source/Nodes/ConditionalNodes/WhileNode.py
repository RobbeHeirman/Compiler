from Nodes.ConditionalNodes.IfNode import IfNode


class WhileNode(IfNode):

    def generate_llvm(self, c_comment: bool = True):
        nw_label = self.get_while_label()
        st_cond = f'start_{nw_label}'
        end_lbl = f'end_{nw_label}'

        ret = f'{self.code_indent_string()}{st_cond}:\n'
        ret += self._condition_node.llvm_load()
        ret += f'{self.code_indent_string()} br i1 {self._condition_node.llvm_value}, label %{nw_label}, '
        ret += f'label %{end_lbl}\n'
        ret += f'{self.code_indent_string()}{nw_label}:\n'
        ret += self._statements_node.generate_llvm(c_comment)
        ret += f'br label %{st_cond}\n'

        return ret
