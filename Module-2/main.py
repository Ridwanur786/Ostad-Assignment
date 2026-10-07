import os

FILE_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expenses.txt")


def get_file_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    local_file = os.path.join(script_dir, "expenses.txt")
    if os.path.exists("expenses.txt") and not os.path.exists(local_file):
        return "expenses.txt"
    return local_file


def format_amount(amount):
    if amount == int(amount):
        return f"{int(amount)}"
    return f"{amount:.2f}"


def load_expenses():
    file_path = get_file_path()
    if not os.path.exists(file_path):
        raise FileNotFoundError("No expense records found.")

    with open(file_path, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file if line.strip()]

    if not lines:
        raise ValueError("No expenses available.")

    expenses = []
    for line in lines:
        parts = line.split(",")
        if len(parts) >= 5:
            try:
                amt = float(parts[4].strip())
            except ValueError:
                continue
            expenses.append({
                "id": parts[0].strip(),
                "date": parts[1].strip(),
                "category": parts[2].strip(),
                "description": parts[3].strip(),
                "amount": amt,
                "raw_amount": parts[4].strip()
            })

    if not expenses:
        raise ValueError("No expenses available.")

    return expenses


def save_expenses(expenses):
    file_path = get_file_path()
    with open(file_path, "w", encoding="utf-8") as file:
        for exp in expenses:
            file.write(f"{exp['id']},{exp['date']},{exp['category']},{exp['description']},{exp['raw_amount']}\n")


def add_expense():
    expense_id = input("Expense ID: ").strip()
    date = input("Date (YYYY-MM-DD): ").strip()
    category = input("Category: ").strip()
    description = input("Description: ").strip()
    amount_input = input("Amount: ").strip()

    try:
        amount = float(amount_input)
        if amount < 0:
            print("Amount cannot be negative.")
            return
    except ValueError:
        print("Invalid amount! Please enter a valid number.")
        return

    raw_amount = str(int(amount)) if amount == int(amount) else f"{amount:.2f}"

    file_path = get_file_path()
    record = f"{expense_id},{date},{category},{description},{raw_amount}\n"

    with open(file_path, "a", encoding="utf-8") as file:
        file.write(record)

    print("\nExpense added successfully.")


def view_expenses():
    try:
        expenses = load_expenses()
    except FileNotFoundError:
        print("No expense records found.")
        return
    except ValueError:
        print("No expenses available.")
        return

    print("------------------------------------")
    for exp in expenses:
        print(f"Expense ID : {exp['id']}")
        print(f"Date : {exp['date']}")
        print(f"Category : {exp['category']}")
        print(f"Description: {exp['description']}")
        print(f"Amount : {format_amount(exp['amount'])}")
        print("------------------------------------")


def search_expense():
    try:
        expenses = load_expenses()
    except FileNotFoundError:
        print("No expense records found.")
        return
    except ValueError:
        print("No expenses available.")
        return

    search_id = input("Expense ID: ").strip()

    for exp in expenses:
        if exp["id"] == search_id:
            print("\nExpense Found")
            print(f"Expense ID : {exp['id']}")
            print(f"Date : {exp['date']}")
            print(f"Category : {exp['category']}")
            print(f"Description: {exp['description']}")
            print(f"Amount : {format_amount(exp['amount'])}")
            return

    print("Expense not found.")


def update_expense():
    try:
        expenses = load_expenses()
    except FileNotFoundError:
        print("No expense records found.")
        return
    except ValueError:
        print("No expenses available.")
        return

    update_id = input("Expense ID: ").strip()

    found_idx = None
    for idx, exp in enumerate(expenses):
        if exp["id"] == update_id:
            found_idx = idx
            break

    if found_idx is None:
        print("Expense not found.")
        return

    new_date = input("Date (YYYY-MM-DD): ").strip()
    new_category = input("Category: ").strip()
    new_description = input("Description: ").strip()
    amount_input = input("Amount: ").strip()

    try:
        amount = float(amount_input)
        if amount < 0:
            print("Amount cannot be negative.")
            return
    except ValueError:
        print("Invalid amount! Please enter a valid number.")
        return

    raw_amount = str(int(amount)) if amount == int(amount) else f"{amount:.2f}"

    expenses[found_idx] = {
        "id": update_id,
        "date": new_date,
        "category": new_category,
        "description": new_description,
        "amount": amount,
        "raw_amount": raw_amount
    }

    save_expenses(expenses)
    print("\nExpense updated successfully.")


def delete_expense():
    try:
        expenses = load_expenses()
    except FileNotFoundError:
        print("No expense records found.")
        return
    except ValueError:
        print("No expenses available.")
        return

    delete_id = input("Expense ID: ").strip()

    found = False
    new_expenses = []
    for exp in expenses:
        if exp["id"] == delete_id:
            found = True
        else:
            new_expenses.append(exp)

    if not found:
        print("Expense not found.")
        return

    save_expenses(new_expenses)
    print("\nExpense deleted successfully.")


def expense_summary():
    try:
        expenses = load_expenses()
    except FileNotFoundError:
        print("No expense records found.")
        return
    except ValueError:
        print("No expenses available.")
        return

    total_expenses = len(expenses)
    total_spending = sum(exp["amount"] for exp in expenses)
    average_expense = total_spending / total_expenses
    highest_expense = max(exp["amount"] for exp in expenses)
    lowest_expense = min(exp["amount"] for exp in expenses)

    print("\n========= Expense Summary =========\n")
    print(f"Total Expenses : {total_expenses}\n")
    print(f"Total Spending : {format_amount(total_spending)} BDT\n")
    print(f"Average Expense : {average_expense:.2f} BDT\n")
    print(f"Highest Expense : {format_amount(highest_expense)} BDT\n")
    print(f"Lowest Expense : {format_amount(lowest_expense)} BDT")


def main():
    while True:
        print("\n========= Expense Tracker =========\n")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Search Expense")
        print("4. Update Expense")
        print("5. Delete Expense")
        print("6. Expense Summary")
        print("7. Exit\n")

        choice = input("Choose: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            search_expense()
        elif choice == "4":
            update_expense()
        elif choice == "5":
            delete_expense()
        elif choice == "6":
            expense_summary()
        elif choice == "7":
            break
        else:
            print("Invalid choice! Please select a valid option.")


if __name__ == "__main__":
    main()
