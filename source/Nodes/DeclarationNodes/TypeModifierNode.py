"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
import typing

import Nodes.AbstractNodes.AbstractNode as AbstractNode
import Nodes.FunctionNodes.ParamListNode as ParamListNode
import Specifiers


class TypeModifierNode(AbstractNode.AbstractNode):
    """
    We use this node to handle prefix/postfix hierarchy.
    We can omit this in a future pass. This node has no actual info about the program.
    """
    _specifier_node: AbstractNode
    _type_modifier_node: "TypeModifierNode"
    # noinspection PyUnresolvedReferences
    _parent_node: typing.Union["TypeModifierNode", "DeclarationNode.DeclarationNode", "ExpressionNode"]

    _BASE_LABEL = "TypeModifier"

    def __init__(self, parent_node, mod_type: Specifiers.TypeModifier = None):
        """
        Initializer
        :param parent_node: the parent node
        """
        super().__init__(parent_node)

        self._type_modifier_node = None  # Child type_modifier_node. Used for nested type modifiers
        self._rhs_node = None
        self._param_list_node = None

        self.modifier_type = mod_type
        self._is_implicit_conversion = False

    @property
    def label(self):

        ret = self._BASE_LABEL
        if self.modifier_type is not None:
            ret += "\nType: {0}\n".format(self.modifier_type.value)
        else:
            ret += "??"

        if self._is_implicit_conversion:
            ret += "(implicit conversion)"
        return ret

    def _add_id_node(self, child):
        self._id_node = child

    def remove_child(self, child):

        if isinstance(child, TypeModifierNode):
            self._type_modifier_node = None

        super().remove_child(child)

    def add_child(self, child, index=None):

        if isinstance(child, TypeModifierNode):
            self._type_modifier_node = child
            self._rhs_node = child

        elif isinstance(child, ParamListNode.ParamListNode):
            self._param_list_node = child

        super().add_child(child)

    def add_id(self, identifier: str):
        """
        Will propagate an added id to the declaration node
        :param identifier: The id to propagate
        :return: None
        """
        self._parent_node.add_id(identifier)

    def generate_type_operator_stack(self, node, messenger):
        """
        This function generates the operators stack.
        :param messenger:
        :param l_value: if l_value or r _value
        :param type_stack: A stack of DeclaratorSpecifiers that represents the member operator stack.
        :return: the type_stack
        """
        if self._type_modifier_node is not None:
            self._type_modifier_node.generate_type_operator_stack(node.type_stack_ref(), messenger)

        node.type_stack_ref().append(self.modifier_type)

    def array_has_length(self) -> bool:
        if self._type_modifier_node is not None:
            return self._type_modifier_node.array_has_length()
        else:  # This is the last of the nodes.
            if self._rhs_node is None:
                return False
            else:
                return True

    def get_function_signature(self):
        if self._param_list_node:
            return self._param_list_node.get_function_signature()

    # def implicit_param_ptr_conversion(self):
    #
    #     if self.declarator_type is DeclaratorSpecifier.ARRAY:
    #         self.declarator_type = DeclaratorSpecifier.PTR
    #         self._is_implicit_conversion = True
    #         if self._rhs_node:
    #             self._rhs_node = None
    #         return
    #     else:
    #         if self._declarator_node:
    #             self._declarator_node.implicit_param_ptr_conversion()
    #     return

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
