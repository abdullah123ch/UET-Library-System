import sys
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from src.System import LibrarySystem
from src.Models import Book, Member

console = Console()

def display_menu():
    """
    Renders the main menu UI using Rich.
    
    This function creates a panel with a list of available options for the user
    and prints it to the console.
    """
    console.print("\n")
    menu_content = (
        "[bold green]1.[/bold green] Add New Book\n"
        "[bold green]2.[/bold green] Register Member\n"
        "[bold green]3.[/bold green] Search Book (ISBN/Title/Author)\n"
        "[bold green]4.[/bold green] Borrow Book\n"
        "[bold green]5.[/bold green] Return Book\n"
        "[bold green]6.[/bold green] List All Books (Sorted by ISBN)\n"
        "[bold green]L.[/bold green] Load Bulk Data (CSV)\n"
        "[bold red]0.[/bold red] Exit"
    )
    console.print(Panel(menu_content, title="[bold cyan]UET Library Management System[/bold cyan]", subtitle="EE234L Project"))

def main():
    """
    The main execution loop of the library management system.
    
    Initializes the LibrarySystem, loads initial data if available, and enters
    an infinite loop to process user commands via the CLI menu.
    """
    library = LibrarySystem()
    if os.path.exists('data/books.csv'):
        library.loadBooksCSV('data/books.csv')

    while True:
        display_menu()
        choice = Prompt.ask("Select an option", default="0").upper()
        
        if choice == "1":
            isbn = Prompt.ask("Enter 13-digit ISBN")
            title = Prompt.ask("Enter Title")
            author = Prompt.ask("Enter Author")
            year = Prompt.ask("Enter Year")
            category = Prompt.ask("Enter Category")
            copies = Prompt.ask("Enter Copies", default="1")
            
            new_book = Book(isbn, title, author, year, category, copies)
            library.addBook(new_book)
            console.print(f"[bold green]Success:[/bold green] '{title}' added to system.")

        elif choice == "2":
            m_id = Prompt.ask("Enter Member ID (e.g., 2024-EE-001)")
            name = Prompt.ask("Enter Member Name")
            newMember = Member(m_id, name)
            library.addMember(newMember)
            console.print(f"[bold green]Success:[/bold green] Member '{name}' registered.")

        elif choice == "3":
            search_type = Prompt.ask("Search by", choices=["ISBN", "Title", "Author"])
            query = Prompt.ask(f"Enter {search_type}")
            
            results = []
            if search_type == "ISBN":
                res = library.isbnSearch(query)
                if res: results.append(res)
            elif search_type == "Title":
                res = library.titleSearch(query)
                if res: results.append(res)
            else:
                results = library.authorSearch(query)

            if results:
                table = Table(title=f"Search Results for '{query}'")
                table.add_column("ISBN", style="cyan")
                table.add_column("Title")
                table.add_column("Author")
                table.add_column("Available", justify="right")
                for b in results:
                    table.add_row(b.isbn, b.title.title(), b.author.title(), str(b.available_copies))
                console.print(table)
            else:
                console.print("[bold red]No books found.[/bold red]")

        elif choice == "4":
            m_id = Prompt.ask("Enter Member ID")
            isbn = Prompt.ask("Enter Book ISBN")
            success, msg = library.borrowBook(m_id, isbn)
            color = "green" if success else "red"
            console.print(f"[bold {color}]{msg}[/bold {color}]")

        elif choice == "5":
            m_id = Prompt.ask("Enter Member ID")
            isbn = Prompt.ask("Enter Book ISBN")
            success, msg = library.returnBooks(m_id, isbn)
            color = "green" if success else "red"
            console.print(f"[bold {color}]{msg}[/bold {color}]")

        elif choice == "6":
            console.print("\n[bold cyan]--- Reporting Sub-Menu ---[/bold cyan]")
            console.print("A. List by Author")
            console.print("M. List by Member")
            console.print("V. List All Available")
            console.print("S. List All (Sorted by ISBN)")
            
            sub_choice = Prompt.ask("Select Report", choices=["A", "M", "V", "S"]).upper()
            
            report_books = []
            title_text = ""

            if sub_choice == "A":
                author = Prompt.ask("Enter Author Name")
                report_books = library.listByAuthor(author)
                title_text = f"Books by {author.title()}"
            elif sub_choice == "M":
                m_id = Prompt.ask("Enter Member ID")
                report_books = library.listByMember(m_id)
                title_text = f"Books borrowed by {m_id}"
            elif sub_choice == "V":
                report_books = library.listAll()
                title_text = "Currently Available Books"
            elif sub_choice == "S":
                report_books = library.listAllSorted()
                title_text = "Complete Catalog (Sorted by ISBN)"

            if report_books:
                table = Table(title=title_text)
                table.add_column("ISBN", style="cyan")
                table.add_column("Title")
                table.add_column("Author")
                table.add_column("Available", justify="right")
                for b in report_books:
                    table.add_row(b.isbn, b.title.title(), b.author.title(), str(b.available_copies))
                console.print(table)
            else:
                console.print("[yellow]No records found for this report.[/yellow]")

        elif choice == "L":
            success, msg = library.loadBooksCSV('data/books.csv')
            console.print(f"[bold blue]{msg}[/bold blue]")

        elif choice == "0":
            console.print("[bold yellow]Exiting Library System. Goodbye![/bold yellow]")
            sys.exit()

if __name__ == "__main__":
    main()