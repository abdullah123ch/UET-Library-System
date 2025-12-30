class ISBNNode:
    def __init__(self, isbn):
        self.isbn = isbn
        self.next = None

class AuthorEntry:
    def __init__(self, authorName, isbn):
        self.authorName = authorName
        self.isbn_list_head = ISBNNode(isbn)
        self.next = None

class AuthorHT:
    def __init__(self, size=50):
        self.size = size
        self.table = [None] * self.size

    def _hash(self, name):
        return hash(name.strip().lower()) % self.size

    def insert(self, author, isbn):
        index = self._hash(author)
        author_norm = author.strip().lower()
        
        if not self.table[index]:
            self.table[index] = AuthorEntry(author_norm, isbn)
        else:
            current = self.table[index]
            while current:
                if current.authorName == author_norm:
                    new_node = ISBNNode(isbn)
                    new_node.next = current.isbn_list_head
                    current.isbn_list_head = new_node
                    return
                if not current.next: break
                current = current.next
            current.next = AuthorEntry(author_norm, isbn)

    def search(self, author):
        index = self._hash(author)
        current = self.table[index]
        author_norm = author.strip().lower()
        
        while current:
            if current.authorName == author_norm:
                isbns = []
                temp = current.isbn_list_head
                while temp:
                    isbns.append(temp.isbn)
                    temp = temp.next
                return isbns
            current = current.next
        return []