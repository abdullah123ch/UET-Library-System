class HashNode:
    """
    Node class for the Hash Table chaining.
    """
    def __init__(self, key, value):
        self.key = key       
        self.value = value  
        self.next = None
 
class HashTable:
    """
    Generic Hash Table implementation using chaining for collision resolution.
    """
    def __init__(self, size=50):
        self.size = size
        self.table = [None] * self.size

    def _hash(self, key):
        """
        Computes the index for a given key.
        """
        return hash(key) % self.size

    def insert(self, key, value):
        """
        Inserts a key-value pair into the hash table.
        If the key already exists, updates the value.
        """
        index = self._hash(key)
        
        if self.table[index] is None:
            self.table[index] = HashNode(key, value)
        else:
            current = self.table[index]
            while current:
                if current.key == key:
                    current.value = value 
                    return
                if current.next is None:
                    break
                current = current.next
            current.next = HashNode(key, value)

    def search(self, key):
        """
        Searches for a value by key.
        
        Returns:
            The value associated with the key, or None if not found.
        """
        index = self._hash(key)
        current = self.table[index]
        
        while current:
            if current.key == key:
                return current.value
            current = current.next
        return None 

    def delete(self, key):
        """
        Deletes a key-value pair from the hash table.
        
        Returns:
            bool: True if deletion was successful, False if key not found.
        """
        index = self._hash(key)
        current = self.table[index]
        prev = None
        
        while current:
            if current.key == key:
                if prev:
                    prev.next = current.next
                else:
                    self.table[index] = current.next
                return True
            prev = current
            current = current.next
        return False