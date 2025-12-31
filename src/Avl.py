class AVLNode:
    def __init__(self, isbn, book):
        self.isbn = str(isbn)
        self.book = book
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def height(self, node):
        return node.height if node else 0

    def balance(self, node):
        return self.height(node.left) - self.height(node.right) if node else 0

    def rotateRight(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self.height(y.left), self.height(y.right))
        x.height = 1 + max(self.height(x.left), self.height(x.right))
        return x

    def rotateLeft(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(self.height(x.left), self.height(x.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))
        return y

    def minValue(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def insert(self, root, isbn, book):
        if not root:
            return AVLNode(isbn, book)

        if isbn < root.isbn:
            root.left = self.insert(root.left, isbn, book)
        elif isbn > root.isbn:
            root.right = self.insert(root.right, isbn, book)
        else:
            return root

        root.height = 1 + max(self.height(root.left), self.height(root.right))
        return self.rebalance(root, isbn)

    def delete(self, root, isbn):
        if not root:
            return root

        if isbn < root.isbn:
            root.left = self.delete(root.left, isbn)
        elif isbn > root.isbn:
            root.right = self.delete(root.right, isbn)
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp

            temp = self.minValue(root.right)
            root.isbn = temp.isbn
            root.book = temp.book
            root.right = self.delete(root.right, temp.isbn)

        if root is None:
            return root

        root.height = 1 + max(self.height(root.left), self.height(root.right))
        balance = self.balance(root)

        # Left Left Case
        if balance > 1 and self.balance(root.left) >= 0:
            return self.rotateRight(root)
        # Left Right Case
        if balance > 1 and self.balance(root.left) < 0:
            root.left = self.rotateLeft(root.left)
            return self.rotateRight(root)
        # Right Right Case
        if balance < -1 and self.balance(root.right) <= 0:
            return self.rotateLeft(root)
        # Right Left Case
        if balance < -1 and self.balance(root.right) > 0:
            root.right = self.rotateRight(root.right)
            return self.rotateLeft(root)

        return root

    def rebalance(self, root, isbn):
        balance = self.balance(root)
        if balance > 1 and isbn < root.left.isbn:
            return self.rotateRight(root)
        if balance < -1 and isbn > root.right.isbn:
            return self.rotateLeft(root)
        if balance > 1 and isbn > root.left.isbn:
            root.left = self.rotateLeft(root.left)
            return self.rotateRight(root)
        if balance < -1 and isbn < root.right.isbn:
            root.right = self.rotateRight(root.right)
            return self.rotateLeft(root)
        return root

    def search(self, root, isbn):
        if not root or root.isbn == isbn:
            return root
        if isbn < root.isbn:
            return self.search(root.left, isbn)
        return self.search(root.right, isbn)

    def inorder(self, root, result_list):
        if root:
            self.inorder(root.left, result_list)
            result_list.append(root.book)
            self.inorder(root.right, result_list)


def display_aux(node):
    """Returns list of strings, width, height, and horizontal coordinate of the root."""
    # No child.
    if node.right is None and node.left is None:
        line = f'< {node.isbn} , {node.book.title} >'
        width = len(line)
        height = 1
        middle = width // 2
        return [line], width, height, middle

    # Only left child.
    if node.right is None:
        lines, n, p, x = display_aux(node.left)
        s = f'< {node.isbn} , {node.book.title} >'
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
        second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
        shifted_lines = [line + u * ' ' for line in lines]
        return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

    # Only right child.
    if node.left is None:
        lines, n, p, x = display_aux(node.right)
        s = f'< {node.isbn} , {node.book.title} >'
        u = len(s)
        first_line = s + x * '_' + (n - x) * ' '
        second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
        shifted_lines = [u * ' ' + line for line in lines]
        return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

    # Two children.
    left, n, p, x = display_aux(node.left)
    right, m, q, y = display_aux(node.right)
    s = f'< {node.isbn} , {node.book.title} >'
    u = len(s)
    first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
    second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
    if p < q:
        left += [n * ' '] * (q - p)
    elif q < p:
        right += [m * ' '] * (p - q)
    zipped_lines = zip(left, right)
    lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
    return lines, n + m + u, max(p, q) + 2, n + u // 2

def display(node):
    if node is None:
        print("Tree is empty.")
        return
    lines, *_ = display_aux(node)
    for line in lines:
        print(line)
    print()