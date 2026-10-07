# Expense Tracker Application (Module-2 Assignment)

A command-line Expense Tracker application built with Python according to the **Django-12_Module-2_Assignment** specification.

## Features & Requirements Implemented
- **Add Expense**: Prompts for Expense ID, Date (YYYY-MM-DD), Category, Description, and Amount. Appends record to `expenses.txt`.
- **View All Expenses**: Displays all recorded expenses in a formatted, readable view.
- **Search Expense**: Finds and displays expense details by Expense ID.
- **Update Expense**: Modifies Date, Category, Description, and Amount for a given Expense ID.
- **Delete Expense**: Removes an expense entry by Expense ID.
- **Expense Summary**: Calculates and displays:
  - Total number of expenses
  - Total amount spent (in BDT)
  - Average expense (in BDT)
  - Highest expense (in BDT)
  - Lowest expense (in BDT)
- **Exception Handling**:
  - `Invalid Amount`: Detects non-numeric amount inputs and displays `Invalid amount! Please enter a valid number.`
  - `Negative Amount`: Detects negative values and displays `Amount cannot be negative.`
  - `File Not Found`: Displays `No expense records found.` if `expenses.txt` does not exist.
  - `Empty File`: Displays `No expenses available.` if `expenses.txt` is empty.
  - `Invalid Menu Option`: Displays `Invalid choice! Please select a valid option.` for invalid selections.

## Required Functions
- `add_expense()`
- `view_expenses()`
- `search_expense()`
- `update_expense()`
- `delete_expense()`
- `expense_summary()`
- `main()`

## How to Run

Navigate to `Module-2` and run:

```bash
python main.py
```
*(or `python expense_tracker.py`)*
