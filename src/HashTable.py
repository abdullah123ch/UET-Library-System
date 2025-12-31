class HashNode:
    def __init__(self, key, value):
        self.key = key       
        self.value = value  
        self.next = None
 
class HashTable:
    def __init__(self, size=50):
        self.size = size
        self.table = [None] * self.size

    def _hash(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
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
        index = self._hash(key)
        current = self.table[index]
        
        while current:
            if current.key == key:
                return current.value
            current = current.next
        return None 

    def delete(self, key):
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