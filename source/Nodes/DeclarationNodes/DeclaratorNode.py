"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from Nodes.AbstractNodes.ExpressionNode import ExpressionNode
from Nodes.ExpressionNodes.IdNode import IdNode
from Nodes.ExpressionNodes.RHSNode import RHSNode
from Specifiers import DeclaratorSpecifier


class DeclaratorNode(ExpressionNode):
    """
    We use this node to handle prefix/postfix hierarchy.
    We can omit this in a future pass. This node has no actual info about the program.
    """
    _declarator_type: DeclaratorSpecifier
    _specifier_node: ExpressionNode
    _declarator_node: "DeclaratorNode"
    _id_node: IdNode

    _BASE_LABEL = "Declarator"

    def __init__(self, parent_node):
        """
        Initializer
        :param parent_node:
        """
        super().__init__(parent_node)
        # self._extra_label = ''
        """attribute = Attributes(TypeSpecifier.DEFAULT, filename, self._line, self._column,
                               self.find_decl_type(ctx.getText()))
        self._parent_node.add_to_scope_symbol_table(self.value, attribute)"""

        self._declarator_node = None
        self._id_node = None
        self._rhs_node = None

        self._declarator_type = None

    @property
    def label(self):

        ret = self._BASE_LABEL
        if self._declarator_type is not None:
            ret += "\nType: {0}".format(self._declarator_type.value)
        return ret

    @property
    def declarator_type(self):
        return self._declarator_type

    @declarator_type.setter
    def declarator_type(self, value):
        self._declarator_type = value

    def _add_declarator_node(self, child):

        self._declarator_node = child

    def _add_id_node(self, child):
        self._id_node = child

    _OVERLOAD_MAP = {
        IdNode: _add_id_node,
    }

    def add_child(self, child):

        if isinstance(child, DeclaratorNode):
            self._add_declarator_node(child)

        elif isinstance(child, RHSNode):
            if isinstance(child, IdNode):
                self._add_id_node(child)

            self._rhs_node = child

        else:
            self._OVERLOAD_MAP.get(type(child))(self, child)

        super().add_child(child)

    def find_id(self):
        """
        We will search the identifier in the declarator tree. The declaration node wants this info for the symbol
        table.
        :return: the identifier
        """

        # this node contained the identifier, so it can just return it
        if self._id_node is not None:

            if self in self.parent_node._children:
                self._parent_node.remove_child(self)
            return self._id_node.value

        elif self._declarator_node is not None:
            return self._declarator_node.find_id()

    def first_pass(self):
        """
        We mainly want to remove this type of node in the Ast since it doesn't generate useful info.
        We use this node to handle pre postfix hierarchy.
        """

        if self._id_node is None:
            self._id_node = self.find_id()

        for child in self._children:
            child.first_pass()

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
