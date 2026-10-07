class Book:
    """Represents a book in the library."""

    total_books = 0  # Class variable

    def __init__(self, title: str, author: str, isbn: str, available: bool = True):
        self.title = title
        self.author = author
        self.isbn = isbn
        self._available = available  # Private attribute for encapsulation
        Book.total_books += 1

    @property
    def available(self) -> bool:
        """Getter for available status."""
        return self._available

    @available.setter
    def available(self, status: bool):
        """Setter for available status."""
        if not isinstance(status, bool):
            raise TypeError("Available status must be a boolean.")
        self._available = status

    @classmethod
    def get_total_books(cls) -> int:
        """Class method to get the total number of book instances created."""
        return cls.total_books

    @staticmethod
    def is_valid_isbn(isbn: str) -> bool:
        """Static method to validate non-empty ISBN format."""
        return bool(isbn and isbn.strip())

    def display_book(self):
        """Displays formatted book information."""
        status_str = "Available" if self.available else "Borrowed"
        print(f"ISBN : {self.isbn}")
        print(f"Title : {self.title}")
        print(f"Author : {self.author}")
        print(f"Status : {status_str}")
