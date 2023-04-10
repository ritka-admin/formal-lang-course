from pyformlang.cfg import Variable, CFG
from pyformlang.regular_expression import Regex


class ECFG:
    """
    The class represents an Extended CFG.
    """

    def __init__(self, start_symbol=None, productions=None):
        self.start_symbol = start_symbol
        self.productions = productions or set()

    @classmethod
    def from_text(cls, text, start_symbol=Variable("S")):
        """
        Read an ECFG from text

        Parameters:
            text:
                Input text
            start_symbol:
                start symbol for the ecfg

        Returns:
            ECFG built via the provided text

        """
        variables = set()
        productions = {}
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue

            production_objects = line.split("->")
            if len(production_objects) != 2:
                raise Exception("More than one production per line")

            head_text, body_text = production_objects
            head = Variable(head_text.strip())

            if head in variables:
                raise Exception("More than one production for the variable")

            variables.add(head)
            body = Regex(body_text.strip())
            productions[head] = body

        return ECFG(
            start_symbol=start_symbol, productions=productions
        )

    @classmethod
    def from_file(cls, path: str):
        """
        Read an ECFG from file

        Parameters
        ----------
        path: str
            Path to the necessary file

        Returns:
            ECFG built via the provided information in a file
        """

        with open(path) as f:
            return ECFG.from_text(f.read())

    @staticmethod
    def from_CFG(cfg: CFG):
        """
        Create ECFG from a given cfg

        Parameters:
            cfg: context-free grammar to create ecfg from

        Returns:
            ECFG built for the provided cfg
        """
        prods = {}
        for prod in cfg.productions:
            regex = Regex(
                ".".join(variable.value for variable in prod.body)
                if len(prod.body) > 0
                else ""
            )
            prods[prod.head] = (
                regex
                if prod.head not in prods
                else prods[prod.head].union(regex)
            )

        return ECFG(cfg.start_symbol, prods)
