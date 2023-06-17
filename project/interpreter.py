from antlr4 import *
from project.types import *
from project.graphs import *
from project.finite_state_automaton import *

from pyformlang.finite_automaton import State
from language.antlr_gen.LaLaLangParserVisitor import LaLaLangParserVisitor
from language.antlr_gen.LaLaLangParser import LaLaLangParser

LOAD = 'load'
ADD_START = 'set_start'
ADD_FINAL = 'set_final'


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
        # TODO: calculate result before printing out
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
                return automaton
            raise TypeError('Illegal argument type for the path')

        elif func_name == ADD_START:
            # TODO: check for the second argument?
            if len(real_args) == 2 and isinstance(real_args[0], LaLaSet):
                automaton = args[1].accept(self)
                if not isinstance(automaton, EpsilonNFA):
                    raise TypeError("Second argument of 'set_start' should be graph")
                for v in real_args[0].value:
                    automaton.add_start_state(State(v))
                return automaton
            raise ValueError("Incorrect number or type of the arguments")

        elif func_name == ADD_FINAL:
            # TODO: check for the second argument?
            if len(real_args) == 2 and isinstance(real_args[0], LaLaSet):
                automaton = args[1].accept(self)
                if not isinstance(automaton, EpsilonNFA):
                    raise TypeError("Second argument of 'set_start' should be graph")
                for v in real_args[0].value:
                    automaton.add_final_state(State(v))
                return automaton

        raise NotImplementedError(f"No function with name {func_name}")

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
