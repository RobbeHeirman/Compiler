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
    ;

decl_list
    : base_type simple_declaration (COMMA simple_declaration)*
    ;

simple_declaration // int a, char foo....
    :  declarator (EQ rhs)?
    ;

base_type
    : CHAR
    | FLOAT
    | INT
    ;

declarator // optional prefix operator sequence + optional postfix operator
    : (ASTERIX)* ID postfix_operator?
    ;

postfix_operator
    : LEFT_BRACKET rhs? RIGHT_BRACKET
    | function_operator
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
    : ID EQ rhs SEMICOLON
    ;

rhs // Possible R values
    : constant
    | id_rhs
    | SUB rhs
    | LPARANT rhs RPARANT
    | <assoc=right> rhs POWER rhs
    | rhs (INCEREMENT | DECREMENT)
    | rhs (ASTERIX | DIVIDE) rhs
    | rhs (ADD | SUB) rhs
    ;

id_rhs
    : (ADDRESS | ASTERIX)* ID rhs_postfix?
    ;
rhs_postfix
    : LPARANT (rhs (COMMA rhs)*)? RPARANT
    | LEFT_BRACKET rhs RIGHT_BRACKET
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
    : RETURN rhs
    ;

selection_statements
    : if_statement
    ;


if_statement
    : IF cond_statement (ELSE IF cond_statement)* (ELSE LBRACES statements RBRACES)?
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
