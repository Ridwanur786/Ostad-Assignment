from book import Book
from member import Member


class Library:
    """Manages the collection of books and registered members through composition."""

    def __init__(self):
        self.books = []  # List of Book objects
        self.members = []  # List of Member objects

    def find_book(self, isbn: str):
        """Helper to find a book by ISBN."""
        for book in self.books:
            if book.isbn.lower() == isbn.lower():
                return book
        return None

    def find_member(self, member_id: str):
        """Helper to find a member by Member ID."""
        for member in self.members:
            if member.member_id.lower() == member_id.lower():
                return member
        return None

    def add_book(self, title: str, author: str, isbn: str):
        """Adds a new book after validation."""
        if not title or not title.strip():
            print("Error: Book title cannot be empty.")
            return False
        if not author or not author.strip():
            print("Error: Author name cannot be empty.")
            return False
        if not isbn or not isbn.strip():
            print("Error: ISBN cannot be empty.")
            return False

        if self.find_book(isbn.strip()):
            print("Error: ISBN already exists.")
            return False

        new_book = Book(title.strip(), author.strip(), isbn.strip())
        self.books.append(new_book)
        print("\nBook added successfully!")
        return True

    def register_member(self, member_id: str, name: str, age: int):
        """Registers a new member after validation."""
        if not member_id or not member_id.strip():
            print("Error: Member ID cannot be empty.")
            return False
        if not name or not name.strip():
            print("Error: Name cannot be empty.")
            return False
        if age <= 0:
            print("Error: Age must be greater than 0.")
            return False

        if self.find_member(member_id.strip()):
            print("Error: Member ID already exists.")
            return False

        new_member = Member(member_id.strip(), name.strip(), age)
        self.members.append(new_member)
        print("\nMember registered successfully!")
        return True

    def borrow_book(self, member_id: str, isbn: str):
        """Allows a registered member to borrow an available book."""
        member = self.find_member(member_id.strip())
        if not member:
            print("Member not found.")
            return False

        book = self.find_book(isbn.strip())
        if not book:
            print("Book not found.")
            return False

        if not book.available:
            print("Sorry! This book is currently unavailable.")
            return False

        if book in member.borrowed_books:
            print("Error: Member has already borrowed this book.")
            return False

        book.available = False
        member.borrow_book(book)
        print("\nBook borrowed successfully.")
        return True

    def return_book(self, member_id: str, isbn: str):
        """Allows a member to return a borrowed book."""
        member = self.find_member(member_id.strip())
        if not member:
            print("Member not found.")
            return False

        book = self.find_book(isbn.strip())
        if not book:
            print("Book not found.")
            return False

        if book not in member.borrowed_books:
            print("Error: This member has not borrowed this book.")
            return False

        book.available = True
        member.return_book(book)
        print("\nBook returned successfully.")
        return True

    def show_books(self):
        """Displays all books currently registered in the library."""
        if not self.books:
            print("------------- BOOK LIST -------------")
            print("No books available in the library.")
            print("-------------------------------------")
            return

        print("------------- BOOK LIST -------------")
        for book in self.books:
            book.display_book()
            print("-------------------------------------")

    def show_members(self):
        """Displays all registered members in the library."""
        if not self.members:
            print("----------- MEMBER LIST ------------")
            print("No members registered yet.")
            print("------------------------------------")
            return

        print("----------- MEMBER LIST ------------")
        for member in self.members:
            member.display_info()
            print("------------------------------------")

    def search_book(self, title: str):
        """Searches for a book by title."""
        if not title or not title.strip():
            print("Error: Search title cannot be empty.")
            return False

        search_query = title.strip().lower()
        found_book = None
        for book in self.books:
            if book.title.lower() == search_query:
                found_book = book
                break

        if found_book:
            print("Book Found!\n")
            found_book.display_book()
            return True

        print("Book not found.")
        return False
