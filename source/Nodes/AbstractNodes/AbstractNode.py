"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
import abc
import typing
import Attributes


class AbstractNode(abc.ABC):
    """
    Abstract class of a node of the AST.
    Should be overridden by specific nodes of the AST.
    """
    _index_counter = -1
    _indent_level = 0

    # Built-ins
    # ==================================================================================================================
    def __init__(self, parent: "AbstractNode" = None, ctx=None):
        """
        Initializer
        """

        AbstractNode._index_counter += 1

        # Block for graphviz dot representation.
        self._index: int = AbstractNode._index_counter

        self._parent_node: "AbstractNode" = parent
        self._children: typing.List["AbstractNode"] = list()

        start = ctx.start
        self._line: int = start.line
        self._column: int = start.column

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
        ret += ''.join([child.dot_string() for child in self._children])
        return ret

    @property
    def index(self) -> int:
        """
        .Dot index mainly. But every node has an unique index number so can be used for other utils.
        :return: int Integer index of node
        """
        return self._index

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

    def get_attribute(self, lexeme: str) -> typing.Union[Attributes.Attributes]:
        """
        Get's an attribute from the symbol table enclosing this scope. The derived scoped nodes have the symbol
        tables to look into
        :param lexeme: str A string representation ID of the symbol we look for
        :return: Attributes Returns the attributes of the id
        """
        return self._parent_node.get_attribute(lexeme)

    def _cleanup(self):
        """
        Some nodes need to clean stuff up
        :return:
        """
        raise Exception("{0} type does not have cleanup implemented".format(type(self)))

    # Semantic analysis
    # ==================================================================================================================
    def semantic_analysis(self, messenger) -> bool:
        """
        Not all nodes check for semantic correctness. Those who do not just forward the check to their children.
        this function NEEDS to be overwritten by nodes who do check on semantics.
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

    def generate_llvm(self) -> str:
        """
        Generates the corresponding node into llvm instructions.
        :return: generates the instructions as a string
        """
        ret = ""
        for child in self._children:
            ret += child.generate_llvm()

        return ret

    @staticmethod
    def code_indent_string() -> str:
        """
        Used to manage indentation in LLVM Code generation
        :return: string A string of whitespaces matching the indent level
        """
        return "  " * AbstractNode._indent_level

    @staticmethod
    def increase_code_indent() -> None:
        """
        Called by all scope enclosing nodes. Will increase the indentation string.
        :return: None
        """
        AbstractNode._indent_level += 1

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
