class Book:
    def __init__(self, isbn, title, author, year, category, copies):
        self.isbn = str(isbn)  
        self.title = title.strip().lower()  
        self.author = author.strip().lower()  
        self.year = year
        self.category = category
        self.available_copies = int(copies)

class Member:
    def __init__(self, member_id, name):
        self.member_id = member_id  
        self.name = name
        self.borrowedBooks = []  