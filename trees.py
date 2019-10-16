"""Tree Data Structures.

Classes
-------
BinaryTree - an immutable representation based on sequence of values.
BinarySearchTree - binary search tree (unique keys and sort order)
"""

from collections import deque
from collections import OrderedDict
from collections import Iterable

from datastructures.nodes import BinaryTreeNode


class BinaryTree:
    """An immutable binary tree based on sequence of values passed in.

    Primary use for representing items in a binary tree structure. Keys are
    mostly under the hood to the user.

    Immutability due to lack of rules governing how nodes should be added
    to tree, which is left to other classes.

    Parameters
    ----------
    items : iterable
        Items to initialize the items of the nodes.

    Examples
    --------
    >>> BinaryTree([1, 2, 3]).items_as_tree()
    [1, 2, 3]
    >>> tree = BinaryTree([1, None, 2, 3])
    >>> tree.items_as_tree()
    [1, None, 2, 3]
    >>> tree.items_as_list()
    [1, 2, 3]
    >>> BinaryTree([5, 4, 7, 3, None, 2, None, -1, None, 9]).items_as_tree()
    [5, 4, 7, 3, None, 2, None, -1, None, 9]
    >>> BinaryTree([5, 1, 4, None, None, 3, 6]).items_as_tree()
    [5, 1, 4, None, None, 3, 6]

    """

    def __init__(self, items):
        if not isinstance(items, Iterable):
            raise ValueError('Must be initialized with Iterable.')

        self._size = 0
        self._root = None

        create_nodes_queue = deque(items)
        assign_children_queue = deque([])
        if create_nodes_queue:
            # Root of tree.
            item = create_nodes_queue.popleft()
            new_node = BinaryTreeNode(item, item, None)
            self._root = new_node
            self._size += 1
            assign_children_queue.append(new_node)

            while create_nodes_queue:
                parent = assign_children_queue.popleft()
                if create_nodes_queue:
                    left_item = create_nodes_queue.popleft()
                    if left_item is not None:
                        left_child = BinaryTreeNode(left_item,
                                                    left_item,
                                                    parent)
                        parent.left_child = left_child
                        self._size += 1
                        assign_children_queue.append(left_child)

                if create_nodes_queue:
                    right_item = create_nodes_queue.popleft()
                    if right_item is not None:
                        right_child = BinaryTreeNode(right_item,
                                                     right_item,
                                                     parent)
                        parent.right_child = right_child
                        self._size += 1
                        assign_children_queue.append(right_child)

    def keys_as_list(self):
        """List of node keys in iter sequence."""
        return [node.key for node in self]

    def items_as_list(self):
        """List of node item in iter sequence."""
        return [node.item for node in self]

    def keys_as_tree(self):
        """List of node keys in iter sequence with None padding to preserve
        internal tree structure.
        """
        return [node.key if node is not None else None
                for node in self._nodes_as_tree()]

    def items_as_tree(self):
        """List of node items in iter sequence with None padding to preserve
        internal tree structure.
        """
        return [node.item if node is not None else None
                for node in self._nodes_as_tree()]

    def _nodes_as_tree(self):
        # Traverse thru the tree until frontier is empty.
        frontier = deque([])
        if len(self) > 0:
            frontier.append(self._root)

        tree_padding_list = []
        while frontier and not all(node is None for node in frontier):
            # Popping off node indicates node visited.
            node = frontier.popleft()
            tree_padding_list.append(node)

            if node is not None:
                frontier.append(node.left_child)
                frontier.append(node.right_child)
        return [node if node is not None else None
                for node in tree_padding_list]

    def __iter__(self):
        self._frontier = deque([])
        if len(self) > 0:
            self._frontier.append(self._root)
        return self

    def __next__(self):
        """Iterate in breadth first sequence."""

        if self._frontier:
            node = self._frontier.popleft()
            if not node.is_leaf():
                if node.left_child is not None:
                    self._frontier.append(node.left_child)
                if node.right_child is not None:
                    self._frontier.append(node.right_child)
            return node
        else:
            raise StopIteration

    def __bool__(self):
        """False if empty."""
        return len(self) > 0

    def __len__(self) -> int:
        """Number of nodes in tree."""
        return self._size

    def __hash__(self):
        """Hash based on tree structure items."""
        return hash(tuple(self.items_as_tree()))

    def __eq__(self, other):
        return isinstance(self, type(other)) and self.__hash__() == other.__hash__()

    def __repr__(self):
        # Can instantiate by copy and paste.
        return '{}({})'.format(self.__class__.__name__, self.items_as_tree())


class BinarySearchTree(BinaryTree):
    """A binary search tree created with unique numerical keys.

    Primarily used for fast search via key comparisons for a large tree. Tree
    representation is typically under the hood to the user.

    Order does matter in determining the structure of the tree.

    Parameters
    ----------
    dict_ : OrderedDict
        Key, item pairs to initialize the BST.

    Examples
    --------
    >>> tree = BinarySearchTree(OrderedDict([(1, 'a'), (2, 'b'), (3, 'c')]))
    >>> tree.keys_as_tree()
    [1, None, 2, None, 3]
    >>> tree.keys_as_list()
    [1, 2, 3]
    >>> tree.items_as_list()
    ['a', 'b', 'c']
    """

    def __init__(self, dict_):
        if not isinstance(dict_, OrderedDict):
            raise ValueError('Must be initialized with OrderedDict.')

        super().__init__([])
        if dict_:
            for key, items in dict_.items():
                self[key] = items

    def _insert(self, key, item):
        # Add a node to the BST if it does not already exist.
        if key in self:
            return

        # Attach new node to appropriate existing node.
        if len(self) > 0:
            parent_node = self._get_insert_loc(self._root, key)
            self._add_edge(parent_node, key, item)
        elif len(self) == 0:
            self._root = BinaryTreeNode(key, item, None)
        else:
            raise AttributeError('Length less than 0.')
        self._size += 1

    def _get_insert_loc(self, current_node, key):
        # Traverse the tree from root and get the appropriate parent to
        # for this node.
        if key < current_node.key:
            if current_node.left_child is not None:
                return self._get_insert_loc(current_node.left_child, key)
        else:
            if current_node.right_child is not None:
                return self._get_insert_loc(current_node.right_child, key)
        return current_node

    def __getitem__(self, key):
        """Get node by key."""
        node = self._get_node(key)
        if node is not None:
            return node.item
        self.__missing__(key)

    def __contains__(self, key):
        """Contains node key."""
        try:
            return self[key] is not None
        except KeyError:
            return False

    def __missing__(self, key):
        raise KeyError('{}'.format(key))

    def __setitem__(self, key, item):
        """Update or create node item by key.  """
        if not isinstance(key, (int, float)):
            raise ValueError('Keys can only be ints or floats.')

        node = self._get_node(key)
        if node is not None:
            node.item = item
        else:
            self._insert(key, item)

    def _get_node(self, key):
        # Search thru tree via binary search
        current_node = self._root
        while current_node is not None:
            if key < current_node.key:
                current_node = current_node.left_child
            elif key > current_node.key:
                current_node = current_node.right_child
            elif key == current_node.key:
                return current_node
            else:
                continue
        return None

    def _add_edge(self, parent_node, key, item):
        # Add links from child to parent and vice versa.
        new_leaf_node = BinaryTreeNode(key, item, parent_node)
        if key > parent_node.key:
            parent_node.right_child = new_leaf_node
        else:
            parent_node.left_child = new_leaf_node

    def __hash__(self):
        """Hash by tree structure keys and items."""
        return hash((tuple(self.keys_as_tree()), tuple(self.items_as_tree())))

    def __eq__(self, other):
        return isinstance(self, type(other)) and self.__hash__() == other.__hash__()

    def __repr__(self):
        # Can instantiate by copy and paste.
        return '{}({})'.format(self.__class__.__name__,
                               OrderedDict(zip(self.keys_as_list(),
                                               self.items_as_list())))