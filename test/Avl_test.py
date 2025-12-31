import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.Avl import AVLTree, display
from src.Models import Book

def test_avl():
    tree = AVLTree()
    root = None
    
    books = [
        Book("9780134685991", "Effective Python", "Brett Slatkin", 2019, "Prog", 3),
        Book("9780132350884", "Clean Code", "Robert Martin", 2008, "Prog", 5),
        Book("9780596009205", "Head First Design Patterns", "Eric Freeman", 2004, "Design", 2),
        Book("9780201633610", "Design Patterns", "Erich Gamma", 1994, "CS", 4)
    ]

    print("--- Testing Insertions ---")
    for b in books:
        root = tree.insert(root, b.isbn, b)
    
    display(root)

    print("\n--- Testing Search ---")
    search_isbn = "9780132350884"
    result = tree.search(root, search_isbn)
    if result:
        print(f"Found: {result.book.title} by {result.book.author}")
    else:
        print("Book not found.")

    print("\n--- Testing Inorder Traversal (Sorted ISBNs) ---")
    sorted_books = []
    tree.inorder(root, sorted_books)
    for b in sorted_books:
        print(f"{b.isbn}: {b.title}")

    print("\n--- Testing Deletion ---")
    root = tree.delete(root, "9780134685991")
    print("Tree after deleting 9780134685991:")
    display(root)

if __name__ == "__main__":
    test_avl()