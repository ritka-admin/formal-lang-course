import pytest
from tempfile import NamedTemporaryFile
from pyformlang.cfg import CFG, Variable
from project.ecfg import ECFG
from pyformlang.regular_expression import Regex


def test_ecfg_from_cfg():
    cfg = CFG.from_text(
        """
        S->A B
        B->a b*
        """
    )

    ecfg = ECFG.from_CFG(cfg)

    assert ecfg.start_symbol == Variable("S")
    assert ecfg.productions[ecfg.start_symbol].to_epsilon_nfa() == Regex("A B").to_epsilon_nfa()
    assert ecfg.productions[Variable("B")].to_epsilon_nfa() == Regex("a b*").to_epsilon_nfa()


def test_ecfg_from_file():
    with NamedTemporaryFile("r+") as file:
        file.write("S -> B S\n")
        file.write("B -> b\n")
        file.write("E -> A F\n")
        file.write("A -> a\n")
        file.write("F -> f\n")
        file.seek(0)
        ecfg = ECFG.from_file(file.name)

    assert ecfg.start_symbol == Variable("S")
    assert ecfg.productions[Variable("S")].to_epsilon_nfa() == Regex("B S").to_epsilon_nfa()
    assert ecfg.productions[Variable("B")].to_epsilon_nfa() == Regex("b").to_epsilon_nfa()
    assert ecfg.productions[Variable("E")].to_epsilon_nfa() == Regex("A F").to_epsilon_nfa()
    assert ecfg.productions[Variable("A")].to_epsilon_nfa() == Regex("a").to_epsilon_nfa()
    assert ecfg.productions[Variable("F")].to_epsilon_nfa() == Regex("f").to_epsilon_nfa()


