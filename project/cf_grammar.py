from pyformlang.cfg import CFG, Terminal


def cfg_to_weak_normal_from(grammar: CFG) -> CFG:
    """
    Turns the grammar into a grammar in a weak Chomsky form

    Parameters:
        grammar: context-free grammar

    Returns:
        context-free grammar in a weak Chomsky form
    """
    initial_grammar_rules = grammar.productions
    initial_grammar_start_symbol = grammar.start_symbol

    without_epsilons = grammar.remove_epsilon().productions
    epsilon_rules = set(initial_grammar_rules) - set(without_epsilons)  # set of epsilon rules

    # add rules with terminals on the right side
    start_terminal_right = set()
    for production in initial_grammar_rules:
        if initial_grammar_start_symbol in production.body and len(production.body) == 2:
            for symb in production.body:
                if not isinstance(symb, Terminal):
                    start_terminal_right.add(production)

    rules = start_terminal_right.union(epsilon_rules)
    normal_form = grammar.to_normal_form()
    return CFG(
        variables=normal_form.variables,
        terminals=normal_form.terminals,
        start_symbol=initial_grammar_start_symbol,
        productions=rules.union(normal_form.productions)
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
