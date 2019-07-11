grammar C;

// Rules
// =====================================================================================================================
    root
    : global_statement* EOF
    ;

    global_statement
    : decl_list
    | func_def
    ;

    statements
    : statement*
    ;

statement
    : assignment
    | decl_list
    | func_def
    | ret_statement SEMICOLON
    | selection_statements
    | while_statement
    | include_statement
    | expression SEMICOLON
    ;

decl_list
    : base_type simple_declaration (COMMA simple_declaration)* SEMICOLON
    ;

simple_declaration // int a, char foo....
    :  declarator (EQ (array_init | expression))?
    ;

array_init
    : LBRACES expression (COMMA expression)* RBRACES
    ;

base_type
    : CHAR
    | FLOAT
    | INT
    ;

declarator // optional prefix operator sequence + optional postfix operator
    : LPARANT declarator RPARANT
    | declarator postfix_operator
    | ptr_decl declarator
    | LPARANT id_decl RPARANT
    | id_decl
    ;

ptr_decl
    : ASTERIX
    ;

id_decl:
    ID
    ;

postfix_operator
    : array_operator
    | function_operator
    ;

array_operator
    :
    LEFT_BRACKET expression? RIGHT_BRACKET
    ;
function_operator
    : LPARANT parameter_list RPARANT
    ;

parameter_list
    : (param (COMMA param)*)?
    ;

param
    : base_type declarator
    ;
assignment // a = 4;, int b = a;
    : lhs EQ expression SEMICOLON
    ;

lhs // L value nodes
    : lhs expression_postfix
    | expression_prefix lhs
    | id_expression
    ;

expression // Possible R values
    : constant # ignore_expression
    | expression expression_postfix # postfix_expression
    | expression_prefix expression  # prefix_expression
    | id_expression # ignore_expression
    | SUB expression # ignore_expression
    | LPARANT expression RPARANT # ignore_expression
    | <assoc=right> expression POWER expression # ignore_expression
    | expression (INCEREMENT | DECREMENT) # ignore_expression
    | expression (ASTERIX | DIVIDE) expression # ignore_expression
    | expression (ADD | SUB) expression # ignore_expression
    ;

id_expression
    : ID
    ;

expression_prefix
    : expression_addr
    | ptr_decl
    ;

expression_addr
    : ADDRESS
    ;

expression_postfix
    : expression_function_operator
    | array_operator
    ;

expression_function_operator
    : LPARANT expression_param_list RPARANT
    ;

expression_param_list
    : (expression (COMMA expression)*)?
    ;

constant
    : character_constant
    | integer_constant
    | floating_constant
    ;

character_constant
    : CHARACTER_C
    ;

integer_constant
    : NUMERAL_C
    ;

floating_constant
    : FLOAT_C
    ;

func_def
    : base_type declarator LPARANT parameter_list RPARANT LBRACES statements RBRACES
    ;

ret_statement
    : RETURN (expression)?
    ;

selection_statements
    : if_statement (else_if_statement)* (else_statement)?
    ;


if_statement
    : IF cond_statement
    ;

else_if_statement
    : ELSE IF cond_statement
    ;

else_statement
    : ELSE LBRACES statements RBRACES
    ;
while_statement
    : WHILE cond_statement
    ;

cond_statement
    :LPARANT condition RPARANT LBRACES statements RBRACES
    ;
condition
    : expression cond_operator expression
    ;

cond_operator
    : EQ EQ
    | SMALLER
    | BIGGER;

include_statement
    :'#include'SMALLER 'stdio.h' BIGGER
    ;

// =====================================================================================================================
// =====================================================================================================================
/** Tokens */
// =====================================================================================================================

/** Operators */
// =====================================================================================================================

// Unary operators

ADDRESS: '&';
INCEREMENT: '++';
DECREMENT: '--';

// Binary operators
EQ: '=';
POWER: '^';
DIVIDE: '/';
ADD: '+';
SUB: '-';
SMALLER: '<';
BIGGER: '>';
// Special Operators
SEMICOLON: ';';
COMMA: ',';
S_QUOTE: '\'';
POINT: '.';
LPARANT: '(';
RPARANT: ')';
ASTERIX: '*';
LBRACES: '{';
RBRACES: '}';
LEFT_BRACKET: '[';
RIGHT_BRACKET: ']';

//======================================================================================================================

// types
// =====================================================================================================================

CHAR: 'char';
FLOAT: 'float';
INT: 'int';

// =====================================================================================================================

// Keywords
// =====================================================================================================================
RETURN: 'return';
IF: 'if';
ELSE: 'else';
WHILE: 'while';


// identifier(s) & literals
// =====================================================================================================================

ID: NONDIGIT_ID (NONDIGIT_ID | DIGIT)*;


fragment NONDIGIT_ID: [a-zA-Z_];
fragment DIGIT: [0-9];



CHARACTER_C: S_QUOTE (~['\\\r\n\u0085\u2028\u2029] | COMMONCHARACTER)  S_QUOTE;

fragment COMMONCHARACTER
    : SIMPLEESCAPESEQUENCE
    ;

fragment SIMPLEESCAPESEQUENCE // TODO: Extend
    : '\\\''
    | '\\"'
    | '\\\\'
    | '\\0'
    | '\\a'
    | '\\b'
    | '\\f'
    | '\\n'
    | '\\r'
    | '\\t'
    | '\\v'
    ;

NUMERAL_C: DIGIT (DIGIT| '_')*;  // TODO: extend (binary, hexadecimal...)

FLOAT_C: [0-9][0-9_]* ( ([eE] [-+]? [0-9][0-9_]*) | '.' [0-9][0-9_]* ([eE] [-+]? [0-9][0-9_]*)?);

WS: [ \n\t\r]+ -> skip;
BLOCK_COMMENT: '/*' .*? '*/' -> skip;
LINE_COMMENT: '//' ~[\r\n]* -> skip;
