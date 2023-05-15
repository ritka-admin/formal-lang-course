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
    : atom
    | funcExpr
    | lambdaFunc
    | expr INTERSECT expr  // пересечение
    | expr UNION expr      // объединение
    | expr PLUS expr       // конкатенация
    | expr KLEENE          // звезда Клини
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
    : OPEN_BRACE expr CLOSE_BRACE
    | collection
    | identifier
    ;

primitives
    : (NUMBER | STRING | TRUE | FALSE)
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

identifier
    : NAME
    ;

