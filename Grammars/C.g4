grammar C;

// Rules
// =====================================================================================================================
statements
    :statement* EOF;

statement
    : declaration
    ;

declaration // specifier(optional)/base type/declarator/initializer(optional) (ref. C++ the programming language, p79)
    : simple_declaration SEMICOLON // the simpelest form like: int a, int*a [];
    ;

simple_declaration
    : base_type declarator
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
// =====================================================================================================================
// =====================================================================================================================
/** Tokens */
// =====================================================================================================================

/** Operators */
// ======================================================================================================================

// Unary operators
DEREFERENCE: '*';
ADDRESS: '&';
ARRAY: '[]';

// Binary operators
EQ: '=';

// Special Operators
SEMICOLON: ';';
COMMA: ',';
//======================================================================================================================

// types
// =====================================================================================================================

CHAR: 'char';
FLOAT: 'float';
INT: 'int';
// =====================================================================================================================

// identifier(s) & literals
// =====================================================================================================================

ID: [_a-zA-Z] [_a-zA-Z0-9]*;
WS: [ \n\t\r]+ -> skip;
