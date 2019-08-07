grammar C;

// Rules
// =====================================================================================================================
    root
    : global_statement* EOF
    ;

    global_statement
    : decl_list
    | func_def
    | include_statement
    ;

    statements
    : statement*
    ;

statement

    : decl_list
    | func_def
    | ret_statement SEMICOLON
    | expression SEMICOLON
    | branch
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
    : LPARANT declarator RPARANT # ignore_declarator
    | declarator postfix_operator # normal_declarator
    | ptr_decl declarator         # normal_declarator
    //| LPARANT id_decl RPARANT
    | id_decl  # id_declarator
    | # epsilon
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

lhs // L value nodes
    : lhs expression_postfix
    | expression_prefix lhs
    | id_expression
    ;


expression // Possible R values
    // Constants and identifier's have highes precedence
    : constant # ignore_expression
    | id_expression # ignore_expression
    | SUB expression # ignore_expression

    // Followed by their modifier's
    | expression expression_postfix # fix_expression
    | expression_prefix expression  # fix_expression

    // Followed by ( expr )
    | LPARANT expression RPARANT # ignore_expression

    // Binary operator's in precdence order
    | <assoc=right> expression POWER expression # binary_operator
    | expression (INCEREMENT | DECREMENT) # binary_operator
    | expression (ASTERIX | DIVIDE) expression # binary_operator
    | expression (ADD | SUB) expression # binary_operator

    //
    | expression cond_operator expression # condition

    // Assignment operator
    | expression  EQ expression #assignment_expression
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

cond_operator
    : EQ EQ
    | SMALLER
    | BIGGER;

 // Functions
 // ====================================================================================================================
func_def
    : base_type func_declarator LBRACES statements RBRACES
    ;

func_declarator
    : LPARANT func_declarator RPARANT
    | func_declarator postfix_operator
    | ptr_decl func_declarator
    | w_p_id function_operator
    ;

w_p_id:
    LPARANT w_p_id RPARANT
    | id_decl
    ;

ret_statement
    : RETURN (expression)?
    ;

include_statement
    :'#include'SMALLER 'stdio.h' BIGGER
    ;

/** Branching*/
// =====================================================================================================================

branch: c_if (c_elif)* (c_else)?;

c_if : IF LPARANT expression RPARANT LBRACES statements RBRACES;
c_elif: ELSE IF LPARANT expression RPARANT LBRACES statements RBRACES;
c_else: ELSE LBRACES statements RBRACES;

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
