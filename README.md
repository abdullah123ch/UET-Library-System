# UET Library Management System (CEP)

## Overview

This is a **Library Management System** developed as a Complex Engineering Problem (CEP) for the **EE234L Data Structures & Algorithms** course. The system is designed to efficiently manage book records, member registrations, borrowing, and returning of books using advanced data structures.

The application provides a command-line interface (CLI) enhanced with the `rich` library for a user-friendly experience.

## Features

- **Book Management**: Add new books with details like ISBN, Title, Author, Year, Category, and Copies.
- **Member Management**: Register new library members.
- **Search Functionality**:
  - Search by **ISBN** (O(log n))
  - Search by **Title** (O(1) average)
  - Search by **Author** (O(1) average)
- **Borrowing & Returning**:
  - Check availability and member limits (max 5 books).
  - Update inventory in real-time.
- **Reporting**:
  - List books by a specific author.
  - List books borrowed by a specific member.
  - List all currently available books.
  - List all books sorted by ISBN.
- **Bulk Data Loading**: Load books and members from CSV files.

## Data Structures Used

The core efficiency of this system relies on the following data structures:

```markdown
| Feature | Data Structure | Reason for Choice |
| source | --- | --- |
| **Main Catalog** | **AVL Tree** | Ensures balanced height for efficient search, insertion, and deletion operations (O(log n)) based on ISBN. |
| **Title Index** | **Hash Table** | Provides fast O(1) average time complexity for looking up ISBNs by Book Title. |
| **Author Index** | **Hash Table with Chaining** | Maps Authors to lists of ISBNs, allowing efficient retrieval of all books by a specific author. |
| **Member Database** | **Hash Table** | Stores member records for quick O(1) access during borrowing/returning operations. |
```

## Prerequisites

- Python 3.x
- `rich` library for the CLI interface.

## Installation

1. Clone the repository.
2. Install the required dependencies:
   ```bash
   pip install rich
   ```

## Usage

Run the main application script:

```bash
python main.py
```

## Project Structure

- `main.py`: Entry point of the application, handles the UI and user input.
- `src/`: Contains the implementation of data structures and logic.
  - `System.py`: Core logic for the Library System (Facade pattern).
  - `Avl.py`: Implementation of the AVL Tree.
  - `HashTable.py`: Generic Hash Table implementation.
  - `AuthorHashTable.py`: specialized Hash Table for Author -> [ISBNs] mapping.
  - `Models.py`: Data models for `Book` and `Member`.
- `data/`: Directory for CSV data files (`books.csv`, `members.csv`).
- `test/`: Unit tests for the data structures.

## Contributors

- Project developed for **EE234L DSA Lab**.
