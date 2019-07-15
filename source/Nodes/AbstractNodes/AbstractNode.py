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
    _children: typing.List["AbstractNode"]
    _parent_node: "AbstractNode"

    _index_counter = 0
    _indent_level = 0

    def __init__(self, parent: "AbstractNode" = None, filename=None, ctx=None):
        """
        Initializer
        """

        # Block for graphviz dot representation.
        self._index = AbstractNode._index_counter
        AbstractNode._index_counter += 1
        self._parent_node = parent
        self._children = list()

        self._filename = filename
        self._line = None
        self._column = None
        if ctx:
            start = ctx.start
            self._line = start.line
            self._column = start.column

    @property
    def filename(self):
        return self._filename

    @property
    def line(self):
        return self._line

    @property
    def column(self):
        return self._column

    @property
    def index(self):
        return self._index

    @property
    @abc.abstractmethod
    def label(self):  # Enforcing every node defines a label
        pass

    @property
    def parent_node(self) -> "AbstractNode":
        return self._parent_node

    @parent_node.setter
    def parent_node(self, value: "AbstractNode"):
        self._parent_node = value

    def dot_string(self) -> str:
        """Generates the visual representation of the node in .dot"""
        ret = "{0}[label = \"{1}\"];\n".format(self._index, self.label)
        ret += "{0}--{{".format(self._index)
        for child in self._children:
            ret += "{0} ".format(child.index)

        ret += "}\n"

        for child in self._children:
            ret += child.dot_string()

        return ret

    def indent_string(self):

        return "  " * self._indent_level

    def get_child_index(self, child):
        return self._children.index(child)

    def add_child(self, child: "AbstractNode", index: int = None):
        """
        Add a child node to the AST.
        :param index: is needs to be placed at a certain location
        :param child: a ASTNode that functions as a child
        """
        if index is None:
            self._children.append(child)
        else:
            self._children.insert(index, child)

    def remove_child(self, child):
        """
        Removes a child by value (reference of child node)
        """
        self._children.remove(child)

    def pop_child(self, index: int = -1) -> "AbstractNode":
        """
        Follows list pop syntax. Removes child at index and returns it
        :param index: index where we want to remove
        :return: THe removed Node
        """
        return self._children.pop(index)

    def is_in_table(self, lexeme: str) -> bool:
        return self._parent_node.is_in_table(lexeme)

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

    @property
    def register_index(self) -> int:
        return self._parent_node.register_index

    def increment_register_index(self):
        self._parent_node.increment_register_index()

    def get_attribute(self, lexeme) -> typing.Union[Attributes.Attributes, Attributes.AttributesGlobal]:
        return self._parent_node.get_attribute(lexeme)

    def cleanup(self):
        """
        Some nodes need to clean stuff up
        :return:
        """
        raise Exception("{0} type does not have cleanup implemented".format(type(self)))

    def first_pass(self):
        """
        AST cleanup.
        :return:
        """
        for child in self._children:
            child.first_pass()

    def semantic_analysis(self, messenger) -> bool:
        """
        Not all nodes check for semantic correctness. Those who do not just forward the check to their children.
        this function NEEDS to be overwritten by nodes who do check on semantics.
        :return: Returns the amount of errors generated.
        """
        ret = any([child.semantic_analysis(messenger) for child in list(self._children)])
        return ret

    def generate_llvm(self) -> str:
        """
        Generates the corresponding node into llvm instructions.
        :return: generates the instructions as a string
        """
        ret = ""
        for child in self._children:
            ret += child.generate_llvm()

        return ret

    def _is_global(self) -> bool:
        return self._parent_node._is_global()
