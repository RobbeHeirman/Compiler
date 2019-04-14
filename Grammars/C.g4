grammar C;

// Rules
// =====================================================================================================================
statements
    :statement* EOF;

statement
    :assignment
    |declaration
    ;

declaration // specifier(optional)/base type/declarator/initializer(optional) (ref. C++ the programming language, p79)
    : simple_declaration SEMICOLON // the simpelest form like: int a, int*a [];
    ;

simple_declaration // int a, char foo....
    : base_type declarator (EQ rhs)? (COMMA declarator (EQ rhs)?)*
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
    : DEREFERENCE
    | ADDRESS
    ;

postfix_operator
    : ARRAY
    ;

assignment // a = 4;, int b = a;
    : ID EQ rhs SEMICOLON
    ;

rhs // Possible R values
    : constant
    ;

constant
    : CHARACTER_C
    | NUMERAL_C
    | FLOAT_C
    ;

// =====================================================================================================================
// =====================================================================================================================
/** Tokens */
// =====================================================================================================================

/** Operators */
// =====================================================================================================================

// Unary operators
DEREFERENCE: '*';
ADDRESS: '&';
ARRAY: '[]';

// Binary operators
EQ: '=';

// Special Operators
SEMICOLON: ';';
COMMA: ',';
S_QUOTE: '\'';
POINT: '.';
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
