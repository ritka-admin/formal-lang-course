from project.ecfg import ECFG
from project.rsm import RSM
from pyformlang.cfg import CFG, Variable
from pyformlang.regular_expression import Regex


def test_ecfg_to_rsm():
    cfg = CFG.from_text(
        """
        S -> A S B
        A -> a
        B -> b
        C -> c
        C -> b
        """
    )

    ecfg = ECFG.from_CFG(cfg)
    rsm = RSM.ecfg_to_rsm(ecfg)
    assert rsm.boxes[Variable("B")] == Regex("b").to_epsilon_nfa()
    assert rsm.boxes[Variable("A")] == Regex("a").to_epsilon_nfa()
    assert rsm.boxes[Variable("S")] == Regex("A (S B)").to_epsilon_nfa()
    assert rsm.boxes[Variable("C")] == Regex("c|b").to_epsilon_nfa()

