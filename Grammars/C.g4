grammar C;

// Rules
// =====================================================================================================================
    statements
    : statement*
    ;

statement
    : assignment
    | decl_list SEMICOLON
    | func_def
    | ret_statement SEMICOLON
    | selection_statements
    | while_statement
    | include_statement
    | rhs SEMICOLON
    ;

decl_list
    : base_type simple_declaration (COMMA simple_declaration)*
    ;

simple_declaration // int a, char foo....
    :  declarator (EQ (array_init | rhs))?
    ;

array_init
    : LBRACES rhs (COMMA rhs)* RBRACES
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
    LEFT_BRACKET rhs? RIGHT_BRACKET
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
    : lhs EQ rhs SEMICOLON
    ;

lhs // L value nodes
    : lhs rhs_postfix
    | rhs_prefix lhs
    | id_rhs
    ;

rhs // Possible R values
    : constant
    | rhs rhs_postfix
    | rhs_prefix rhs
    | id_rhs
    | SUB rhs
    | LPARANT rhs RPARANT
    | <assoc=right> rhs POWER rhs
    | rhs (INCEREMENT | DECREMENT)
    | rhs (ASTERIX | DIVIDE) rhs
    | rhs (ADD | SUB) rhs
    ;

id_rhs
    : ID
    ;

rhs_prefix
    : rhs_addr
    | ptr_decl
    ;

rhs_addr
    : ADDRESS
    ;

rhs_postfix
    : rhs_function_operator
    | array_operator
    ;

rhs_function_operator
    : LPARANT rhs_param_list RPARANT
    ;

rhs_param_list
    : (rhs (COMMA rhs)*)?
    ;

constant
    : CHARACTER_C
    | NUMERAL_C
    | FLOAT_C
    ;

func_def
    : base_type ASTERIX* ID LPARANT parameter_list RPARANT LBRACES statements RBRACES
    ;

ret_statement
    : RETURN (rhs)?
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
    : rhs cond_operator rhs
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
