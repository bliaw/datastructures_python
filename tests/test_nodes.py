"""Test nodes module. Demonstration for usage of pytest and hypothesis
libraries.

Fixtures
-------
set_up - example of using pytest fixtures.

"""

from hypothesis import given
import hypothesis.strategies as st
import pytest

from datastructures.nodes import BinaryTreeNode


@pytest.fixture
def set_up_fixture():
    """Example using fixture for setup and teardown."""
    print('i am in setup')
    root_node = BinaryTreeNode(1, 1, None)
    left_child_node = BinaryTreeNode(2, 1, root_node)
    root_node.left_child = left_child_node
    right_child_node = BinaryTreeNode(3, 1, root_node)
    root_node.right_child = right_child_node

    yield root_node

    print('i am now in teardown')


def test_init(set_up_fixture):
    """Test init 3 nodes."""
    root_node = set_up_fixture
    assert root_node.key == 1
    assert root_node.left_child.key == 2
    assert root_node.right_child.key == 3
    assert root_node.left_child.left_child is None


def test_add_node(set_up_fixture):
    """Test add node."""
    root_node = set_up_fixture
    root_node.left_child.left_child = BinaryTreeNode(4, 4, root_node.left_child)
    assert root_node.left_child.left_child.key == 4


@given(st.integers(), st.integers())
def test_ints_are_commutative(x, y):
    """Example showing how to use hypothesis."""
    assert x + y == y + x
