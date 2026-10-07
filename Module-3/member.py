from person import Person


class Member(Person):
    """Represents a library member, inheriting from Person."""

    total_members = 0  # Class variable

    def __init__(self, member_id: str, name: str, age: int):
        super().__init__(name, age)
        self.member_id = member_id
        self.borrowed_books = []  # List of Book objects
        Member.total_members += 1

    @classmethod
    def get_total_members(cls) -> int:
        """Class method returning total members created."""
        return cls.total_members

    @staticmethod
    def validate_age(age: int) -> bool:
        """Static method to validate member age."""
        return age > 0

    def borrow_book(self, book):
        """Appends book to member's borrowed list."""
        self.borrowed_books.append(book)

    def return_book(self, book):
        """Removes book from member's borrowed list."""
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)

    def display_info(self):
        """Overrides Person.display_info to display full member details."""
        print(f"Member ID : {self.member_id}")
        print(f"Name : {self.name}")
        print(f"Age : {self.age}")
        print(f"Borrowed Books : {len(self.borrowed_books)}")
