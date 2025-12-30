import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.Avl import AVLTree
from src.HashTable import HashTable
from src.AuthorHT import AuthorHT
from src.Models import Book, Member

def run_tests():
    # 1. Setup
    catalog = AVLTree()
    title_idx = HashTable()
    author_idx = AuthorHT()
    member_db = HashTable()
    root = None

    # 2. Test Data
    b1 = Book("9780134685991", "Effective Python", "Brett Slatkin", 2019, "Coding", 3)
    m1 = Member("2024-EE-001", "Ali Ahmed")

    # 3. Insertion Logic
    root = catalog.insert(root, b1.isbn, b1)
    title_idx.insert(b1.title, b1.isbn)
    author_idx.insert(b1.author, b1.isbn)
    member_db.insert(m1.member_id, m1)

    # 4. Search Verification (Title -> ISBN -> AVL)
    found_isbn = title_idx.search("effective python")
    assert found_isbn == "9780134685991"
    book_details = catalog.search(root, found_isbn)
    assert book_details.book.author == "brett slatkin"

    # 5. Author Search (Returns List)
    author_isbns = author_idx.search("Brett Slatkin")
    assert "9780134685991" in author_isbns

    print("All individual data structure tests passed!")

if __name__ == "__main__":
    run_tests()