import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from src.models import Book

console = Console()

def display_menu():
    console.print("\n")
    menu_content = (
        "[bold green]1.[/bold green] Add New Book\n"
        "[bold green]2.[/bold green] Register Member\n"
        "[bold green]3.[/bold green] Search (ISBN/Title/Author)\n"
        "[bold green]4.[/bold green] Borrow Book\n"
        "[bold green]5.[/bold green] Return Book\n"
        "[bold green]6.[/bold green] List All Books (Sorted)\n"
        "[bold red]0.[/bold red] Exit"
    )
    console.print(Panel(menu_content, title="[bold cyan]UET Library Management System[/bold cyan]", subtitle="EE234L Project"))

def main():
    display_menu()

if __name__ == "__main__":
    main()