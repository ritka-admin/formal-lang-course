import tempfile
from pyformlang.cfg import CFG, Variable, Production, Epsilon, Terminal

from project.cf_grammar import (
    cfg_to_weak_normal_from,
    text_grammar_to_weak_normal_form
)


def test_cfg_to_weak_nf():
    with tempfile.NamedTemporaryFile(mode='r+') as file:
        file.write('S -> S A\n')
        file.write('S -> a S\n')
        file.write('A -> epsilon\n')
        # file.write('B -> b')
        file.seek(0)
        grammar = text_grammar_to_weak_normal_form(file.name)
        grammar = cfg_to_weak_normal_from(grammar)

    production1 = Production(head=Variable('S'), body=[Variable('S'), Variable('A')])
    production2 = Production(head=Variable('S'), body=[Variable('a'), Variable('S')])
    production3 = Production(head=Variable('A'), body=[Epsilon()])
    # production4 = Production(head=Variable('B'), body=[Terminal('b')])

    assert grammar.start_symbol.value == 'S'
    assert production1 in grammar.productions
    assert production2 not in grammar.productions
    assert production3 in grammar.productions
    # assert production4 in grammar.productions




