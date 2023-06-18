from antlr4 import *
from project.types import *
from project.graphs import *
from project.reachibility import *
from project.finite_state_automaton import *

from pyformlang.finite_automaton import State
from language.antlr_gen.LaLaLangParserVisitor import LaLaLangParserVisitor
from language.antlr_gen.LaLaLangParser import LaLaLangParser

LOAD = 'load'
ADD_START = 'set_start'
ADD_FINAL = 'set_final'
GET_START = 'get_start'
GET_FINAl = 'get_final'
GET_REACHABLE = 'get_reachable'
GET_VERTICES = 'get_vertices'
GET_EDGES = 'get_edges'
GET_LABELS = 'get_labels'
MAP = 'map'                      # TODO
FILTER = 'filter'                # TODO


class Interpreter(LaLaLangParserVisitor):

    def __init__(self, program: LaLaLangParser.ProgramContext):
        self.program = program
        self._exec_stack = list()
        self._local_vars = dict()
        self._local_vars['true'] = LaLaBool(True)
        self._local_vars['false'] = LaLaBool(False)

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
        self._local_vars[var_name] = value

    def visitAssStmt(self, ctx: LaLaLangParser.AssStmtContext):
        var_name = ctx.assignmentStmt().identifier().NAME().symbol.text
        if var_name not in self._local_vars.keys():
            raise NameError(f"{var_name} was not initialized")
        self._local_vars[var_name] = ctx.assignmentStmt().expr().accept(self)

    def visitFuncExpr(self, ctx: LaLaLangParser.FuncExprContext):
        func_name = ctx.FUNCNAME().getText()
        args = ctx.arg()

        real_args = []
        for arg in args:
            res = arg.accept(self)
            real_args.append(res)

        if func_name == LOAD:
            if len(real_args) == 1 and isinstance(real_args[0], LaLaString):
                graph = load_graph(real_args[0].value, SourceType.FILE)
                automaton = graph_to_nfa(graph, graph.nodes, graph.nodes)
                return LaLaFa(automaton)
            raise ValueError("Incorrect number or type of the arguments")

        elif func_name == ADD_START:
            # TODO: check for the second argument?
            if len(real_args) == 2 and isinstance(real_args[0], LaLaSet):
                automaton = args[1].accept(self)
                if not isinstance(automaton, LaLaFa):
                    raise TypeError("Second argument of 'set_start' should be graph")
                for v in real_args[0].value:
                    automaton.value.add_start_state(State(v))
                return automaton
            raise ValueError("Incorrect number or type of the arguments")

        elif func_name == ADD_FINAL:
            # TODO: check for the second argument?
            if len(real_args) == 2 and isinstance(real_args[0], LaLaSet):
                automaton = args[1].accept(self)
                if not isinstance(automaton, LaLaFa):
                    raise TypeError("Second argument of 'set_start' should be graph")
                for v in real_args[0].value:
                    automaton.value.add_final_state(State(v))
                return automaton
            raise ValueError("Incorrect number or type of the arguments")

        elif func_name == GET_START:
            if len(real_args) == 1 and isinstance(real_args[0], LaLaFa):
                automaton = args[0].accept(self)
                return LaLaSet(automaton.value.start_states)
            raise ValueError("Incorrect number or type of the arguments")

        elif func_name == GET_FINAl:
            if len(real_args) == 1 and isinstance(real_args[0], LaLaFa):
                automaton = args[0].accept(self)
                return LaLaSet(automaton.value.final_states)
            raise ValueError("Incorrect number or type of the arguments")

        elif func_name == GET_VERTICES:
            if len(real_args) == 1 and isinstance(real_args[0], LaLaFa):
                automaton = args[0].accept(self)
                vertices = set()
                for vertex in automaton.value.states:
                    vertices.add(vertex)
                return LaLaSet(vertices)
            raise ValueError("Incorrect number or type of the arguments")

        elif func_name == GET_EDGES:
            if len(real_args) == 1 and isinstance(real_args[0], LaLaFa):
                automaton = args[0].accept(self)
                edges = set()
                for v_from, label, v_to in automaton.value:
                    edges.add((v_from, label, v_to))
                return LaLaSet(edges)
            raise ValueError("Incorrect number or type of the arguments")

        elif func_name == GET_LABELS:
            if len(real_args) == 1 and isinstance(real_args[0], LaLaFa):
                automaton = args[0].accept(self)
                labels = set()
                for _, label, _ in automaton.value:
                    labels.add(label)
                return LaLaSet(labels)
            raise ValueError("Incorrect number or type of the arguments")

        elif func_name == GET_REACHABLE:
            if len(real_args) == 1 and isinstance(real_args[0], LaLaFa):
                automaton = args[0].accept(self)
                v_reachable = find_reachable_for_each_vertex(automaton)
                return LaLaSet(v_reachable)

        raise NotImplementedError(f"No function with name {func_name}")

    def visitInterExpr(self, ctx: LaLaLangParser.InterExprContext):
        pass

    def visitUnionExpr(self, ctx: LaLaLangParser.UnionExprContext):
        pass

    def visitPlusExpr(self, ctx: LaLaLangParser.PlusExprContext):
        pass

    def visitKleeneExpr(self, ctx: LaLaLangParser.KleeneExprContext):
        pass

    def visitLambdaFunc(self, ctx: LaLaLangParser.LambdaFuncContext):
        # TODO
        pass

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
        if ctx.NAME().symbol.text in self._local_vars.keys():
            return self._local_vars[ctx.NAME().symbol.text]

        raise NameError(f"No variable with name {ctx.NAME()}")

    def visitNumber(self, ctx: LaLaLangParser.NumberContext):
        return LaLaInt(int(ctx.NUMBER().symbol.text))

    def visitString(self, ctx: LaLaLangParser.StringContext):
        return LaLaString(ctx.STRING().symbol.text)

    def visitTrue(self, ctx: LaLaLangParser.TrueContext):
        return LaLaBool(True)

    def visitFalse(self, ctx: LaLaLangParser.FalseContext):
        return LaLaBool(False)
