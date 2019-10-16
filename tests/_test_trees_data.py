"""Test data for test_trees."""

from collections import OrderedDict

ids = ['Init Empty',
       'Init 1 node',
       'Init 3 level full nodes',
       'Init 3 level empty left nodes',
       'Init 3 level middle nodes',
       'Init 3 vertical nodes',
       'Init 5 level left heavy nodes'
       ]
inputs = [OrderedDict([]),
          OrderedDict([(2, 'b'), (1, 'a')]),
          OrderedDict([(5, 'e'), (2, 'b'), (7, 'g'), (1, 'a'), (3, 'c'), (6, 'f'), (8, 'h')]),
          OrderedDict([(5, 'e'), (2, 'b'), (7, 'g'), (3, 'c'), (6, 'f'), (9, 'i')]),
          OrderedDict([(5, 'e'), (7, 'g'), (-1, 'z'), (6, 'f')]),
          OrderedDict([(-1, 'z'), (0, ' '), (1, 'a')]),
          OrderedDict([(5, 'e'), (4, 'd'), (7, 'g'), (3, 'c'), (2, 'b'), (-1, 'z'), (9, 'i')])]

shuffled_inputs = [OrderedDict([]),
                   OrderedDict([(2, 'b'), (1, 'a')]),
                   OrderedDict([(5, 'e'), (7, 'g'), (2, 'b'), (3, 'c'), (1, 'a'), (8, 'h'), (6, 'f')]),
                   OrderedDict([(5, 'e'), (2, 'b'), (7, 'g'), (9, 'i'), (3, 'c'), (6, 'f')]),
                   OrderedDict([(5, 'e'), (6, 'f'), (7, 'g'), (-1, 'z')]),
                   OrderedDict([(-1, 'z'), (0, ' '), (1, 'a'), ]),
                   OrderedDict([(5, 'e'), (4, 'd'), (7, 'g'), (3, 'c'), (2, 'b'), (-1, 'z'), (9, 'i')])]

is_equal = [True, True, True, True, False, True, True]

expected_list = [[],
                 [2, 1],
                 [5, 2, 7, 1, 3, 6, 8],
                 [5, 2, 7, 3, 6, 9],
                 [5, -1, 7, 6],
                 [-1, 0, 1],
                 [5, 4, 7, 3, 9, 2, -1]]

expected_items_list = [[],
                       ['b', 'a'],
                       ['e', 'b', 'g', 'a', 'c', 'f', 'h'],
                       ['e', 'b', 'g', 'c', 'f', 'i'],
                       ['e', 'z', 'g', 'f'],
                       ['z', ' ', 'a'],
                       ['e', 'd', 'g', 'c', 'i', 'b', 'z']]

expected_tree = [[],
                 [2, 1],
                 [5, 2, 7, 1, 3, 6, 8],
                 [5, 2, 7, None, 3, 6, 9],
                 [5, -1, 7, None, None, 6],
                 [-1, None, 0, None, 1],
                 [5, 4, 7, 3, None, None, 9, 2, None, None, None, -1]]

expected_items_tree = [[],
                       ['b', 'a'],
                       ['e', 'b', 'g', 'a', 'c', 'f', 'h'],
                       ['e', 'b', 'g', None, 'c', 'f', 'i'],
                       ['e', 'z', 'g', None, None, 'f'],
                       ['z', None, ' ', None, 'a'],
                       ['e', 'd', 'g', 'c', None, None, 'i', 'b', None, None, None, 'z']]

expected_len = [0, 2, 7, 6, 4, 3, 7]

expected_valid_BST = [False, True, True, True, True, True, True]
