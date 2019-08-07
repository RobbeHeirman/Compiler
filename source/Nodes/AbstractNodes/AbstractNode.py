"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
import abc
import typing
import Attributes
import messages


class AbstractNode(abc.ABC):
    """
    Abstract class of a node of the AST.
    Should be overridden by specific nodes of the AST.
    """

    # Built-ins
    # ==================================================================================================================
    def __init__(self, parent: "AbstractNode" = None, ctx=None):
        """
        Initializer
        """
        self._parent_node: "AbstractNode" = parent
        self._children: typing.List["AbstractNode"] = list()

        # Block for graphviz dot representation.
        self._index: int = self.assign_index()

        start = ctx.start
        self._line: int = start.line
        self._column: int = start.column

        self._is_drawn = False

    # AST Visuals
    # ==================================================================================================================
    def dot_string(self) -> str:
        """
        Generates the visual representation of the subtree in .dot.
        :return: str A string representing the dot representation of the subtree.
        """

        ret = "{0}[label = \"{1}\"];\n".format(self._index, self.label)
        ret += "{0}--{{".format(self._index)
        ret += ''.join([f'{child.index} ' for child in self._children])
        ret += "}\n"
        self._is_drawn = True
        ret += ''.join([child.dot_string() for child in self._children])

        return ret

    @property
    def index(self) -> int:
        """
        .Dot index mainly. But every node has an unique index number so can be used for other utils.
        :return: int Integer index of node
        """
        return self._index

    def assign_index(self) -> int:
        """
        Assigns the node a new index on creation
        :return: the assigned integer index
        """
        return self._parent_node.assign_index()

    @property
    @abc.abstractmethod
    def label(self) -> str:  # Enforcing every node defines a label
        """
        Label of the AST. Used in the DOT representation.
        :return: string label representation of node in DOT
        """
        pass

    # AST Generation
    # ==================================================================================================================
    @property
    def parent_node(self) -> "AbstractNode":
        return self._parent_node

    @parent_node.setter
    def parent_node(self, value: "AbstractNode") -> None:
        self._parent_node = value

    def get_child_index(self, child: "AbstractNode") -> int:
        """
        Returns the index in the children container of child
        :param: child AbstractNode
        :return: int integer index of child
        """
        return self._children.index(child)

    def add_child(self, child: "AbstractNode", index: int = None) -> None:
        """
        Add a child node to the AST.
        :param child AbstractNode a ASTNode that functions as a child
        :param index int is needs to be placed at a certain location
        """
        if index is None:
            self._children.append(child)
        else:
            self._children.insert(index, child)

    def remove_child(self, child: "AbstractNode") -> None:
        """
        Removes a child by value (reference of child node)
        :param child AbstractNode the node that needs to be removed from the child list
        """
        self._children.remove(child)

    def pop_child(self, index: int = -1) -> "AbstractNode":
        """
        Follows list pop syntax. Removes child at index and returns it
        :param index: index where we want to remove
        :return: THe removed Node
        """
        return self._children.pop(index)

    def child_count(self) -> int:
        """
        :return: int The amount of children a node has.
        """
        return len(self._children)

    def get_children(self) -> typing.List["AbstractNode"]:
        """
        Returns a copy of the children list
        :return:
        """
        return list(self._children)

    def get_attribute(self, lexeme: str) -> typing.Union[Attributes.Attributes]:
        """
        Get's an attribute from the symbol table enclosing this scope. The derived scoped nodes have the symbol
        tables to look into
        :param lexeme: str A string representation ID of the symbol we look for
        :return: Attributes Returns the attributes of the id
        """
        return self._parent_node.get_attribute(lexeme)

    def cleanup(self):
        """
        Some nodes need to clean stuff up
        :return:
        """
        raise Exception("{0} type does not have cleanup implemented".format(type(self)))

    # Semantic analysis
    # ==================================================================================================================
    def semantic_analysis(self, messenger: messages.MessageGenerator) -> bool:
        """
        Not all nodes check for semantic correctness. Those who do not just forward the check to their children.
        this function NEEDS to be overwritten by nodes who do check on semantics.
        :param MessageGenerator messenger: Responsible for generation of error messages
        :return: Returns the amount of errors generated.
        """
        ret = all([child.semantic_analysis(messenger) for child in list(self._children)])
        return ret

    @property
    def line(self) -> int:
        """
        Line in C code this node is generated from.
        :return: int the line number.
        """
        return self._line

    @property
    def column(self) -> int:
        """
        Place in line in C code where this node is generated from.
        :return: the index on line
        """
        return self._column

    def is_in_table(self, lexeme: str) -> bool:
        return self._parent_node.is_in_table(lexeme)

    def is_in_global_table(self, lexeme: str) -> bool:
        return self._parent_node.is_in_global_table(lexeme)

    def add_to_scope_symbol_table(self, lexeme: str, attribute: Attributes.Attributes) -> bool:
        """
        Hook to add a lexeme to symbol table. Child classes may need to implement this.
        We will just call the parents add symbol to scope. Scoped nodes contain SymbolTables and will look
        in their own table.
        :param lexeme: the lexeme we want to add.
        :param attribute Attribute object that describes the attributes of the lexeme.
        :return bool true if successfully added, false if not.
        """
        return self._parent_node.add_to_scope_symbol_table(lexeme, attribute)

    def is_global(self) -> bool:
        """
        Check is a Node is global declared or local declared
        :return:
        """
        return self._parent_node.is_global()

    # LLVM Code Generation
    # ==================================================================================================================

    def generate_llvm(self, c_comment: bool = True) -> str:
        """
        Generates the corresponding node into llvm instructions.
        :param bool c_comment: Will generate The Compiled C code in comment's next to the instructions
        :return str: generates the instructions as a string
        """
        ret = ""
        for child in self._children:
            ret += child.generate_llvm(c_comment)

        return ret

    def llvm_comment(self, comment_string: str, do_comment: bool) -> str:
        """
        Generates a comment string.
        :param string comment_string:
        :param bool do_comment: Must we generate the comment string?
        :return: a comment string if write comment's is enabled otherwise a empty string
        """

        return f'{self.code_indent_string()}; {comment_string}\n' if do_comment else ""

    # MIPS Code Generation
    # ==================================================================================================================

    def generate_mips(self, c_comment: bool = True) -> str:
        """
            Generates the corresponding node into mips instructions.
            :param bool c_comment: Will generate The Compiled C code in comment's next to the instructions
            :return str: generates the instructions as a string
            """
        ret = ""
        for child in self._children:
            ret += child.generate_mips(c_comment)

        return ret

    def mips_comment(self, comment_string: str, do_comment: bool) -> str:
        """
        Generates a comment string.
        :param string comment_string:
        :param bool do_comment: Must we generate the comment string?
        :return: a comment string if write comment's is enabled otherwise a empty string
        """

        return f'{self.code_indent_string()}# {comment_string}\n' if do_comment else ""

    def mips_register_available(self) -> bool:
        """
        Just forwards the request to check of there are register mips available in this scope.
        :return: True if there are register's available else False
        """

        return self._parent_node.mips_register_available()

    def mips_get_available_register(self) -> bool:
        """
        Forward's request for an available register
        :return: A Available Register
        """

        return self._parent_node.mips_get_available_register()

    @property
    def mips_stack_pointer(self) -> int:
        return self._parent_node.mips_stack_pointer

    def mips_increase_stack_pointer(self, amount: int) -> int:
        return self._parent_node.mips_increase_stack_pointer(amount)

    def mips_stack_space_needed(self) -> int:
        return 0

    def mips_assign_register(self):
        pass

    def mips_assign_address(self):
        pass

    @property
    def code_function_base_label(self) -> str:
        return self._parent_node.code_function_base_label

    # Meta Code Generation
    # ==================================================================================================================
    @property
    def code_indent_level(self):
        return self._parent_node.code_indent_level

    def code_indent_string(self) -> str:
        """
        Used to manage indentation in LLVM Code generation
        :return: string A string of whitespaces matching the indent level
        """
        return "  " * self._parent_node.code_indent_level

    def increase_code_indent(self) -> None:
        """
        Called by all scope enclosing nodes. Will increase the indentation string.
        :return: None
        """
        self._parent_node.increase_code_indent()

    def decrease_code_indent(self) -> None:
        self._parent_node.decrease_code_indent()

    @property
    def register_index(self) -> int:
        """
        Returns the top register index.
        Used to assign temporal register indexes
        :return: int the register index integer
        """
        return self._parent_node.register_index

    def increment_register_index(self) -> None:
        """
        If we need a new register we can increment the register indexes
        :return: None
        """
        self._parent_node.increment_register_index()


