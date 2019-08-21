"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
import Nodes.GlobalNodes.RootNode as RootNode
import messages


class AST:
    """
    Representation of the Abstract syntax tree.
    This is the interface of the underlying tree.
    All functionality we need from the AST can be accessed trough this interface.
    """
    # Type Annotations
    _root: RootNode.RootNode

    # Built-ins
    # ==================================================================================================================
    def __init__(self, filename, stream=None):
        """
        Initializer
        """
        self._root = None
        self._messenger = messages.MessageGenerator(filename, stream)

    # AST-Visuals
    # ==================================================================================================================
    def to_dot(self, filename):
        """
        Generates a string, in dot language format. That can be used as a visual representation for the AST.
        :return:
        """
        if self._root is None:
            print("AST not initialized")
            return

        graph_string = "graph{\n"
        graph_string += self._root.dot_string()
        graph_string += "}\n"
        file = open(filename, 'w')
        file.write(graph_string)
        file.close()

    # AST-Generation
    # ==================================================================================================================
    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, root):
        self._root = root

    # Semantic analysis
    # ==================================================================================================================
    def semantic_analysis(self) -> bool:
        """
        Does the semantic analysis of our program.
        Will fill in & check the symbol table(s) (Scoped)
        The messageGenerator is used to generate messages
        :return: True if the program is semantically correct.
        """
        return self._root.semantic_analysis(self._messenger)

    def error_count(self) -> int:
        return self._messenger.error_counter

    def warning_count(self) -> int:
        return self._messenger.warning_counter

    def constant_folding(self):
        self._root.constant_folding()

    # Generate LLVM
    # ==================================================================================================================
    def generate_llvm(self) -> str:
        """
        Generates the LLVM instruction code
        :return: a string with the llvm instructions of this ast.
        """

        return self._root.generate_llvm()

    # Generate MIPS
    # ==================================================================================================================
    def generate_mips(self) -> str:
        """
        Generates MIPS instruction Code.
        :return: The string with mips instructions
        """

        return self._root.generate_mips()
