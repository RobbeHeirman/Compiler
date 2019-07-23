"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from typing import List, Union, TYPE_CHECKING

import LlvmCode
import Nodes.AbstractNodes.AbstractNode as AbstractNode
import Nodes.DeclarationNodes.DeclarationNode as DeclarationNode


if TYPE_CHECKING:
    import Nodes.ExpressionNodes.ExpressionNode as ExpressionNode


class ParamListNode(AbstractNode.AbstractNode):
    # Type annotations
    _children: Union[List['DeclarationNode.DeclarationNode'], List['ExpressionNode.ExpressionNode']]

    label = "Param list"

    # Built-ins
    # ==================================================================================================================
    def __init__(self, parent_node, ctx):
        super().__init__(parent_node, ctx)

    # Semantic analysis
    # ==================================================================================================================
    def get_function_signature(self):
        self._children: List[DeclarationNode]
        return [child.type_stack for child in self._children]

    # LLVM Code
    # ==================================================================================================================
    def generate_llvm_function_signature(self):
        ret = ""
        for child in self._children:
            ret += "{0}".format(child.type_stack[0].llvm_type)
            for d_type in child.type_stack[1:]:
                ret += d_type.value
            # ret += " %{0}".format(child.id)

            ret += ", "
        ret = ret[:-2]
        return ret

    def llvm_load_params(self) -> str:
        """
        Will load all parameters that are variables to temporal registers
        :return:
        """
        import Nodes.ExpressionNodes.IdentifierExpressionNode as IdentifierExpressionNode

        ret = ""
        for child in self._children:
            if isinstance(child, IdentifierExpressionNode.IdentifierExpressionNode):
                ret += child.llvm_load()

            elif isinstance(child, DeclarationNode.DeclarationNode):
                ret += child.generate_llvm()
        return ret

    def llvm_store_params(self):
        return "".join([LlvmCode.llvm_store_instruction(str(index), child.type_stack, child.id, child.type_stack,
                                                        self.code_indent_string())
                        for index, child in enumerate(self._children)])

    def llvm_call_param_nodes(self) -> str:
        return "".join([child.generate_llvm() for child in self._children])
