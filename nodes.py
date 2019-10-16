"""Module containing node data structures.

Classes
-------
BinaryTreeNode - node with key, value and parent with <=2 children.

"""


class BinaryTreeNode:
    """A binary tree node with 0 -> 2 children.

    Parameters
    ----------
    key : Any
        Key of the node.
    item : Any
        Value of the node.
    parent : BinaryTreeNode or None
        Parent to this node.
    right_child : BinaryTreeNode (optional)
        Right child of  node.
    left_child : BinaryTreeNode (optional)
        Left child of node.

    Raises
    ------
    Exception
        abc

    Examples
    --------
    >>> parent_node = BinaryTreeNode(1, 'a', None)
    >>> left_child_node = BinaryTreeNode(2, 'b', parent_node)
    >>> parent_node.left_child = left_child_node
    >>> right_child_node = BinaryTreeNode(3, 'c', parent_node)
    >>> parent_node.right_child = right_child_node
    >>> parent_node.key
    1
    >>> parent_node.item
    'a'
    >>> parent_node.left_child.key
    2
    >>> parent_node.right_child.key
    3
    >>> left_child_node.left_child is None
    True
    >>> left_child_node.left_child = BinaryTreeNode(4, 'd', left_child_node)
    >>> parent_node.left_child.left_child.key
    4

    """

    def __init__(self, key, item, parent, right_child=None, left_child=None):
        self._parent = parent
        self._key = key
        self._item = item
        self._left_child = left_child
        self._right_child = right_child

    @property
    def key(self):
        """Key of the node."""
        return self._key

    @property
    def item(self):
        """Item of the node."""
        return self._item

    @item.setter
    def item(self, new_item):
        self._item = new_item

    @property
    def right_child(self):
        """Right child node."""
        return self._right_child

    @right_child.setter
    def right_child(self, node):
        self._right_child = node

    @property
    def left_child(self):
        """Left child node."""
        return self._left_child

    @left_child.setter
    def left_child(self, node):
        self._left_child = node

    @property
    def parent(self):
        """Parent of the node."""
        return self._parent

    def is_leaf(self):
        """Is node a leaf."""
        return self.right_child is None and self.left_child is None

    def is_root(self):
        """Is node a root."""
        return self.parent is None
