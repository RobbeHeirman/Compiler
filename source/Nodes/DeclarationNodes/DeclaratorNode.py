"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from Nodes.AbstractNodes.ExpressionNode import ExpressionNode


class DeclaratorNode(ExpressionNode):
    """
    We use this node to handle prefix/postfix hierarchy.
    We can omit this in a future pass. This node has no actual info about the program.
    """
    label = "Declarator"

    def __init__(self, parent_node, filename, ctx):
        """
        Initializer
        :param parent_node:
        :param filename:
        :param ctx:
        """
        super().__init__(parent_node)
        self._extra_label = ''
        """attribute = Attributes(TypeSpecifier.DEFAULT, filename, self._line, self._column,
                               self.find_decl_type(ctx.getText()))
        self._parent_node.add_to_scope_symbol_table(self.value, attribute)"""

    def llvm_code_value(self):
        pass

    """def find_decl_type(self, val) -> DeclType:
        match = re.search(r"\((.)*\)", val)
        if match is not None:
            self._value = self._value[:match.span()[0]]
            self._extra_label = "function:"
            return DeclType.FUNCTION
        else:
            return DeclType.SIMPLE"""

    def llvm_type(self):
        pass
