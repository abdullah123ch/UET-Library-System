class ISBNNode:
    """
    Linked list node to store an ISBN.
    """
    def __init__(self, isbn):
        self.isbn = isbn
        self.next = None

class AuthorEntry:
    """
    Represents an author entry in the hash table.
    Contains a pointer to a linked list of ISBNs associated with this author.
    """
    def __init__(self, authorName, isbn):
        self.authorName = authorName
        self.isbn_list_head = ISBNNode(isbn)
        self.next = None

class AuthorHT:
    """
    Specialized Hash Table to map Authors to multiple ISBNs.
    
    This helps in retrieving all books written by a specific author efficiently.
    It uses chaining for collisions and a secondary linked list for ISBNs under the same author.
    """
    def __init__(self, size=50):
        self.size = size
        self.table = [None] * self.size

    def _hash(self, name):
        return hash(name.strip().lower()) % self.size

    def insert(self, author, isbn):
        """
        Inserts an Author-ISBN mapping.
        
        If the author exists, appends the ISBN to their list.
        If not, creates a new AuthorEntry.
        """
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
        """
        Retrieves all ISBNs associated with an author.
        
        Args:
            author (str): Name of the author.
            
        Returns:
            list[str]: A list of ISBNs.
        """
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