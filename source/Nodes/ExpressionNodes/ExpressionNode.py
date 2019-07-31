import abc
from typing import List

import Nodes.AbstractNodes.TypedNode as TypedNode
import Nodes.DeclarationNodes.DeclarationTypeModifierNode as TypeModifierNode
import type_specifier


class ExpressionNode(TypedNode.TypedNode, abc.ABC):
    _BASE_LABEL = "expression"

    # Built-ins
    # ==================================================================================================================
    def __init__(self, parent_node, ctx):
        super().__init__(parent_node, ctx)
        self._identifier_node = None
        self.type = None

        self.l_value = True

    # AST-Visuals
    # ==================================================================================================================

    @property
    def label(self):
        ret = self._BASE_LABEL + "\n"
        if self._type_stack:
            ret += "Base type: " + self._type_stack[0].value + "\n"
        return ret

    # AST-Generation
    # ==================================================================================================================
    def add_child(self, child, index=None):

        if isinstance(child, TypeModifierNode.TypeModifierNode):
            temp = self._type_modifier_node
            self._type_modifier_node = child

        super().add_child(child)

    # Semantic-Analysis
    # ==================================================================================================================
    def semantic_analysis(self, messenger) -> bool:
        """
        Semantic analysis in expressive nodes is looking up if the signature of the identifier matches the
        one in the symbol table.
        Note: We do not support implicit conversions.
        :return:
        """
        if not self._generate_secondary_types(messenger):  # the modifiers applied in the expression
            return False
        ret = True

        for child in self._children:
            if not child.semantic_analysis(messenger):
                ret = False

        return ret

    def is_constant(self):
        return False

    # LLVM-code
    # ==================================================================================================================

    @property
    @abc.abstractmethod
    def llvm_value(self) -> str:
        """
        Returns te LLVM value as a string can either be the constant directly or be a register
        :return:
        """
        pass

    def taking_address(self) -> bool:
        if self._type_modifier_node:
            return self._type_modifier_node.taking_address()
        else:
            return False

    def do_we_dereference(self) -> bool:
        if self._type_modifier_node:
            return self._type_modifier_node.do_we_dereference()
        else:
            return False

    def _generate_type_operator_stack(self) -> List[type_specifier.TypeSpecifier]:
        """
        Will make a List of all applied operator's in stack order. (Bound closest = Last Element).
        The list is represented with TypeSpecifier elements
        :return List[TypeSpecifier]: A list of type specifier if this expression had typeModifiers. Else an
                                     Empty list.
        """
        if self._type_modifier_node:
            return self._type_modifier_node.generate_type_modifier_stack()

        return []

    def generate_llvm_store(self, store_addr: int) -> str:
        """
        Store llvm value into store address
        :param int store_addr: The address to store to
        :return str : String to store to.
        """

    # Mips Code
    # ==================================================================================================================

    def mips_store_in_register(self, reg: str) -> str:
        """
        Store's the value of the expression into given register.
        :param reg: The register to store to
        :return: a mips code string resolving the store of the expression.
        """
