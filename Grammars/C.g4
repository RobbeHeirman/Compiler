grammar C;

// Rules
// =====================================================================================================================
statements
    :statement* EOF;

statement
    : decleration SEMICOLON
    ;

decleration
    : type ID
    ;

type
    : CHAR
    | FLOAT
    | INT
    ;
// =====================================================================================================================
// =====================================================================================================================
/** Tokens */
// =====================================================================================================================

/** Operators */
// ======================================================================================================================

// Binary operators
EQ: '=';

// Special Operators
SEMICOLON: ';';
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
