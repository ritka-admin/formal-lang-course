lexer grammar LaLaLangLexer;

TRUE: 'True';
FALSE: 'False';

VAR: 'var';
PRINT: 'print';
ASSIGNMENT: '=';
SEMICOLON: ';';
COMMA: ',';
LAMBDA: '\\';
ARROW: '->';
INTERSECT: '&';
UNION: '|';
PLUS: '+';
KLEENE: '*';

OPEN_PARENS: '(';
CLOSE_PARENS: ')';
OPEN_BRACE: '{';
CLOSE_BRACE: '}';
OPEN_SQUARE: '[';
CLOSE_SQUARE: ']';

FUNCNAME: ('set_start' | 'set_final' | 'add_start' |
'add_final' | 'get_start' | 'get_final' | 'get_reachable' |
'get_vertices' | 'get_edges' | 'get_labels' | 'map' | 'filter'
| 'load');

fragment DIGIT: [0-9];
NUMBER: [1-9] DIGIT* | DIGIT;

fragment LETTER: [a-zA-Z];
fragment INPUT_CHARACTER: ~[\r\n\u0085\u2028\u2029];
NAME: ('_' | LETTER)+;
STRING: '"' INPUT_CHARACTER* '"';

fragment NEW_LINE:    '\n';
fragment WHITE_SPACE: [ \t];
SPACE:   (WHITE_SPACE | NEW_LINE)+ -> skip;