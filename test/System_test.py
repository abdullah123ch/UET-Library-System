import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.System import LibrarySystem
from src.Models import Book, Member

def test_full_system():
    lib = LibrarySystem()
    
    # Setup Data
    book1 = Book("9780134685991", "Effective Python", "Brett Slatkin", 2019, "Tech", 1)
    member1 = Member("2024-EE-001", "Ali")
    
    lib.addBook(book1)
    lib.addMember(member1)

    print("--- Testing Search ---")
    # Search Title -> Hash Table -> AVL Tree
    found = lib.titleSearch("Effective Python")
    assert found.isbn == "9780134685991"
    print("Title search integrated successfully.")

    print("\n--- Testing Borrowing ---")
    # First borrow
    success, msg = lib.borrowBook("2024-EE-001", "9780134685991")
    print(msg)
    
    # Attempt borrow when copies = 0 (Edge Case) 
    success, msg = lib.borrowBook("2024-EE-001", "9780134685991")
    print(f"Second attempt: {msg}")
    assert success is False

    print("\n--- Testing Return ---")
    success, msg = lib.returnBooks("2024-EE-001", "9780134685991")
    print(msg)
    assert book1.available_copies == 1

if __name__ == "__main__":
    test_full_system()