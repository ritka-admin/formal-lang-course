lexer grammar LaLaLangLexer;

@header {
    package com.github.ritka_admin.formal-lang-course.language;
}

TRUE: 'True';
FALSE: 'False';

VAR: 'var';
PRINT: 'print';
ASSIGNMENT: '=';
SEMICOLON: ';';
COMMA: ',';
LAMBDA: '\\';
ARROW: '->';

OPEN_PARENS: '(';
CLOSE_PARENS: ')';
OPEN_BRACE: '{';
CLOSE_BRACE: '}';
OPEN_SQUARE: '[';
CLOSE_SQUARE: ']';

fragment DIGIT: [0-9];
NUMBER: [1-9] DIGIT* | DIGIT;

fragment LETTER: [a-zA-Z];
fragment INPUT_CHARACTER: ~[\r\n\u0085\u2028\u2029];
NAME: ('_' | LETTER)+;
STRING: '"' INPUT_CHARACTER* '"';

fragment NEW_LINE:    '\n';
fragment WHITE_SPACE: [ \t];
SPACE:   (WHITE_SPACE | NEW_LINE)+ -> skip;