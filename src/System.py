import csv
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.Models import Book, Member
from src.Avl import AVLTree
from src.HashTable import HashTable
from src.AuthorHashTable import AuthorHT

class LibrarySystem:
    """
    The main facade class for the Library Management System.
    
    This class integrates the AVL Tree (for the catalog) and Hash Tables
    (for indexes and member database) to provide high-level library operations.
    """
    def __init__(self):
        """
        Initialize the LibrarySystem with necessary data structures.
        
        - catalog: AVL Tree for storing books sorted by ISBN.
        - title_index: Hash Table for Title -> ISBN mapping.
        - author_index: Hash Table for Author -> [ISBNs] mapping.
        - member_db: Hash Table for MemberID -> Member mapping.
        """
        self.catalog = AVLTree()
        self.root = None  
        
        self.title_index = HashTable(size=50)
        self.author_index = AuthorHT(size=50)
        self.member_db = HashTable(size=50)

    def addBook(self, book):
        """
        Adds a new book to the library catalog and updates all secondary indexes.
        
        Args:
            book (Book): The Book object to be added.
        """
        self.root = self.catalog.insert(self.root, book.isbn, book)
        self.title_index.insert(book.title, book.isbn)
        self.author_index.insert(book.author, book.isbn)

    def addMember(self, member):
        """
        Registers a new member in the member database.
        
        Args:
            member (Member): The Member object to be added.
        """
        self.member_db.insert(member.member_id, member)

    def isbnSearch(self, isbn):
        """
        Searches for a book by its ISBN using the AVL Tree.
        
        Args:
            isbn (str): The ISBN to search for.
            
        Returns:
            Book: The book object if found, else None.
        """
        node = self.catalog.search(self.root, isbn)
        return node.book if node else None

    def titleSearch(self, title):
        """
        Searches for a book by its Title using the Hash Table index.
        
        Args:
            title (str): The title of the book.
            
        Returns:
            Book: The book object if found, else None.
        """
        isbn = self.title_index.search(title.strip().lower())
        if isbn:
            return self.isbnSearch(isbn)
        return None

    def authorSearch(self, author):
        """
        Searches for books by a specific Author.
        
        Args:
            author (str): The name of the author.
            
        Returns:
            list[Book]: A list of Book objects written by the author.
        """
        isbns = self.author_index.search(author)
        books = []
        for isbn in isbns:
            book = self.isbnSearch(isbn)
            if book:
                books.append(book)
        return books

    def borrowBook(self, member_id, isbn):
        """
        Processes a book borrowing request.
        
        Checks if the member exists, the book exists, copies are available,
        and if the member has not exceeded their borrowing limit.
        
        Args:
            member_id (str): ID of the member.
            isbn (str): ISBN of the book to borrow.
            
        Returns:
            tuple: (bool, str) indicating success/failure and a message.
        """
        member = self.member_db.search(member_id)
        bookNode = self.catalog.search(self.root, isbn)

        if not member: return False, "Member not found."
        if not bookNode: return False, "Book not found."
        
        book = bookNode.book
        if book.available_copies <= 0:
            return False, "No copies available."
        if len(member.borrowedBooks) >= 5:
            return False, "Member has reached the 5-book limit."

        book.available_copies -= 1
        member.borrowedBooks.append(isbn)
        return True, f"Successfully borrowed '{book.title.title()}'."

    def returnBooks(self, member_id, isbn):
        """
        Processes a book return.
        
        Args:
            member_id (str): ID of the member.
            isbn (str): ISBN of the book to return.
            
        Returns:
            tuple: (bool, str) indicating success/failure and a message.
        """
        member = self.member_db.search(member_id)
        bookNode = self.catalog.search(self.root, isbn)

        if member and isbn in member.borrowedBooks:
            member.borrowedBooks.remove(isbn)
            if bookNode:
                bookNode.book.available_copies += 1 
            return True, "Book returned successfully."
        return False, "Return failed: Book not found in member's list."

    def allSort(self):
        books = []
        self.catalog.inorder(self.root, books)
        return books

    def listByAuthor(self, authorName):
        """
        Lists all books by a given author.
        
        Args:
            authorName (str): Name of the author.
            
        Returns:
            list[Book]: List of books.
        """
        isbns = self.author_index.search(authorName)
        books = []
        
        for isbn in isbns:
            bookNode = self.catalog.search(self.root, isbn)
            if bookNode:
                books.append(bookNode.book)
        return books

    def listByMember(self, member_id):
        """
        Lists all books currently borrowed by a member.
        
        Args:
            member_id (str): ID of the member.
            
        Returns:
            list[Book]: List of borrowed books.
        """
        member = self.member_db.search(member_id)
        if not member:
            return None
        
        books = []
        for isbn in member.borrowedBooks:
            bookNode = self.catalog.search(self.root, isbn)
            if bookNode:
                books.append(bookNode.book)
        return books

    def listAll(self):
        """
        Lists all books that have at least one copy available.
        
        Returns:
            list[Book]: List of available books.
        """
        all_books = []
        self.catalog.inorder(self.root, all_books)  
        
        available_books = [b for b in all_books if b.available_copies > 0]
        return available_books

    def listAllSorted(self):
        """
        Lists all books in the catalog, sorted by ISBN (AVL In-order traversal).
        
        Returns:
            list[Book]: All books in the system.
        """
        sorted_books = []
        self.catalog.inorder(self.root, sorted_books) 
        return sorted_books    
    
    def loadBooksCSV(self, file_path):
        """
        Loads books from a CSV file into the system.
        
        Args:
            file_path (str): Path to the CSV file.
            
        Returns:
            tuple: (bool, str) indicating success/failure and status message.
        """
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file) 
                count = 0
                for row in reader:
                    new_book = Book(
                        isbn=row['ISBN'],
                        title=row['Title'],
                        author=row['Author'],
                        year=row['Year'],
                        category=row['Category'],
                        copies=row['TotalCopies']
                    )
                    self.addBook(new_book)
                    count += 1
                return True, f"Successfully loaded {count} books."
        except FileNotFoundError:
            return False, "Error: books.csv file not found."
        except Exception as e:
            return False, f"An error occurred: {str(e)}"

    def loadMembersCSV(self, file_path):
        """
        Loads members from a CSV file into the system.
        
        Args:
            file_path (str): Path to the CSV file.
            
        Returns:
            tuple: (bool, str) indicating success/failure and status message.
        """
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                count = 0
                for row in reader:
                    newMember = Member(
                        member_id=row['MemberID'],
                        name=row['Name']
                    )
                    self.addMember(newMember)
                    count += 1
                return True, f"Successfully registered {count} members."
        except FileNotFoundError:
            return False, "Error: members.csv file not found."