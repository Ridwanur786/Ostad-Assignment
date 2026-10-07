# Library Management System (Python OOP)

A console-based Library Management System developed using Object-Oriented Programming (OOP) concepts in Python for Ostad Python/Django Module-3 Assignment.

## Object-Oriented Programming (OOP) Concepts Demonstrated

1. **Classes and Objects**:
   - `Person`, `Member`, `Book`, `Library` classes.
2. **Constructors (`__init__`)**:
   - Initializing instance attributes across all classes.
3. **Inheritance & Method Overriding**:
   - `Member` class inherits from `Person` base class (`class Member(Person):`).
   - Overrides `display_info()` to include membership details and borrowed book counts while chaining `super()`.
4. **Encapsulation & Properties**:
   - `Book` class encapsulates `_available` attribute using `@property` getter and `@available.setter`.
5. **Class Variables & Class Methods**:
   - `total_books` and `total_members` track instance counts with `@classmethod` accessors.
6. **Static Methods**:
   - Helper validation methods such as `@staticmethod validate_age(age)` and `is_valid_isbn(isbn)`.
7. **Composition**:
   - `Library` class has-a relationship with `Book` and `Member` objects.
8. **Exception Handling**:
   - Catches invalid menu selections, negative/non-numeric ages, empty inputs, duplicate ISBNs, and duplicate Member IDs.

## Project Structure

```text
Module-3/
├── person.py    # Person base class
├── member.py    # Member child class (inherits from Person)
├── book.py      # Book class with encapsulated availability
├── library.py   # Library class with composition
├── main.py      # Console application runner with interactive menu
└── README.md    # Documentation
```

## How to Run

From the `Module-3` directory, run:

```bash
python main.py
```
