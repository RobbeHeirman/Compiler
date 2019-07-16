"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
import LlvmCode
import Nodes.AbstractNodes.TypedNode as TypedNode
import Nodes.DeclarationNodes.TypeModifierNode as TypeModifierNode
import Nodes.DeclarationNodes.ArrayInitNode as ArrayInitNode
import Nodes.ExpressionNodes.ExpressionNode as ExpressionNode

import Attributes as Attributes
from messages import MessageGenerator


class DeclarationNode(TypedNode.TypedNode):
    """
    Represents a GlobalDeclaration in our abstract syntax tree.
    Will deduct the base type of the declaration in the first pass.
    Has 1 or 2 children a declarator (will become a stack of pre and postfix type specifiers after first pass)
    An optional initializer as 2d child.
    """
    _type_modifier_node: "TypeModifierNode"
    _lexeme: str

    _BASE_LABEL = "Declaration"

    def __init__(self, parent_node, filename, ctx):
        super().__init__(parent_node, filename, ctx)

        self.id = None
        self._expression_node = None
        # Error message info
        self._filename = filename
        start = ctx.start
        self._line = start.line
        self._column = start.column

    @property
    def label(self):
        ret_label = self._BASE_LABEL
        if self._type_stack:
            ret_label += f"\\n Type: {[val.value for val in self._type_stack]}"

        if self.id is not None:
            ret_label += f"\\n Identifier: {self.id}"

        return ret_label

    @property
    def type_string_llvm(self):
        return self._type_stack[0].llvm_type + "*" * len(self._type_stack)

    def to_attribute(self):

        return Attributes.Attributes(self._type_stack, self._filename, self._line, self._column)

    def add_id(self, identifier):

        self.id = identifier

    def add_child(self, child, index: int = None):
        """
        extends add_child of abstractNode. To quick filter useful information for DeclarationNode
        :param index: index where to add
        :param child: An abstractNode
        """

        if isinstance(child, TypeModifierNode.TypeModifierNode):
            self._type_modifier_node = child

        elif isinstance(child, ExpressionNode.ExpressionNode) or isinstance(child, ArrayInitNode.ArrayInitNode):
            self._expression_node = child

        elif child is None:
            print("happens")

        super().add_child(child)

    def remove_child(self, child):

        if isinstance(child, TypeModifierNode.TypeModifierNode):
            self._type_modifier_node = None

        super().remove_child(child)

    def semantic_analysis(self, messenger: MessageGenerator) -> bool:
        """
        On a declaration, a new identifier is introduced into the scope. This has to be an unique identifier
        on this scope lvl. But it can overshadow higher scoped (global...) declared variables with the same identifier.
        :return: Amount of errors encountered in node and children.
        """
        ret = True
        self._generate_type_modifier_stack(messenger)
        # We have all the info for the corresponding attribute object
        attr = self._make_attribute()

        # Check of the expression is semantically correct
        if self._expression_node:
            if not self._expression_node.semantic_analysis(messenger):
                return False
            self.analyze_initializer(messenger)

            # # 2) Explicit list init if array has no init size if type is array .
            # if self._type_stack[-1] is Specifiers.TypeModifier.ARRAY:
            #     # Last element is top of the stack.
            #     # If array size is not specified MUST have array init rhs.
            #     if not self._type_modifier_node.array_has_length():
            #         if self._expression_node is None:
            #             if not isinstance(self._parent_node, ParamListNode.ParamListNode):
            #                 DeclarationNode._messages.error_array_size_missing(self.id, attr)
            #                 ret = False
            #
            #     if not isinstance(self._expression_node, ArrayInitNode.ArrayInitNode):
            #         tpl = self._expression_node.get_error_info()
            #         t_file = attr.filename
            #         attr.filename = tpl[0]
            #         t_line = attr.line
            #         attr.line = tpl[1]
            #         t_column = attr.column
            #         attr.column = tpl[2]
            #         DeclarationNode._messages.error_invalid_initializer(self.id, attr)
            #         attr.filename = t_file
            #         attr.line = t_line
            #         attr.column = t_column
            #         ret = False
            #
            # # Functions are allowed to be declared but definitions are not handled by this node
            # elif self._type_stack[-1] is Specifiers.TypeModifier.FUNC:
            #     DeclarationNode._messages.error_func_initialized_like_var(self.id, attr)
            #     attr.function_signature = self._type_modifier_node.get_function_signature()
            #     ret = False

        # Add to the scopes symbol_table.

        if not self._parent_node.add_to_scope_symbol_table(self.id, attr):
            messenger.error_redeclaration(self.id, attr)
            ret = False

        return ret

    def analyze_initializer(self, messenger: MessageGenerator):
        """
        Here we will check if the type of the initializer is conform with te type of the declaration
        :return:
        """
        # print(self.__class__.warning_count())
        expression_stack = self._expression_node.type_stack
        try:
            prev_ele = expression_stack[-1]
        except IndexError:
            print(self.id)
            raise IndexError
        for element in reversed(self._type_stack):
            if expression_stack and element == expression_stack[-1]:
                prev_ele = expression_stack.pop()
            else:
                print(messenger.warning_init_makes_a_from_b(prev_ele.value, self._type_stack[-1].value, self._filename,
                                                            self._line, self._column))
                break

        return True
        # TODO mechanism to inform expression node of conversion

    def _make_attribute(self):
        return Attributes.Attributes(self._type_stack, self._filename, self._line, self._column)

    def generate_llvm(self) -> str:
        """"
        This is allocating addresses, form is : %{lexeme} = alloca {type}, align {alignment}
        """
        type_modifier_str = ""
        for _type in self.type_stack:
            type_modifier_str += _type.value

        ret = self.indent_string() + "; Declaration: {0}{1} {2}\n".format(self._type_stack[0].value, type_modifier_str,
                                                                          self.id)

        # # Special types need other llvm code first
        # if self._type_stack and self._type_stack[-1] is TypeModifierNode.TypeModifier.ARRAY:
        #     # Find the type
        #     size = 0
        #     if self._expression_node:
        #         size = self._expression_node.size()  # Size of array if declared trough list
        #     r_type = self.base_type.llvm_type + ptr
        #     secondary_type = "[ " + str(size) + " x " + r_type + " ]"  # This is how we init an array
        #     ret += self.indent_string() + "%{0} = alloca {1}\n".format(
        #         self.id, secondary_type, self.base_type.llvm_alignment)

        # else:

        ret += LlvmCode.llvm_allocate_instruction(self.id, self._type_stack, self.indent_string())

        if self._expression_node is not None:
            ret += self.indent_string() + "; = ...\n"
            ret += self._expression_node.generate_llvm()
            if not (isinstance(self._expression_node, ArrayInitNode.ArrayInitNode)):
                ret += LlvmCode.llvm_store_instruction(str(self.register_index), self._type_stack, self.id,
                                                       self._type_stack, self.indent_string())
        ret += self.indent_string() + "; end declaration\n"
        return ret
