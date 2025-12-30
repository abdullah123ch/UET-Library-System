import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.HashTable import HashTable

def test_title_index():
    # Initialize index with capacity for 50 books [cite: 8]
    title_index = HashTable(size=50)

    # 1. Normalizing keys as required 
    title1 = "  Clean Code  ".strip().lower() 
    isbn1 = "9780132350884"

    # 2. Testing Insert [cite: 56]
    title_index.insert(title1, isbn1)
    print(f"Inserted: {title1} -> {isbn1}")

    # 3. Testing Search (Exact matching) [cite: 28]
    result = title_index.search("clean code")
    print(f"Search 'clean code': {'Found ' + result if result else 'Not Found'}")

    # 4. Testing Collision (using a small table size to force chaining)
    collision_test = HashTable(size=2)
    collision_test.insert("title a", "111")
    collision_test.insert("title b", "222")
    print("Collision search 'title b':", collision_test.search("title b"))

    # 5. Testing Delete [cite: 56]
    collision_test.delete("title a")
    print("Search 'title a' after delete:", collision_test.search("title a"))

if __name__ == "__main__":
    test_title_index()