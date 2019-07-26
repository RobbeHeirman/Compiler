"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from typing import List, Union

import Nodes.ExpressionNodes.ExpressionNode as ExpressionNode
import Nodes.FunctionNodes.ParamListNode as ParamListNode

import LlvmCode
import messages
import type_specifier


class IdentifierExpressionNode(ExpressionNode.ExpressionNode):
    # TypeAnnotations
    id: str
    _l_value: bool

    # Built-ins
    # ==================================================================================================================
    def __init__(self, parent_node, ctx):
        super().__init__(parent_node, ctx)
        self.id = ctx.getText()
        self._l_value = True  # As it's base form an identifier is an Lvalue
        self._place_of_value: Union[int, str] = self.id  # The register the current value of the identifier is placed

    def __str__(self):
        return f'{self.id}{[child for child in self._type_stack]}'

    # AST visuals
    # ==================================================================================================================
    @property
    def label(self) -> str:

        ret = super().label
        ret += "Identifier\n Id: {0}".format(self.id)

        return ret

    # Semantic analysis
    # ==================================================================================================================
    def semantic_analysis(self, messenger: messages.MessageGenerator) -> bool:

        # First check if the id was declared
        if not self.is_in_table(self.id):
            messenger.error_undeclared_var(self.id, self._line, self._column)
            return False

        self._type_stack = self.get_attribute(self.id).operator_stack
        if not self._generate_secondary_types(messenger):  # the modifiers applied in the expression

            return False

        return True

    # LLVM Code generation
    # ==================================================================================================================
    def generate_llvm(self, c_comment: bool = True):

        self.increment_register_index()

        if self._is_function_call():
            print("llvm for a function call")

            # We pop off the function type since it's a call
            self._type_stack.pop()
            # This node will load all the value's in place
            param_node = self._get_param_node()
            ret = param_node.llvm_call_param_nodes()

        else:
            ret = self.code_indent_string() + ";... {0}\n".format(self.id)
            ret += self.llvm_load()

        return ret

    def llvm_load(self, reg_load_from=None) -> str:
        """
        Will load this variable into a register
        :return: a string that loaded the value of the var into the register
        """

        self._place_of_value = reg_load_from if reg_load_from else self._place_of_value

        # The first el of the operator stack is the implicit conversion from L to R value
        stack: type_specifier.TypeStack = [type_specifier.TypeSpecifier(type_specifier.TypeSpecifier.POINTER)]
        stack += self._generate_type_operator_stack()

        # Currently the different we can handle are * = Dereference, & = Take Address of, (params) = A function call
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

                # Now for the actual call we will load the call value into a new temporal register
                self.increment_register_index()
                self._place_of_value = self.register_index
                ret_string += f'{self.code_indent_string()}%{self._place_of_value} = call'
                ret_string += f' {"".join([child.llvm_type for child in self._type_stack])}'
                ret_string += f' @{self.id}{call_string}\n'

            elif element == type_specifier.TypeSpecifier.POINTER:
                call_global = True if self.is_in_global_table(str(self._place_of_value)) else False
                self.increment_register_index()
                ret_string += LlvmCode.llvm_load_instruction(self._place_of_value, self._type_stack,  # Load From
                                                             str(self.register_index), self._type_stack,  # To
                                                             call_global, self.code_indent_string())  # Metadata
                self._place_of_value = self.register_index

            elif element == type_specifier.TypeSpecifier.ADDRESS:
                item = stack.pop()
                assert (item == type_specifier.TypeSpecifier.POINTER), f"We dereference something else then addr " \
                    f"type This: {item} "

            return ret_string

    def generate_llvm_store(self, addr: str) -> str:
        """
        Tell the IDExpresionNode to store it's value to a certain address. This could be a temporal address
        or a register constructed by a declaration. The trick is to deduce the corresponding loads, calls and stores
        depending on the type Modifiers
        :param addr:  the address to store to
        :return: The generated store instruction string
        """
        ret = self.llvm_load()
        ret += LlvmCode.llvm_store_instruction(self._place_of_value, self._type_stack, addr, self._type_stack,
                                               self.code_indent_string())
        return ret

    def _is_function_call(self) -> bool:
        if self._type_modifier_node:
            return self._type_modifier_node.is_function_call()
        return False

    def _get_param_node(self) -> ParamListNode.ParamListNode:
        return self._type_modifier_node.get_param_node()

    @property
    def llvm_value(self):
        return f'%{self._place_of_value}'
