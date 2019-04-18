grammar C;

// Rules
// =====================================================================================================================
statements
    :statement*
    ;

statement
    : assignment
    | decl_list SEMICOLON
    | func_def
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
    : prefix_operator* ID postfix_operator?
    ;

prefix_operator
    : ASTERIX
    | ADDRESS
    ;

postfix_operator
    : ARRAY
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
    : ID
    ;

constant
    : CHARACTER_C
    | NUMERAL_C
    | FLOAT_C
    ;

func_def
    : base_type ASTERIX* ID LPARANT parameter_list RPARANT LBRACES statements RBRACES
    ;

// =====================================================================================================================
// =====================================================================================================================
/** Tokens */
// =====================================================================================================================

/** Operators */
// =====================================================================================================================

// Unary operators

ADDRESS: '&';
ARRAY: '[]';
INCEREMENT: '++';
DECREMENT: '--';

// Binary operators
EQ: '=';
POWER: '^';
DIVIDE: '/';
ADD: '+';
SUB: '-';

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
//======================================================================================================================

// types
// =====================================================================================================================

CHAR: 'char';
FLOAT: 'float';
INT: 'int';
// =====================================================================================================================

// identifier(s) & literals
// =====================================================================================================================

ID: NONDIGIT_ID (NONDIGIT_ID | DIGIT)*;
WS: [ \n\t\r]+ -> skip;

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
