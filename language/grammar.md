## Абстрактный синтаксис

```
prog = List<stmt>

stmt =
    bind of var * expr
  | print of expr

val =
    String of string
  | Int of int
  | Bool of bool
  | Set of set
  | List of list

expr =
    Var of var                   // переменные
  | Val of val                   // константы
  | Set_start of Set<val> * expr // задать множество стартовых состояний
  | Set_final of Set<val> * expr // задать множество финальных состояний
  | Add_start of Set<val> * expr // добавить состояния в множество стартовых
  | Add_final of Set<val> * expr // добавить состояния в множество финальных
  | Get_start of expr            // получить множество стартовых состояний
  | Get_final of expr            // получить множество финальных состояний
  | Get_reachable of expr        // получить все пары достижимых вершин
  | Get_vertices of expr         // получить все вершины
  | Get_edges of expr            // получить все рёбра
  | Get_labels of expr           // получить все метки
  | Map of lambda * expr         // классический map
  | Filter of lambda * expr      // классический filter
  | Load of path                 // загрузка графа
  | Intersect of expr * expr     // пересечение языков
  | Concat of expr * expr        // конкатенация языков
  | Union of expr * expr         // объединение языков
  | Star of expr                 // замыкание языков (звезда Клини)
  | Smb of expr                  // единичный переход

lambda = \ list<var> -> expr
```

## Примеры

- Объявление перемнной

  `var x = 5;`
  
- Присвоение значения переменной
  
  `x = 5;`
  
- Передача невычисленного выражения как аргумента функции

  `set_final({get_vertices(graph)}, graph)`
  
- Загрузить граф из файла и сделать все его вершины стартовыми:

  ```
  var graph = load("/path/to/the/file");
  var res = set_start({get_vertices(graph)}, graph);
  ```

- Сделать выборочные вершины стартовыми / финальными
  
  ```
  var resGraph = set_start({1, 2, 3}, graph);
  var resGraph0 = set_final({4, 5, 6}, graph);
  ```
  
- Добавить стартовое / финальное состояние

  ```
  resGraph = add_start({4}, graph);
  resGraph0 = add_final({0}, graph);
  ```
  
- Получить все пары достижимых вершин конкретного графа и функция того же функционала, ожидающая аргумент
  
  ```
  var allPairs = get_reachable(graph);
  var allPairs0 = \[g] -> get_reachable(g);
  ```
  
- Получить стартовые вершины, аналогичные тем, что есть в другом графе
  
  ```
  vert = get_vertices(graph);
  var lambdaFunc = \[a] -> a elem vert;
  similarVert = filter(lambdaFunc, {get_vertices(graph0)};
  print(similarVert);
  ```
  
