"""
 Author: Robbe Heirman
 Project: Simple C Compiler
 Course: Compilers
 Academic Year: 2018-2019
"""
from source.gen.CListener import CListener
from source.gen.CParser import CParser


class CListenerExtend(CListener):
    """
    Extension the Generated Antlr CListener.
    Responsible for building the AST
    """

    def enterDeclaration(self, ctx: CParser.DeclarationContext):
        """
        Handles a declaration statement. the identifier needs to be added to the symbol table with corresponding
        attributes. Also handles semantic errors like a redeclaration of an identifier.
        :param ctx:
        """
        base_type = None
        for i in range(ctx.getChildCount()):
            child = ctx.getChild(i).getPayload()
            print(type(ctx.getChild(i).getPayload()))

            if isinstance(child, CParser.Base_typeContext):
                print("yay!")