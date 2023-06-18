import os
import pytest
from project.dot_visitor import check_syntax, write_to_dot_file


@pytest.mark.parametrize('string', ['var x = 5;',
                                    'var y = set_start(get_final(graph), graph);',
                                    'var z = [[a, b, c], d, e];',
                                    'var xx = \\[x] -> x;'
                                    'x = {4, 5, 6};'])
def test_check_syntax_valid(string):
    res = check_syntax(string, False)
    assert string.replace(" ", "") == res.split('<EOF>')[0]


@pytest.mark.parametrize('string', ['var x = 5',
                                    'var xx = \\ x -> x',
                                    'var y = set_start(get_final(graph), graph)'])
def test_check_invalid_syntax(string):
    res = check_syntax(string, False)
    assert not string.replace(" ", "") == res.split('<EOF>')[0]


@pytest.mark.parametrize('string, res', [('var x = 5;', 'example1'),
                                          ('x = 5;', 'example2')])
                                          # ('print(set_final({1, 2, 3}, a));', 'example3')])
def test_dot(string, res):
    write_to_dot_file(string, False, 'kek')
    with open('kek') as f:
        graph_dot = f.readlines()
        real_dot = open(res)
        lines = real_dot.readlines()
        assert graph_dot == lines
        real_dot.close()
    os.remove('kek')


