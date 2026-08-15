RED = "R"
BLACK = "B"


class Node:
    def __init__(self, value):
        self.value = value
        self.color = RED
        self.left = None
        self.right = None
        self.parent = None


def color(node):
    if node is None:
        return BLACK

    return node.color


def rotate_left(root, node):
    new_root = node.right
    node.right = new_root.left

    if new_root.left is not None:
        new_root.left.parent = node

    new_root.parent = node.parent

    if node.parent is None:
        root = new_root
    elif node == node.parent.left:
        node.parent.left = new_root
    else:
        node.parent.right = new_root

    new_root.left = node
    node.parent = new_root

    return root


def rotate_right(root, node):
    new_root = node.left
    node.left = new_root.right

    if new_root.right is not None:
        new_root.right.parent = node

    new_root.parent = node.parent

    if node.parent is None:
        root = new_root
    elif node == node.parent.left:
        node.parent.left = new_root
    else:
        node.parent.right = new_root

    new_root.right = node
    node.parent = new_root

    return root


def balance(root, node):
    while node != root and color(node.parent) == RED:

        parent = node.parent
        grandparent = parent.parent

        if parent == grandparent.left:

            # se o lado direito também é vermelho, só troca as cores
            if color(grandparent.right) == RED:
                parent.color = BLACK
                grandparent.right.color = BLACK
                grandparent.color = RED
                node = grandparent

            else:
                if node == parent.right:
                    node = parent
                    root = rotate_left(root, node)

                node.parent.color = BLACK
                node.parent.parent.color = RED
                root = rotate_right(root, node.parent.parent)

        else:

            # mas e o lado esquerdo também é vermelho, só troca as cores
            if color(grandparent.left) == RED:
                parent.color = BLACK
                grandparent.left.color = BLACK
                grandparent.color = RED
                node = grandparent

            else:
                if node == parent.left:
                    node = parent
                    root = rotate_right(root, node)

                node.parent.color = BLACK
                node.parent.parent.color = RED
                root = rotate_left(root, node.parent.parent)

    root.color = BLACK

    return root


def insert(root, value):
    new = Node(value)

    parent = None
    current = root

    while current is not None:
        parent = current

        if value < current.value:
            current = current.left
        else:
            current = current.right

    new.parent = parent

    if parent is None:
        root = new
    elif value < parent.value:
        parent.left = new
    else:
        parent.right = new

    return balance(root, new)


def print_tree(node):
    if node is not None:
        print_tree(node.left)
        print(node.value, node.color)
        print_tree(node.right)


def main():
    root = None

    values = [10, 20, 30, 15, 5]

    for value in values:
        root = insert(root, value)

    print_tree(root)


if __name__ == "__main__":
    main()