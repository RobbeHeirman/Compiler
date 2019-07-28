"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""

import Nodes.AbstractNodes.AbstractNode as AbstractNode
import Nodes.AbstractNodes.ScopedNode as ScopedNode
import Nodes.GlobalNodes.GlobalDeclarationNode as GlobalDeclarationNode
import Attributes
import type_specifier
import Nodes.FunctionNodes.ParamListNode as ParamListNode
import Nodes.GlobalNodes.StatementsNode


class FuncDefNode(GlobalDeclarationNode.GlobalDeclarationNode, ScopedNode.ScopedNode):
    # The Mips Register ref's. Used for comparing with mips register stack's
    _LAZY_MIPS_REGISTERS = tuple(f't{i}' for i in reversed(range(10)))
    _PRESERVE_MIPS_REGISTERS = tuple(f's{i}' for i in reversed(range(8)))

    # Built-ins
    # ==================================================================================================================
    def __init__(self, parent_node: AbstractNode.AbstractNode, ctx):
        super().__init__(parent_node, ctx)
        self._param_list_node: ParamListNode.ParamListNode = None
        self._function_signature = []

        # We need a mechanism to keep track of the Mips Register's available
        self._lazy_mips_registers_available = list(self.__class__._LAZY_MIPS_REGISTERS)
        self._preserve_mips_registers_available = list(self.__class__._PRESERVE_MIPS_REGISTERS)

    # AST-Visuals
    # ==================================================================================================================
    @property
    def label(self):
        return 'Func def\nIdentifier: {0}\nReturn type {1}'.format(self.id, [el.value for el in
                                                                             self._type_stack[:-1]])

    # AST-generation
    # ==================================================================================================================
    @property
    def base_type(self):
        return self._type_stack[0]

    @base_type.setter
    def base_type(self, tp):
        self._type_stack.append(tp)

    def add_child(self, child, index=None):

        if isinstance(child, Nodes.GlobalNodes.StatementsNode.StatementsNode):
            self._expression_node = child

        elif isinstance(child, ParamListNode.ParamListNode):
            self._param_list_node = child

        super().add_child(child, index)

    # Semantic analysis
    # ==================================================================================================================
    def semantic_analysis(self, messenger) -> bool:
        """
        Semantic analysis of a function definition.
        1)The function and his signature needs to be added to the symbol
        Table of the upper scope.
        2) The parameters are declared variables belonging to the scope of this function.
        :return: If the semantic analysis is correct.
        """
        # Check if the children are playing nice

        if not self._param_list_node.semantic_analysis(messenger):
            return False

        # Applies all special types to the function definition
        self._generate_secondary_types(messenger)
        self._type_stack.append(type_specifier.TypeSpecifier(type_specifier.TypeSpecifier.FUNCTION,
                                                             self._param_list_node.get_function_signature()))

        self._function_signature = self._param_list_node.get_function_signature()
        attribute = Attributes.AttributesGlobal(self._type_stack, self._line, self._column, True, self)

        attribute.function_signature = self._function_signature
        if not self._add_to_table(attribute, messenger):
            return False

        for child in self._children:
            if child is not self._param_list_node:
                if not child.semantic_analysis(messenger):
                    return False
        return True

    def get_return_type(self):
        return self._type_stack[:-1]

    # LLVM Code-Generation
    # ==================================================================================================================
    def generate_llvm(self, c_comment: bool = True):

        function_signature = self._param_list_node.generate_llvm_function_signature()
        return_type = f'{"".join([child.llvm_type for child in self._type_stack[:-1]])} '
        ret = self.comment_code(c_comment, False)
        ret += f'{self.code_indent_string()} define {return_type} @{self.id}'
        ret += f'({function_signature}){{\n'
        self.increase_code_indent()

        # Read and store the parameters to their respective registers.
        ret += self._param_list_node.llvm_load_params()
        ret += self._param_list_node.llvm_store_params()

        # We need to increment our register for each param
        self.increment_register_index(self._param_list_node.child_count())

        for child in self._children[1:]:
            ret += child.generate_llvm(c_comment)

        # if self._return_node is None:
        #     ret += self.indent_string() + "  ret {0} 0\n".format(self.base_type.llvm_type)

        ret += "}\n"
        self.decrease_code_indent()
        return ret

    # MIPS Code-Generation
    # ==================================================================================================================
    def generate_mips(self, c_comment: bool = True):

        ret = self.comment_code(c_comment)

        # Label the start of the function
        ret += f'{self.id}:\n'
        # First we need to tell the symbol table where to find the arguments. It is possible there are some element's
        # on the stack. So the method will increment the sp accordingly.
        self._mips_stack_pointer += self._param_list_node.mips_assign_params_to_mem()

        # Fill in the function body
        self.increase_code_indent()
        # ret += self.code_indent_string()
        ret += f"{self.code_indent_string()}".join([child.generate_mips(c_comment) for child in self._children[1:]])
        # Some awesome code here

        # Return
        # ret += f'{self.code_indent_string()}jr $ra'
        return ret

    def register_available(self) -> bool:
        """
        Return's True if their is a register available, False if not (Variables should be stored on stack then)
        :return bool:  A bool = True if register(s) are available Else = False
        """
        return True if (self._PRESERVE_MIPS_REGISTERS or self._LAZY_MIPS_REGISTERS) else False

    def get_available_register(self) -> str:
        """
        Return's a available register. Start's with the register the function doesn't need to preserve
        :return string: A register string
        """

        return self._lazy_mips_registers_available.pop() if self._lazy_mips_registers_available else \
            self._preserve_mips_registers_available.pop()



    # Meta Code Generation
    # ==================================================================================================================
    def comment_code(self, c_comment: bool = True, mips=True):
        """
        Generates the comment code
        :param mips:
        :param c_comment:
        :return: a string with comment code
        """
        # Code for a function Def in LLVM: Example: LLVM: Define i32 @main(int) {...} <=> C: int main(int){...}
        # Commenting...
        function_signature = self._param_list_node.generate_llvm_function_signature()
        return_type = f'{"".join([child.llvm_type for child in self._type_stack[:-1]])} '

        return self.mips_comment(f'{return_type} {self.id}({function_signature}){{...}}', c_comment) if mips else \
            self.llvm_comment(f'{return_type} {self.id}({function_signature}){{...}}', c_comment)
