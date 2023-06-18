parser grammar LaLaLangParser;

options {
  tokenVocab=LaLaLangLexer;
}

program
    : (stmts+=stmt)* EOF
    ;

stmt
    : initializerStmt SEMICOLON #iniStmt
    | assignmentStmt SEMICOLON  #assStmt
    | printStmt SEMICOLON       #priStmt
    ;

expr
    : atom                          #atomExpr
    | funcExpr                      #func
    | lambdaFunc                    #lambda
    | lhs=expr INTERSECT rhs=expr   #interExpr      // пересечение
    | lhs=expr UNION rhs=expr       #unionExpr      // объединение
    | lhs=expr PLUS rhs=expr        #plusExpr       // конкатенация
    | expr KLEENE                   #kleeneExpr     // звезда Клини
    ;

funcExpr
    : FUNCNAME OPEN_PARENS ((arg)? | arg (COMMA arg)+) CLOSE_PARENS
    ;

lambdaFunc
    : LAMBDA listVars ARROW expr
    ;

initializerStmt
    : VAR identifier ASSIGNMENT expr
    ;

assignmentStmt
    : identifier ASSIGNMENT expr
    ;

printStmt
    : PRINT OPEN_PARENS expr CLOSE_PARENS
    ;

atom
    : identifier
    | primitives
    | collection
    ;

arg
    : expr
    | primitives
    | collection
    | identifier
    ;

primitives
    : number
    | string
    | bool
    ;

collection
    : listVars
    | setVars
    ;

listVars
    : OPEN_SQUARE ((atom)? | atom (COMMA atom)+) CLOSE_SQUARE
    ;

setVars
    : OPEN_BRACE ((primitives)? | primitives (COMMA primitives)+) CLOSE_BRACE
    ;

number
    : value=NUMBER
    ;

string
    : value=STRING
    ;

bool
    : true
    | false
    ;

true: TRUE;
false: FALSE;

identifier
    : value=NAME
    ;

