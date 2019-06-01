"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from typing import List

import Specifiers


def convert_operator_stack_to_str(operator_stack: List[Specifiers.DeclaratorSpecifier]) -> str:
    """
    Converts operator stack to a string
    :param operator_stack: The stack of declaratorSpecifiers
    :return: Operator stack in string notation
    """
    return "*" * len(operator_stack[:-1])


def llvm_allocate_instruction(target_register: str, spec_type: Specifiers.TypeSpecifier, operator_stack) -> str:
    """
    :param target_register:
    :param spec_type:
    :param operator_stack:
    :return: Code string
    """

    operator_string = convert_operator_stack_to_str(operator_stack)

    return "%{0} alloca = {1}{2}, align {3}".format(
        target_register, spec_type.llvm_type, operator_string, spec_type.llvm_alignment)


def llvm_store_instruction(source_type: Specifiers.TypeSpecifier, source_register: str,
                           source_operator_stack: List[Specifiers.DeclaratorSpecifier],
                           target_type: Specifiers.TypeSpecifier, target_register: str,
                           target_operator_stack: List[Specifiers.DeclaratorSpecifier],
                           indent_string: str) -> str:
    """

    :param indent_string: The indentation string of the code
    :param source_type: The type specifier of the source value
    :param source_register: The register of the source
    :param source_operator_stack: The extra operator stack (*, [], () ...)
    :param target_type: Type of the target where we store.
    :param target_register: Register of target.
    :param target_operator_stack: Target's operator stack.
    :return: a String of result llvm code
    """
    s_operator_string = convert_operator_stack_to_str(source_operator_stack)
    t_operator_string = convert_operator_stack_to_str(target_operator_stack)
    ret = indent_string + "store {0}{1} %{2}, {3}{4}* %{5}, align {6}\n".format(
        source_type.llvm_type,
        s_operator_string,
        source_register,
        target_type.llvm_type,
        t_operator_string,
        target_register,
        source_type.llvm_alignment
    )
    return ret


def llvm_load_instruction(source_type: Specifiers.TypeSpecifier, source_register: str,
                          source_operator_stack: List[Specifiers.DeclaratorSpecifier],
                          target_type: Specifiers.TypeSpecifier, target_register: str,
                          target_operator_stack: List[Specifiers.DeclaratorSpecifier],
                          indent_string: str) -> str:
    """

      :param indent_string: The indentation string of the code
      :param source_type: The type specifier of the source value
      :param source_register: The register of the source
      :param source_operator_stack: The extra operator stack (*, [], () ...)
      :param target_type: Type of the target where we store.
      :param target_register: Register of target.
      :param target_operator_stack: Target's operator stack.
      :return: a String of result llvm code
      """
    s_operator_string = convert_operator_stack_to_str(source_operator_stack)
    t_operator_string = convert_operator_stack_to_str(target_operator_stack)

    ret = indent_string + " %{0} = load {1}{2}, {3}{4}* %{5}, align {6}\n".format(
        target_register,
        target_type.llvm_type,
        t_operator_string,

        source_type.llvm_type,
        s_operator_string,
        source_register,
        source_type.llvm_alignment
    )

    return ret
