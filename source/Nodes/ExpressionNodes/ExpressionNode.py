import abc
from typing import List

import Nodes.AbstractNodes.TypedNode as TypedNode
import Nodes.DeclarationNodes.DeclarationTypeModifierNode as TypeModifierNode
import type_specifier
from Nodes.FunctionNodes import ParamListNode


class ExpressionNode(TypedNode.TypedNode, abc.ABC):
    _BASE_LABEL = "expression"

    # Built-ins
    # ==================================================================================================================
    def __init__(self, parent_node, ctx):
        super().__init__(parent_node, ctx)
        self._identifier_node = None
        self.type = None

        self.l_value = True

        self._place_of_value = 0  # The register the current value of the identifier is placed

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

    def llvm_load(self, reg_load_from=None, is_l_val: bool = False) -> str:
        """
        Will load this variable into a register
        :return: a string that loaded the value of the var into the register
        """

        self._place_of_value = reg_load_from if reg_load_from else self._place_of_value

        # The first el of the operator stack is the implicit conversion from L to R value

        stack: type_specifier.TypeStack = []
        type_stack = list(self._parent_node.get_attribute(self._place_of_value).operator_stack)
        if not is_l_val:
            stack = [type_specifier.TypeSpecifier(type_specifier.TypeSpecifier.POINTER)]
            type_stack.insert(1, type_specifier.TypeSpecifier(type_specifier.TypeSpecifier.POINTER))
        stack += self._generate_type_operator_stack()

        ret_string = ''
        while stack:
            element: type_specifier.TypeSpecifier = stack.pop()
            if element == type_specifier.TypeSpecifier.FUNCTION:

                # Function calls are trickier we need to have the call argument's in place we do that in the next block
                param_node = self._get_param_node()
                ret_string += param_node.llvm_load_params()

                # Next up we make a string for the parameter call
                child_list: List[ExpressionNode] = param_node.get_children()
                # the children know where there values are loaded into in child.llv_value
                children_their_strings = []
                for child in child_list:
                    child_string = ''.join([type_child.llvm_type for type_child in child.type_stack])
                    child_string += f' {child.llvm_value}'
                    children_their_strings.append(child_string)
                call_string = '(' + ', '.join(children_their_strings) + ')'

                stack.pop()

                # Now for the actual call we will load the call value into a new temporal register
                self.increment_register_index()

                ret_string += f'{self.code_indent_string()}%{self.register_index} = call'
                ret_string += f' {"".join([child.llvm_type for child in self._type_stack])}'
                ret_string += f' @{self._place_of_value}{call_string}\n'
                self._place_of_value = self.register_index
            elif element == type_specifier.TypeSpecifier.POINTER:
                type_stack.pop()
                stack_string = "".join([child.llvm_type for child in type_stack])
                call_global = '@' if self.is_in_global_table(str(self._place_of_value)) else '%'
                self.increment_register_index()
                ret_string += f'{self.code_indent_string()} %{self.register_index} = load '
                ret_string += f'{stack_string}, '
                ret_string += f'{stack_string}* {call_global}{self._place_of_value}\n'
                self._place_of_value = self.register_index

            elif element == type_specifier.TypeSpecifier.ADDRESS:
                item = stack.pop()
                assert (item == type_specifier.TypeSpecifier.POINTER), f"We dereference something else then addr " \
                    f"type This: {item} "

        return ret_string

    @property
    @abc.abstractmethod
    def llvm_value(self) -> str:
        """
        Returns te LLVM value as a string can either be the constant directly or be a register
        :return:
        """
        pass

    @property
    def llvm_place_of_value(self):
        return self._place_of_value

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

    def _get_param_node(self) -> ParamListNode.ParamListNode:
        return self._type_modifier_node.get_param_node()

    # Mips Code
    # ==================================================================================================================

    def mips_store_in_register(self, reg: str) -> str:
        """
        Store's the value of the expression into given register.
        :param reg: The register to store to
        :return: a mips code string resolving the store of the expression.
        """
