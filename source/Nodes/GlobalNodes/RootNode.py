"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""

import Nodes.AbstractNodes.ScopedNode as ScopedNode
import SymbolTable
from Nodes.DeclarationNodes.IncludeStatementNode import IncludeStatementNode
from Nodes.FunctionNodes.FuncDefNode import FuncDefNode


class RootNode(ScopedNode.ScopedNode):
    """
    The root of our program. Root is a ScopedNode, the base scope of our C program.
    """
    label = "Root"
    _index_counter = 0
    _indent_level = 0

    _REGISTER_LIST = ['t0', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 's0', 's1', 's3'
        , 's4', 's5', 's6', 's7']
    # Built-ins
    # ==================================================================================================================
    def __init__(self, ctx):
        super().__init__(None, ctx)

        self._symbol_table = SymbolTable.GlobalSymbolTable()

        self._index_counter: int = 0
        self._indent_level: int = 0

        self._index = 0

        self._register_list = list(self._REGISTER_LIST)
        self._register_list.reverse()

    # Ast-visuals
    # ==================================================================================================================
    def assign_index(self):
        self._index_counter += 1
        return self._index_counter

    # Semantic analysis
    # ==================================================================================================================
    def is_in_table(self, lexeme: str) -> bool:
        """
        Checks if a lexeme is already in the symbol table
        :param lexeme: The lexeme that needs to be returned
        :return: bool if successful = true else false
        """

        return self._symbol_table.is_in_symbol_table(lexeme)

    def is_in_global_table(self, lexeme: str):
        return self.is_in_table(lexeme)

    def get_attribute(self, lexeme):
        return self._symbol_table.get_attribute(lexeme)

    def is_global(self):
        return True

    def find_while_sw_node(self):
        return 0

    # LLVM Code
    # ==================================================================================================================

    def generate_llvm(self, c_comment: bool = True):
        self._indent_level = 0
        return super().generate_llvm(c_comment)

    def increase_code_indent(self):
        self._indent_level += 1

    def decrease_code_indent(self):
        self._indent_level -= 1

    @property
    def code_indent_level(self):
        return self._indent_level

    def llvm_count_declared_scopes(self, id) -> int:
        return 0

    def llvm_found_in_n_scope(self, id, found_first=False):
        return 0

    # Mips Code
    # ==================================================================================================================

    def generate_mips(self, c_comment: bool = True):
        ret = "#" * 72 + "\n"
        ret += ".data\n"

        data_ret = ""
        text_ret = ""
        for child in self._children:
            if isinstance(child, FuncDefNode) or isinstance(child, IncludeStatementNode):
                text_ret += child.generate_mips(c_comment)

            else:

                data_ret += child.generate_mips(c_comment)

        ret += data_ret
        ret += "#" * 72 + "\n"
        ret += ".text\n"
        ret += "\n"
        # We always start by calling main
        ret += "jal .main # .enter is not supported by mars, using this to emulate behaviour\n"

        # Now we cleanly exit We will return the return of main as exit code
        # Load 17 in to v0 10 = exit (end of program)
        ret += "\n# .exit is also not supported so use next part to emulate behaviour\n"
        ret += "move $a0 $v0  # We move the return value of main for syscall\n"
        ret += "li $v0, 17 # System call code for end of program\n"
        ret += "syscall\n\n"

        ret += text_ret
        ret += "#" * 72
        return ret

    def mips_register_reserve(self) -> str:
        return self._register_list.pop()

    def mips_register_free(self, reg: str):
        self._register_list.append(reg)

    def mips_registers_in_use(self):
        l1 = [item for item in self.__class__._REGISTER_LIST if item not in self._register_list]
        return l1

    def top_register(self):
        return self._register_list[-1]
