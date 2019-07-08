"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from typing import List, Union

import Nodes.AbstractNodes.AbstractNode as AbsractNode
import Nodes.DeclarationNodes.DeclarationNode as DeclarationNode
from Specifiers import TypeSpecifier


class DeclListNode(AbsractNode.AbstractNode):
    """
    Start of a , separated list of declarations.
    this such nodes has ONE base type and a list of declarations
    """
    base_type: TypeSpecifier
    _declaration_nodes: List[DeclarationNode.DeclarationNode]
    _BASE_LABEL = "decl_list"

    def __init__(self, parent_node):
        super().__init__(parent_node)

        self.base_type = None
        self._declaration_nodes = list()

    @property
    def label(self):
        return '{0}'.format(self._BASE_LABEL)

    def _add_declaration_node(self, child: DeclarationNode.DeclarationNode):
        self._declaration_nodes.append(child)

    # This is how we mimic function overloading. Basically the node needs to know what to do with his child.
    _ADD_OVERLOAD_MAP = {
        DeclarationNode.DeclarationNode: _add_declaration_node,
    }

    def add_child(self, child: Union[DeclarationNode.DeclarationNode], index=None):
        self._ADD_OVERLOAD_MAP[type(child)](self, child)
        super().add_child(child, index)

    def cleanup(self):
        """
        On the first pass we need to decide the type of the list. And prepend what we found to the declarations.
        Since the list is just an abstract way of handling a multi declaration on a single line.
        """

        # We will tell al the declaration nodes what their base type is. They need it for further code generation
        # A base type is integer, float, char (can be extended with void, double...)
        # Since we don't really need more info from this node. It will become obsolete in further code gen,
        # So we remove it.

        index = self._parent_node.get_child_index(self)
        for decl_node in self._declaration_nodes:
            decl_node.base_type = self.base_type
            decl_node.parent_node = self._parent_node
            self._parent_node.add_child(decl_node, index)
            index += 1
            decl_node.first_pass()

        self._parent_node.remove_child(self)

