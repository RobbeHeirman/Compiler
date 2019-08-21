import abc
from typing import List, TYPE_CHECKING

import Nodes.AbstractNodes.TypedNode as TypedNode
from Nodes.ExpressionNodes import ExpressionTypeModifierNode

import type_specifier


if TYPE_CHECKING:
    import Nodes.FunctionNodes.ParamListNode as ParamListNode


class ExpressionNode(TypedNode.TypedNode, abc.ABC):
    _BASE_LABEL = "expression"
    _place_of_value: str
    _type_modifier_node: "ExpressionTypeModifierNode.ExpressionTypeModifierNode"
    # Built-ins
    # ==================================================================================================================

    def __init__(self, parent_node, ctx):
        super().__init__(parent_node, ctx)
        self._identifier_node = None
        self.type = None

        self.l_value = False
        self.code_l_value = False
        self._place_of_value: str = 0  # The register the current value of the identifier is placed
        self._is_global = False

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

        if isinstance(child, ExpressionTypeModifierNode.ExpressionTypeModifierNode):
            if self._type_modifier_node:
                self._children.remove(self._type_modifier_node)
                child.add_child(self._type_modifier_node)

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

    def llvm_load(self, get_l_val: bool = False) -> str:
        """
        Will load this variable into a register
        :return: a string that loaded the value of the var into the register
        """

        # Modification
        stack: type_specifier.TypeStack = []

        # If marked as an natural l val (like identifier's) we need to dereference once in LLVM
        if self.code_l_value and not get_l_val:
            stack = [type_specifier.TypeSpecifier(type_specifier.TypeSpecifier.POINTER)]

        stack += self._generate_type_operator_stack()
        # Type of node
        attr = self._parent_node.get_attribute(self._place_of_value)
        type_stack = list(attr.operator_stack)

        ret_string = ''
        if self._type_modifier_node:
            self._type_modifier_node.reset_used_switches()
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
                self._is_global = False
                # Now for the actual call we will load the call value into a new temporal register
                self.increment_register_index()

                ret_string += f'{self.code_indent_string()}%{self.register_index} = call'
                ret_string += f' {"".join([child.llvm_type for child in self._type_stack])}'

                if self._parent_node.is_in_table(self._place_of_value):
                    attr_stack = self._parent_node.get_attribute(self._place_of_value).operator_stack
                    if attr_stack[-1].function_signature and attr_stack[-1].function_signature[-1] == [
                        type_specifier.TypeSpecifier.ANY]:
                        ret_string += '( i8*, ...) '

                ret_string += f' @{self._place_of_value}{call_string}\n'
                self._place_of_value = self.register_index

            elif element == type_specifier.TypeSpecifier.POINTER:

                stack_string = "".join([child.llvm_type for child in type_stack])
                call_global = '@' if self.is_in_global_table(str(self._place_of_value)) else '%'
                self.increment_register_index()
                ret_string += f'{self.code_indent_string()}%{self.register_index} = load '
                ret_string += f'{stack_string}, '
                ret_string += f'{stack_string}* {call_global}{self._place_of_value}\n'
                self._place_of_value = self.register_index
                self._is_global = False
                if type_stack:
                    type_stack.pop()

            elif element == type_specifier.TypeSpecifier.ADDRESS:
                item = stack.pop()
                assert (item == type_specifier.TypeSpecifier.POINTER), f"We dereference something else then addr " \
                    f"type This: {item} "

            elif element == type_specifier.TypeSpecifier.ARRAY:
                arr_node = self._type_modifier_node.get_bottom_arr()

                ret_string += arr_node.expression_node.llvm_load()
                self.increment_register_index()

                inbound_type = "".join([child.llvm_type for child in type_stack])
                arr_type = f'[{attr.array_size} x {inbound_type}]'
                ret_string += f'{self.code_indent_string()}%{self.register_index} = getelementptr {arr_type},'
                ret_string += f' {arr_type}* %{self._place_of_value}, i32 0, i32 {arr_node.expression_node.llvm_value}\n'
                self._place_of_value = self.register_index
                # stack.append(type_specifier.TypeSpecifier(type_specifier.TypeSpecifier.POINTER))

        return ret_string

    @property
    def llvm_value(self) -> str:
        """
        Returns te LLVM value as a string can either be the constant directly or be a register
        :return:
        """
        return f'%{self._place_of_value}'

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
        return ""

    def _get_param_node(self) -> "ParamListNode.ParamListNode":
        return self._type_modifier_node.get_param_node()

    # Mips Code
    # ==================================================================================================================

    def generate_mips(self, c_comment: bool = True):
        return self.mips_store_in_register("t0")

    def mips_store_in_register(self, reg: str) -> str:
        """
        Store's the value of the expression into given register.
        :param reg: The register to store to
        :return: a mips code string resolving the store of the expression.
        """
        return ""

    def mips_store_address_in_reg(self, target_reg):
        """
        Return's the address of where the variable is stored.
        :param target_reg:
        :return:
        """
        return ""
