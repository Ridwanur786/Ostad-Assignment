import sys
from library import Library


def pause():
    """Pauses until the user presses Enter, safely handling non-interactive runs."""
    try:
        input("\nPress Enter to continue...")
    except (EOFError, KeyboardInterrupt):
        pass


def main():
    library = Library()

    while True:
        print("\n=========================================")
        print("LIBRARY MANAGEMENT SYSTEM")
        print("=========================================")
        print("1. Add Book")
        print("2. Register Member")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Show All Books")
        print("6. Show All Members")
        print("7. Search Book")
        print("8. Exit")

        try:
            choice = input("\nEnter your choice: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nThank you for using Library Management System.\nGoodbye!")
            break

        if choice == "1":
            print("\n----- Add New Book -----")
            try:
                title = input("Enter Book Title : ")
                author = input("Enter Author : ")
                isbn = input("Enter ISBN : ")
                library.add_book(title, author, isbn)
            except Exception as e:
                print(f"Error: {e}")
            pause()

        elif choice == "2":
            print("\n----- Register Member -----")
            try:
                member_id = input("Enter Member ID : ")
                name = input("Enter Name : ")
                age_input = input("Enter Age : ").strip()

                try:
                    age = int(age_input)
                except ValueError:
                    print("Error: Age must be a valid number.")
                    pause()
                    continue

                library.register_member(member_id, name, age)
            except Exception as e:
                print(f"Error: {e}")
            pause()

        elif choice == "3":
            print("\n------ Borrow Book ------")
            try:
                member_id = input("Enter Member ID : ")
                isbn = input("Enter Book ISBN : ")
                library.borrow_book(member_id, isbn)
            except Exception as e:
                print(f"Error: {e}")
            pause()

        elif choice == "4":
            print("\n------ Return Book ------")
            try:
                member_id = input("Enter Member ID : ")
                isbn = input("Enter Book ISBN : ")
                library.return_book(member_id, isbn)
            except Exception as e:
                print(f"Error: {e}")
            pause()

        elif choice == "5":
            print()
            library.show_books()
            pause()

        elif choice == "6":
            print()
            library.show_members()
            pause()

        elif choice == "7":
            print("\n------ Search Book ------")
            try:
                title = input("Enter Book Title : ")
                print()
                library.search_book(title)
            except Exception as e:
                print(f"Error: {e}")
            pause()

        elif choice == "8":
            print("\nThank you for using Library Management System.")
            print("Goodbye!")
            break

        else:
            print("\nInvalid choice! Please select a valid option (1-8).")
            pause()


if __name__ == "__main__":
    main()
