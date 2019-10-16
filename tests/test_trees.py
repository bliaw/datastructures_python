"""Test for trees module.

Classes
-------
TestBinarySearchTree - Test binary search tree class.


Fixtures
--------
pytest_generate_tests - read in data for fixtures w/dynamic parameters.
init_instance - factory for binary search tree.
"""
from collections import OrderedDict
import random

from hypothesis import given
import hypothesis.strategies as st
import pytest

from datastructures.trees import BinarySearchTree
from datastructures.trees import BinaryTree


def pytest_generate_tests(metafunc):
    """Read in test data to create fixtures with dynamic parameters."""
    from datastructures.tests._test_trees_data import \
        ids, \
        inputs, \
        expected_list, \
        expected_items_list, \
        expected_tree, \
        expected_items_tree, \
        expected_len, \
        expected_valid_BST, \
        shuffled_inputs, \
        is_equal

    if 'get_test_as_list_data' in metafunc.fixturenames:
        metafunc.parametrize('get_test_as_list_data',
                             list(zip(inputs, expected_list)),
                             ids=ids)

    if 'get_test_items_as_list_data' in metafunc.fixturenames:
        metafunc.parametrize('get_test_items_as_list_data',
                             list(zip(inputs, expected_items_list)),
                             ids=ids)

    if 'get_test_as_tree_data' in metafunc.fixturenames:
        metafunc.parametrize('get_test_as_tree_data',
                             list(zip(inputs, expected_tree)),
                             ids=ids)

    if 'get_test_items_as_tree_data' in metafunc.fixturenames:
        metafunc.parametrize('get_test_items_as_tree_data',
                             list(zip(inputs, expected_items_tree)),
                             ids=ids)

    if 'get_test_len_data' in metafunc.fixturenames:
        metafunc.parametrize('get_test_len_data',
                             list(zip(inputs, expected_len)),
                             ids=ids)

    if 'get_test_valid_BST_glassbox' in metafunc.fixturenames:
        metafunc.parametrize('get_test_valid_BST_glassbox',
                             list(zip(inputs, expected_valid_BST)),
                             ids=ids)

    if 'get_test_eq' in metafunc.fixturenames:
        metafunc.parametrize('get_test_eq',
                             list(zip(inputs, shuffled_inputs, is_equal)),
                             ids=ids)


@pytest.fixture
def init_instance():
    """BST Factory based on list of keys.

    Returns
    -------
    f
        Factory method to create BST instance.
    """
    def _init_instance(dicts_):
        return BinarySearchTree(dicts_)
    return _init_instance


class TestBinarySearchTree:
    """Test for BinarySearchTree Class."""

    def test_as_list(self, init_instance, get_test_as_list_data):
        inputs, expected = get_test_as_list_data
        assert init_instance(inputs).keys_as_list() == expected

    def test_items_as_list(self, init_instance, get_test_items_as_list_data):
        inputs, expected = get_test_items_as_list_data
        assert init_instance(inputs).items_as_list() == expected

    def test_as_tree(self, init_instance, get_test_as_tree_data):
        inputs, expected = get_test_as_tree_data
        assert init_instance(inputs).keys_as_tree() == expected

    def test_items_as_tree(self, init_instance, get_test_items_as_tree_data):
        inputs, expected = get_test_items_as_tree_data
        assert init_instance(inputs).items_as_tree() == expected

    def test_len(self, init_instance, get_test_len_data):
        inputs, expected = get_test_len_data
        assert len(init_instance(inputs)) == expected

    @given(gen_input=st.dictionaries(st.integers(), st.integers()))
    def test_len_randomgen(self, init_instance, gen_input):
        assert len(init_instance(OrderedDict(gen_input))) == len(set(gen_input))

    def test_valid_BST_glassbox(self, init_instance, get_test_valid_BST_glassbox):
        inputs, expected = get_test_valid_BST_glassbox
        assert self._is_valid_BST(init_instance(inputs)) is expected

    def test_negative_BST_2_level(self):
        tree = BinaryTree([5, 1, 4, None, None, 3, 6])
        assert self._is_valid_BST(tree) is False

    @given(gen_input=st.dictionaries(st.integers(), st.integers(), min_size=1),
           gen_key=st.integers(),
           gen_items=st.characters())
    def test_set_random_key(self, init_instance, gen_input, gen_key, gen_items):
        tree = init_instance(OrderedDict(gen_input))
        tree[gen_key] = gen_items
        assert tree[gen_key] == gen_items

    @given(gen_input=st.dictionaries(st.integers(), st.integers(), min_size=1))
    def test_getitem_from_sampled_key(self, init_instance, gen_input):
        tree = init_instance(OrderedDict(gen_input))
        sampled_key = random.choice(list(gen_input.keys()))
        assert tree[sampled_key] == gen_input[sampled_key]

    @given(gen_input=st.dictionaries(st.integers(), st.integers(), min_size=1),
           gen_items=st.text())
    def test_setitem_from_sampled_key(self, init_instance, gen_input, gen_items):
        tree = init_instance(OrderedDict(gen_input))
        sampled_key = random.choice(list(gen_input.keys()))
        tree[sampled_key] = gen_items
        assert tree[sampled_key] == gen_items

    @given(gen_input=st.dictionaries(st.integers(), st.integers(), min_size=1))
    def test_contains_sampled_key(self, init_instance, gen_input):
        tree = init_instance(OrderedDict(gen_input))
        sampled_key = random.choice(list(gen_input.keys()))
        assert bool(sampled_key in tree) is True

    @given(gen_input=st.dictionaries(st.integers(), st.integers(), min_size=1))
    def test_set_twice_same_sampled_key(self, init_instance, gen_input):
        tree = init_instance(OrderedDict(gen_input))
        length = len(tree)
        sampled_key = random.choice(list(gen_input.keys()))
        tree[sampled_key] = sampled_key
        assert len(tree) == length

    @given(gen_input=st.dictionaries(st.floats(allow_infinity=False, allow_nan=False),
                                     st.floats(allow_infinity=False, allow_nan=False),
                                     min_size=1))
    def test_init_random_float_keys(self, init_instance, gen_input):
        tree = init_instance(OrderedDict(gen_input))
        assert tree[random.choice(list(gen_input.keys()))] is not None

    @given(gen_input=st.dictionaries(st.characters(), st.characters(), min_size=1))
    def test_insert_non_numeric_keys_exception(self, init_instance, gen_input):
        with pytest.raises(ValueError):
            init_instance(OrderedDict(gen_input))

    @given(gen_input=st.dictionaries(st.integers(), st.characters(), min_size=1))
    def test_repr(self, init_instance, gen_input):
        assert repr(init_instance(OrderedDict(gen_input))) == \
               repr(eval(repr(init_instance(OrderedDict(gen_input)))))

    def test_eq_2_bst(self, init_instance, get_test_eq):
        inputs, shuffled_inputs, is_equal = get_test_eq
        assert bool(init_instance(inputs) == init_instance(shuffled_inputs)) is is_equal

    # def test_negative_cases(self):
    #     pass
    #
    # def test_del_node(self):
    #     pass


    def _is_valid_BST(self, bst):
        # Check each node's children based on node's parent values.
        if bst:
            for node in (node for node in bst if node.parent is not None):
                if not self._are_children_valid_given_parent(node):
                    return False
            return True
        return False

    def _are_children_valid_given_parent(self, node):
        # Parent -> node -> child relationship dictates min / max range
        if (node.left_child is not None) and (node.parent.left_child == node):
            if node.left_child.key > node.key:
                return False
        if (node.left_child is not None) and (node.parent.right_child == node):
            if (node.left_child.key < node.parent.key) or (node.left_child.key > node.key):
                return False
        if (node.right_child is not None) and (node.parent.left_child == node):
            if (node.right_child.key > node.parent.key) or (node.right_child.key < node.key):
                return False
        if (node.right_child is not None) and (node.parent.right_child == node):
            if node.right_child.key < node.key:
                return False
        return True
