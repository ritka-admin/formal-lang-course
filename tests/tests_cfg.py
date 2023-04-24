import tempfile
from pyformlang.cfg import CFG, Variable, Production, Epsilon, Terminal

from project.cf_grammar import (
    cfg_to_weak_normal_from,
    text_grammar_to_weak_normal_form
)


def test_cfg_to_weak_nf():
    with tempfile.NamedTemporaryFile(mode='r+') as file:
        file.write('S -> A B C\n')
        file.write('A -> a \n')
        file.write('B -> b \n')
        file.write('C -> c')
        file.seek(0)
        grammar = text_grammar_to_weak_normal_form(file.name)
        grammar = cfg_to_weak_normal_from(grammar)

    res = CFG.from_text(
        """
        B -> b
        A -> a
        C -> c
        S -> A C#CNF#1
        C#CNF#1 -> B C"""
    )

    assert grammar.start_symbol.value == 'S'
    assert set(grammar.productions) == set(res.productions)



