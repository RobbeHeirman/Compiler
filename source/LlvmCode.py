"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
import typing
import Specifiers


def convert_operator_stack_to_str(operator_stack: typing.List[Specifiers.TypeModifier]) -> str:
    """
    Converts operator stack to a string
    :param operator_stack: The stack of declaratorSpecifiers
    :return: Operator stack in string notation
    """
    ret_str = ""
    for operator in operator_stack:
        ret_str += operator.modifier_type.value
    return ret_str


def llvm_allocate_instruction(target_register: str, operator_stack,
                              indent_string: str) -> str:
    """
    :param target_register:
    :param operator_stack:
    :param indent_string:
    :return: Code string
    """

    operator_string = convert_operator_stack_to_str(operator_stack)

    return indent_string + "%{0} = alloca {1}{2}\n".format(
        target_register, operator_stack[0].llvm_type, operator_string)


def llvm_store_instruction(source_register: str,
                           source_operator_stack: typing.List[Specifiers.TypeModifier],
                           target_register: str,
                           target_operator_stack: typing.List[Specifiers.TypeModifier],
                           indent_string: str) -> str:
    """

    :param indent_string: The indentation string of the code
    :param source_register: The register of the source
    :param source_operator_stack: The extra operator stack (*, [], () ...)
    :param target_register: Register of target.
    :param target_operator_stack: Target's operator stack.
    :return: a String of result llvm code
    """
    s_operator_string = convert_operator_stack_to_str(source_operator_stack)
    t_operator_string = convert_operator_stack_to_str(target_operator_stack)
    ret = indent_string + "store {0}{1} %{2}, {3}{4}* %{5}\n".format(
        source_operator_stack[0].llvm_type,
        s_operator_string,
        source_register,
        target_operator_stack[0].llvm_type,
        t_operator_string,
        target_register,
        # source_type.llvm_alignment
    )
    return ret


def llvm_store_instruction_c(source_type, source_constant: str, target_type, target_register: str, indent_string: str) \
        -> str:
    """

    :param indent_string: The indentation string of the code
    :param source_type: The type specifier of the source value
    :param source_constant: The source constant
    :param target_type: Type of the target where we store.
    :param target_register: Register of target.
    :return: a String of result llvm code
    """
    s_operator_string = convert_operator_stack_to_str(source_type)
    t_operator_string = convert_operator_stack_to_str(target_type)
    ret = indent_string + "store {0}{1} {2}, {3}{4}* %{5}\n".format(
        source_type[0].llvm_type,
        s_operator_string,
        source_constant,
        target_type[0].llvm_type,
        t_operator_string,
        target_register
        # source_type.llvm_alignment
    )
    return ret


def llvm_load_instruction(source_register: str,
                          source_operator_stack: typing.List[Specifiers.TypeModifier], target_register: str,
                          target_operator_stack: typing.List[Specifiers.TypeModifier],
                          indent_string: str) -> str:
    """

      :param indent_string: The indentation string of the code
      :param source_register: The register of the source
      :param source_operator_stack: The extra operator stack (*, [], () ...)
      :param target_register: Register of target.
      :param target_operator_stack: Target's operator stack.
      :return: a String of result llvm code
      """
    s_operator_string = convert_operator_stack_to_str(source_operator_stack)
    t_operator_string = convert_operator_stack_to_str(target_operator_stack)

    ret = indent_string + "%{0} = load {1}{2}, {3}{4}* %{5}\n".format(
        target_register,
        source_operator_stack[0].llvm_type,
        t_operator_string,

        source_operator_stack[0].llvm_type,
        s_operator_string,
        source_register,
        # source_type.llvm_alignment
    )

    return ret


# Global
# ======================================================================================================================

def llvm_allocate_instruction_global(target_register: str, operator_stack, val,
                                     indent_string: str) -> str:
    """
    :param val:
    :param target_register:
    :param operator_stack:
    :param indent_string:
    :return: Code string
    """

    operator_string = convert_operator_stack_to_str(operator_stack)

    return indent_string + "@{0} = global {1}{2} {3}\n".format(
        target_register, operator_stack[0].llvm_type, operator_string, val)
