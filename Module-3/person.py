class Person:
    """Base class representing a person."""

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def display_info(self):
        """Displays basic information of the person."""
        print(f"Name : {self.name}")
        print(f"Age : {self.age}")
