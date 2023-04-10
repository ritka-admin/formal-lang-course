from pyformlang.cfg import CFG, Terminal


def cfg_to_weak_normal_from(grammar: CFG) -> CFG:
    """
    Turns the grammar into a grammar in a weak Chomsky form

    Parameters:
        grammar: context-free grammar

    Returns:
        context-free grammar in a weak Chomsky form
    """
    grammar_m = grammar.eliminate_unit_productions().remove_useless_symbols()
    dec = grammar_m._get_productions_with_only_single_terminals()
    new_prod = grammar_m._decompose_productions(dec)

    return CFG(
        variables=grammar_m.variables,
        terminals=grammar_m.terminals,
        start_symbol=grammar_m.start_symbol,
        productions=new_prod
    )


def text_grammar_to_weak_normal_form(file: str) -> CFG:
    """
    Creates context-free grammar with the rules from a file.

    Parameters:
        file: name of a file to read from

    Return:
        Context-free grammar with the rules from a file
    """
    with open(file) as f:
        return CFG.from_text(f.read())
