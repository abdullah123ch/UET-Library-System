import sys
import os
# Adjust path to import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.Models import Book, Member
from src.System import LibrarySystem

def run_tests():
    lib = LibrarySystem()
    print("--- 1. Testing Edge Case: Empty Library ---")
    # Verify reporting on empty system
    assert lib.allSort() == []
    assert lib.titleSearch("Non-existent") is None
    print("✓ Empty library operations handled correctly.")

    print("\n--- 2. Testing Bulk Loading (50+ Books, 20+ Members) ---")
    # Load bulk data from CSV files
    success_b, msg_b = lib.loadBooksCSV('data/books.csv')
    success_m, msg_m = lib.loadMembersCSV('data/members.csv')
    
    print(f"Books: {msg_b}")
    print(f"Members: {msg_m}")
    
    all_books = lib.allSort()
    assert len(all_books) >= 50, "Failed to load at least 50 books"
    print(f"✓ Successfully verified {len(all_books)} books in system.")

    print("\n--- 3. Testing Search Operations ---")
    # Test AVL Tree search by ISBN
    target_isbn = all_books[10].isbn
    found_isbn = lib.isbnSearch(target_isbn)
    assert found_isbn.isbn == target_isbn
    
    # Test Hash Table search by Title (Normalized)
    target_title = all_books[5].title
    found_title = lib.titleSearch(target_title)
    assert found_title.title == target_title
    print("✓ Search operations (ISBN and Title) verified.")

    print("\n--- 4. Testing Borrowing and Edge Cases ---")
    member_id = "2024-EE-001"
    book_isbn = all_books[0].isbn
    
    # Test standard borrowing
    success, msg = lib.borrowBook(member_id, book_isbn)
    print(f"Borrowing: {msg}")
    
    # Edge Case: Borrowing when copies are 0
    # Manually set copies to 0 for a test book
    empty_book = all_books[1]
    empty_book.available_copies = 0
    success, msg = lib.borrowBook(member_id, empty_book.isbn)
    print(f"Edge Case (0 copies): {msg}")
    assert success is False
    
    # Edge Case: Member 5-book limit
    # Borrow 4 more books to reach the limit
    for i in range(2, 6):
        lib.borrowBook(member_id, all_books[i].isbn)
    
    # Attempt to borrow the 6th book
    success, msg = lib.borrowBook(member_id, all_books[6].isbn)
    print(f"Edge Case (5-book limit): {msg}")
    assert success is False
    print("✓ Borrowing constraints enforced.")

    print("\n--- 5. Testing Return Operations ---")
    # Return a book and verify copy increment
    initial_copies = all_books[0].available_copies
    success, msg = lib.returnBooks(member_id, all_books[0].isbn)
    assert all_books[0].available_copies == initial_copies + 1
    print(f"Return: {msg}")
    print("✓ Return operations verified.")

if __name__ == "__main__":
    run_tests()