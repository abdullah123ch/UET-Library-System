class Book:
    """
    Represents a book in the library system.
    """
    def __init__(self, isbn, title, author, year, category, copies):
        """
        Initializes a Book instance.
        
        Args:
            isbn (str): Unique International Standard Book Number.
            title (str): Title of the book.
            author (str): Author of the book.
            year (str): Publication year.
            category (str): Genre/Category.
            copies (int): Total number of copies available.
        """
        self.isbn = str(isbn)  
        self.title = title.strip().lower()  
        self.author = author.strip().lower()  
        self.year = year
        self.category = category
        self.available_copies = int(copies)

class Member:
    """
    Represents a library member.
    """
    def __init__(self, member_id, name):
        """
        Initializes a Member instance.
        
        Args:
            member_id (str): Unique ID for the member.
            name (str): Full name of the member.
        """
        self.member_id = member_id  
        self.name = name
        self.borrowedBooks = []  