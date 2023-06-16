from antlr4 import *
from project.types import *

from language.antlr_gen.LaLaLangParserVisitor import LaLaLangParserVisitor
from language.antlr_gen.LaLaLangParser import LaLaLangParser
from language.antlr_gen.LaLaLangLexer import LaLaLangLexer


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
        pass

    def visitLambdaFunc(self, ctx: LaLaLangParser.LambdaFuncContext):
        pass

    # TODO: identifier only for the access, cannot visit it in iniStmt?
    def visitIdentifier(self, ctx: LaLaLangParser.IdentifierContext):
        if ctx.NAME().symbol.text in self._local_vars.keys():
            return self._local_vars[ctx.NAME().symbol.text]

        raise NameError(f"No variable with name {ctx.NAME()}")

    # def visitCollections

    def visitNumber(self, ctx: LaLaLangParser.NumberContext):
        return LaLaInt(int(ctx.NUMBER().symbol.text))

    def visitString(self, ctx: LaLaLangParser.StringContext):
        return LaLaString(ctx.STRING().symbol.text)

    def visitTrue(self, ctx: LaLaLangParser.TrueContext):
        return LaLaBool(True)

    def visitFalse(self, ctx: LaLaLangParser.FalseContext):
        return LaLaBool(False)
