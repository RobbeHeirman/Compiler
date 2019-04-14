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

simple_declaration // int a, char foo....
    : base_type declarator (COMMA declarator)*
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
    : lhs EQ rhs SEMICOLON
    ;

lhs // all possible L values
    : ID
    | simple_declaration
    ;

rhs // Possible R values
    : constant
    ;

constant
    : character
    | numeral
    |
    ;

character

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
