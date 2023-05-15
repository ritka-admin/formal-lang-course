from antlr4 import *
from pydot import *
from language.antlr_gen.LaLaLangParserVisitor import LaLaLangParserVisitor

from language.antlr_gen.LaLaLangParser import LaLaLangParser
from language.antlr_gen.LaLaLangLexer import LaLaLangLexer


def get_script_from_source(source: str = None, file: bool = None):
    if file:
        stream = FileStream(source)
    elif not file and source:
        stream = InputStream(source)
    # if source is None
    else:
        stream = StdinStream()
    return stream


def get_tree_root(stream: InputStream):
    lexer = LaLaLangLexer(stream)
    stream = CommonTokenStream(lexer)
    parser = LaLaLangParser(stream)
    tree = parser.program()
    return tree


def check_syntax(source: str, file: bool = None):
    stream = get_script_from_source(source, file)
    tree = get_tree_root(stream)
    res = tree.getText()
    return res


def write_to_dot_file(source: str, file: bool, path):
    visitor = DotTreeVisitor()
    stream = get_script_from_source(source, file)
    tree = get_tree_root(stream)
    tree.accept(visitor)
    visitor.graph.write(path)


class DotTreeVisitor(LaLaLangParserVisitor):
    def __init__(self):
        self.graph = Dot("LaLaLang graph")
        self.n_nodes = 0

    def visitProgram(self, ctx: LaLaLangParser.ProgramContext):
        n_number = str(self.n_nodes + 1)
        node = Node('prog ' + n_number)
        self.graph.add_node(node)

        for i, stmt in enumerate(ctx.stmts):
            child_node = stmt.accept(self)
            edge = Edge(node, child_node, label='stmt ' + str(i))
            self.graph.add_edge(edge)

        return node

    def visitPriStmt(self, ctx:LaLaLangParser.PriStmtContext):
        n_number = str(self.n_nodes + 1)
        node = Node(n_number, label='printStmt')
        self.graph.add_node(node)

        child_node = ctx.printStmt().expr().accept(self)
        edge = Edge(node, child_node, label='exprInPrint')
        self.graph.add_edge(edge)

        return node

    def visitIniStmt(self, ctx:LaLaLangParser.IniStmtContext):
        n_number = str(self.n_nodes + 1)
        node = Node(n_number, label='iniStmt')
        self.graph.add_node(node)

        child_node = ctx.initializerStmt().identifier().accept(self)
        self.graph.add_node(child_node)

        edge = Edge(node, child_node, label='varName')
        self.graph.add_edge(edge)

        child_node = ctx.initializerStmt().expr().accept(self)
        edge = Edge(node, child_node)
        self.graph.add_edge(edge)

        return node

    def visitAssStmt(self, ctx:LaLaLangParser.AssStmtContext):
        n_number = str(self.n_nodes + 1)
        node = Node(n_number, label='assignStmt')
        self.graph.add_node(node)

        child_node = ctx.assignmentStmt().identifier().accept(self)
        self.graph.add_node(child_node)

        edge = Edge(node, child_node, label='varName')
        self.graph.add_edge(edge)

        child_node = ctx.assignmentStmt().expr().accept(self)
        edge = Edge(node, child_node, label='value')
        self.graph.add_edge(edge)

        return node

    def visitExpr(self, ctx: LaLaLangParser.ExprContext):
        n_number = str(self.n_nodes + 1)
        node = Node(n_number, label='expr')
        self.graph.add_node(node)

        return node

    def visitIdentifier(self, ctx: LaLaLangParser.IdentifierContext):
        n_number = str(self.n_nodes + 1)
        name = ctx.NAME().symbol.text
        node = Node(name, label=f'id{n_number}')
        self.graph.add_node(node)
        return node
