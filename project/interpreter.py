from project.types import *
from project.graphs import *
from project.reachibility import *
from project.finite_state_automaton import *

from pyformlang.finite_automaton import State
from language.antlr_gen.LaLaLangParserVisitor import LaLaLangParserVisitor
from language.antlr_gen.LaLaLangParser import LaLaLangParser

LOAD = 'load'
ADD_START = 'add_start'
ADD_FINAL = 'add_final'
GET_START = 'get_start'
GET_FINAl = 'get_final'
GET_REACHABLE = 'get_reachable'
GET_VERTICES = 'get_vertices'
GET_EDGES = 'get_edges'
GET_LABELS = 'get_labels'
MAP = 'map'                      # TODO
FILTER = 'filter'                # TODO

funcs = [LOAD, ADD_START, ADD_FINAL, GET_START, GET_FINAl, GET_REACHABLE, GET_VERTICES, GET_EDGES, GET_LABELS]


class Func:
    @staticmethod
    def load(inter, args, real_args):
        if len(real_args) == 1 and isinstance(real_args[0], LaLaString):
            graph = load_graph(real_args[0].value, SourceType.FILE)
            automaton = graph_to_nfa(graph, graph.nodes, graph.nodes)
            return LaLaFa(automaton)
        raise ValueError("Incorrect number or type of the arguments")

    @staticmethod
    def add_start(inter, args, real_args):
        if len(real_args) == 2 and isinstance(real_args[0], LaLaSet):
            automaton = args[1].accept(inter)
            if not isinstance(automaton, LaLaFa):
                raise TypeError("Second argument of 'set_start' should be graph")
            for v in real_args[0].value:
                automaton.value.add_start_state(State(v))
            return automaton
        raise ValueError("Incorrect number or type of the arguments")

    @staticmethod
    def add_final(inter, args, real_args):
        if len(real_args) == 2 and isinstance(real_args[0], LaLaSet):
            if isinstance(args[0], LaLaLangParser.ArgContext):
                automaton = args[1].accept(inter)
            else:
                automaton = args[0]
            if not isinstance(automaton, LaLaFa):
                raise TypeError("Second argument of 'set_start' should be graph")
            for v in real_args[0].value:
                automaton.value.add_final_state(State(v))
            return automaton
        raise ValueError("Incorrect number or type of the arguments")

    @staticmethod
    def get_start(inter, args, real_args):
        if len(real_args) == 1 and isinstance(real_args[0], LaLaFa):
            automaton = args[0].accept(inter)
            return LaLaSet(automaton.value.start_states)
        raise ValueError("Incorrect number or type of the arguments")

    @staticmethod
    def get_final(inter, args, real_args):
        if len(real_args) == 1 and isinstance(real_args[0], LaLaFa):
            automaton = args[0].accept(inter)
            return LaLaSet(automaton.value.final_states)
        raise ValueError("Incorrect number or type of the arguments")

    @staticmethod
    def get_vertices(inter, args, real_args):
        if len(real_args) == 1 and isinstance(real_args[0], LaLaFa):
            automaton = args[0].accept(inter)
            vertices = set()
            for vertex in automaton.value.states:
                vertices.add(vertex)
            return LaLaSet(vertices)
        raise ValueError("Incorrect number or type of the arguments")

    @staticmethod
    def get_edges(inter, args, real_args):
        if len(real_args) == 1 and isinstance(real_args[0], LaLaFa):
            automaton = args[0].accept(inter)
            edges = set()
            for v_from, label, v_to in automaton.value:
                edges.add((v_from, label, v_to))
            return LaLaSet(edges)
        raise ValueError("Incorrect number or type of the arguments")

    @staticmethod
    def get_labels(inter, args, real_args):
        if len(real_args) == 1 and isinstance(real_args[0], LaLaFa):
            automaton = args[0].accept(inter)
            labels = set()
            for _, label, _ in automaton.value:
                labels.add(label)
            return LaLaSet(labels)
        raise ValueError("Incorrect number or type of the arguments")

    @staticmethod
    def get_reachable(inter, args, real_args):
        if len(real_args) == 1 and isinstance(real_args[0], LaLaFa):
            automaton = args[0].accept(inter)
            v_reachable = find_reachable_for_each_vertex(automaton)
            return LaLaSet(v_reachable)
        raise ValueError("Incorrect number or type of the arguments")


class Interpreter(LaLaLangParserVisitor):

    def __init__(self, program: LaLaLangParser.ProgramContext):
        self.program = program
        self.lambda_arg = False
        self.lambda_body = False
        self.count_lambdas = 0
        self._local_vars = [dict()]
        self._local_vars = [dict()]
        self._global_vars = dict()
        self._global_vars['true'] = LaLaBool(True)
        self._global_vars['false'] = LaLaBool(False)

    def interpret(self):
        return self.program.accept(self)

    def visitProgram(self, ctx: LaLaLangParser.ProgramContext):
        for stmt in ctx.stmts:
            stmt.accept(self)

    def visitPriStmt(self, ctx: LaLaLangParser.PriStmtContext):
        child_node = ctx.printStmt().expr().accept(self)
        print(child_node.value)

    def visitInitializerStmt(self, ctx: LaLaLangParser.InitializerStmtContext):
        var_name = ctx.identifier().NAME().symbol.text
        value = ctx.expr().accept(self)
        self._global_vars[var_name] = value

    def visitAssStmt(self, ctx: LaLaLangParser.AssStmtContext):
        var_name = ctx.assignmentStmt().identifier().NAME().symbol.text
        if var_name not in self._global_vars.keys():
            raise NameError(f"{var_name} was not initialized")
        self._global_vars[var_name] = ctx.assignmentStmt().expr().accept(self)

    def visitFuncExpr(self, ctx: LaLaLangParser.FuncExprContext):
        func_name = ctx.FUNCNAME().getText()
        args = ctx.arg()

        real_args = []
        for arg in args:
            res = arg.accept(self)
            real_args.append(res)

        if self.count_lambdas:
            return func_name, real_args

        if func_name == LOAD:
            return Func.load(self, args, real_args)

        elif func_name == ADD_START:
            return Func.add_start(self, args, real_args)

        elif func_name == ADD_FINAL:
            return Func.add_final(self, args, real_args)

        elif func_name == GET_START:
            return Func.get_start(self, args, real_args)

        elif func_name == GET_FINAl:
            return Func.get_final(self, args, real_args)

        elif func_name == GET_VERTICES:
            return Func.get_vertices(self, args, real_args)

        elif func_name == GET_EDGES:
            return Func.get_edges(self, args, real_args)

        elif func_name == GET_LABELS:
            return Func.get_labels(self, args, real_args)

        elif func_name == GET_REACHABLE:
            return Func.get_reachable(self, args, real_args)

        elif func_name == FILTER:
            if len(real_args) == 2 and isinstance(real_args[0], LaLaLambda) \
                    and isinstance(real_args[1], LaLaCollection):
                pass

        elif func_name == MAP:
            if len(real_args) == 2 and isinstance(real_args[0], LaLaLambda) \
                    and isinstance(real_args[1], LaLaCollection):
                lambda_func = real_args[0]
                collection = real_args[1]
                if lambda_func.body[0] in funcs:
                    method = getattr(Func, lambda_func.body[0])
                    arguments = lambda_func.body[1]

                    for i, arg in enumerate(arguments):
                        if not isinstance(arg, LaLaType):
                            arguments[i] = self._local_vars[1][arguments[i][1]]

                    res = []
                    for elem in collection.value:
                        elem_res = method(self, [LaLaFa(elem)], [arguments[0], None])
                        res.append(elem_res)
                    return res

        raise NotImplementedError(f"No function with name {func_name}")

    def visitInterExpr(self, ctx: LaLaLangParser.InterExprContext):
        lhs = ctx.lhs.accept(self)
        rhs = ctx.rhs.accept(self)

        if isinstance(lhs, LaLaFa) and isinstance(rhs, LaLaFa):
            res = automaton_intersect(lhs.value, rhs.value)
            return LaLaFa(res)

        raise ValueError("Incorrect number or type of the arguments")

    def visitUnionExpr(self, ctx: LaLaLangParser.UnionExprContext):
        lhs = ctx.lhs.accept(self)
        rhs = ctx.rhs.accept(self)

        if isinstance(lhs, LaLaFa) and isinstance(rhs, LaLaFa):
            res = automatons_union(lhs.value, rhs.value)
            return LaLaFa(res)

        raise ValueError("Incorrect number or type of the arguments")

    def visitPlusExpr(self, ctx: LaLaLangParser.PlusExprContext):
        lhs = ctx.lhs.accept(self)
        rhs = ctx.rhs.accept(self)

        if isinstance(lhs, LaLaFa) and isinstance(rhs, LaLaFa):
            res = automaton_concat(lhs.value, rhs.value)
            return LaLaFa(res)

        raise ValueError("Incorrect number or type of the arguments")

    def visitKleeneExpr(self, ctx: LaLaLangParser.KleeneExprContext):
        automaton = ctx.expr().accept(self)

        if isinstance(automaton, LaLaFa):
            res = automaton_kleene(automaton.value)
            return LaLaFa(res)

        raise ValueError("Incorrect number or type of the arguments")

    def visitLambdaFunc(self, ctx: LaLaLangParser.LambdaFuncContext):
        self.count_lambdas += 1
        self.lambda_arg = True
        args = ctx.listVars().accept(self)
        self.lambda_arg = False
        self.lambda_body = True
        body = ctx.expr().accept(self)
        self.lambda_body = False

        self.count_lambdas -= 1
        if isinstance(args, LaLaList) and len(args.value):  # and something body
            return LaLaLambda(args.value, body)

        raise ValueError("Incorrect lambda representation. Should be \\[args] -> body")

    def visitSetVars(self, ctx: LaLaLangParser.SetVarsContext):
        primitives = ctx.primitives()

        real_args = []
        for primitive in primitives:
            arg = primitive.accept(self)
            real_args.append(arg)

        if len(real_args):
            my_type = type(real_args[0])

            if not all(isinstance(x, my_type) for x in real_args):
                raise TypeError("Different element types in a a set")

            return LaLaSet({x.value for x in real_args})

        return LaLaSet(set())

    def visitListVars(self, ctx: LaLaLangParser.ListVarsContext):
        atoms = ctx.atom()

        real_args = []
        for atom in atoms:
            arg = atom.accept(self)
            real_args.append(arg)

        return LaLaList([arg.value for arg in real_args])

    def visitIdentifier(self, ctx: LaLaLangParser.IdentifierContext):
        if self.lambda_arg:
            self._local_vars.append({ctx.NAME().symbol.text: ''})
            return LaLaString(ctx.NAME().symbol.text)

        elif self.lambda_body:
            for key in self._local_vars[self.count_lambdas].keys():
                self._local_vars[self.count_lambdas][key] = LaLaString(ctx.NAME().symbol.text)
            return 'id', ctx.NAME().symbol.text

        elif ctx.NAME().symbol.text in self._global_vars.keys():
            return self._global_vars[ctx.NAME().symbol.text]

        raise NameError(f"No variable with name {ctx.NAME()}")

    def visitNumber(self, ctx: LaLaLangParser.NumberContext):
        return LaLaInt(int(ctx.NUMBER().symbol.text))

    def visitString(self, ctx: LaLaLangParser.StringContext):
        return LaLaString(ctx.STRING().symbol.text)

    def visitTrue(self, ctx: LaLaLangParser.TrueContext):
        return LaLaBool(True)

    def visitFalse(self, ctx: LaLaLangParser.FalseContext):
        return LaLaBool(False)
