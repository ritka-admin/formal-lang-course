parser grammar LaLaLangParser;

@header {
    package com.github.ritka_admin.formal-lang-course.language;;
}

options {
  tokenVocab=LaLaLangLexer;
}

program
    : stmt* EOF
    ;

stmt
    : initializerStmt SEMICOLON
    | assignmentStmt SEMICOLON
    | printStmt SEMICOLON
    ;

expr
    : atom
    | funcExpr
    | lambda
    ;

funcExpr
    : identifier OPEN_PARENS ((arg)? | arg (COMMA arg)+) CLOSE_PARENS
    ;

lambda
    : LAMBDA list ARROW expr
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
    | identifier
    ;

primitives
    : (NUMBER | STRING | TRUE | FALSE)
    ;

collection
    : list
    | set
    ;

list
    : OPEN_SQUARE ((atom)? | atom (COMMA atom)+) CLOSE_SQUARE
    ;

set
    : OPEN_BRACE ((primitives)? | primitives (COMMA primitives)+) CLOSE_BRACE
    ;

identifier
    : NAME
    ;

