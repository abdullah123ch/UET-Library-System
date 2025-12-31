import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.AuthorHashTable import AuthorHT 

def test_author_hash_table():
    at = AuthorHT(size=10)
    
    print("--- Testing Author Hash Table ---")

    print("\n1. Testing one author with multiple ISBNs...")
    at.insert("Robert Martin", "9780132350884")
    at.insert("Robert Martin", "9780134494166")
    at.insert("Robert Martin", "9780135957059")
    
    isbns = at.search("Robert Martin")
    print(f"ISBNs for Robert Martin: {isbns}")
    assert len(isbns) == 3, "Should have 3 ISBNs stored"
    assert "9780132350884" in isbns

    print("\n2. Testing normalization (case and spaces)...")
    at.insert("  BRETT SLATKIN  ", "9781491912058")
    
    res = at.search("brett slatkin")
    print(f"Search 'brett slatkin': {res}")
    assert "9781491912058" in res, "Should find the ISBN despite casing/spaces"

    print("\n3. Testing collision handling...")
    at.insert("Author A", "111")
    at.insert("Author B", "222")
    
    isbns_a = at.search("Author A")
    isbns_b = at.search("Author B")
    print(f"Author A: {isbns_a}")
    print(f"Author B: {isbns_b}")
    assert "111" in isbns_a
    assert "222" in isbns_b

    print("\n4. Testing search for non-existent author...")
    missing = at.search("Unknown Author")
    print(f"Search 'Unknown Author': {missing}")
    assert missing == [], "Should return an empty list for missing authors"

    print("\n[SUCCESS] All AuthorHashTable tests passed.")

if __name__ == "__main__":
    test_author_hash_table()