import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

FILE_NAME = "expenses.csv"

def initialize_file():
    """Create the CSV file if it doesn't exist."""
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Date", "Category", "Description", "Amount"])

def add_expense():
    """Add a new expense."""
    date = input("Enter date (YYYY-MM-DD) or press Enter for today: ")
    if not date:
        date = datetime.today().strftime("%Y-%m-%d")

    category = input("Enter category (e.g., Food, Transport, Bills): ")
    description = input("Enter description: ")
    amount = float(input("Enter amount: "))

    with open(FILE_NAME, mode="a", newline="") as file:
        writer = csv.writer(file)
        id = sum(1 for _ in open(FILE_NAME))  # count lines for ID
        writer.writerow([id, date, category, description, amount])

    print("✅ Expense added successfully!\n")

def view_expenses():
    """Display all expenses in a nice table."""
    try:
        df = pd.read_csv(FILE_NAME)
        if df.empty:
            print("No expenses found.")
        else:
            print("\n------ All Expenses ------")
            print(df.to_string(index=False))
            print("--------------------------\n")
    except FileNotFoundError:
        print("No expenses found. Try adding one first.")

def edit_expense():
    """Edit an existing expense by ID."""
    try:
        df = pd.read_csv(FILE_NAME)
        if df.empty:
            print("No expenses to edit.")
            return

        print(df.to_string(index=False))
        expense_id = int(input("\nEnter the ID of the expense to edit: "))

        if expense_id not in df["ID"].values:
            print("❌ Expense not found.")
            return

        print("\nLeave a field empty to keep the current value.")
        row = df.loc[df["ID"] == expense_id]

        new_date = input(f"Date ({row['Date'].values[0]}): ") or row["Date"].values[0]
        new_category = input(f"Category ({row['Category'].values[0]}): ") or row["Category"].values[0]
        new_description = input(f"Description ({row['Description'].values[0]}): ") or row["Description"].values[0]
        new_amount_input = input(f"Amount ({row['Amount'].values[0]}): ")
        new_amount = float(new_amount_input) if new_amount_input else row["Amount"].values[0]

        df.loc[df["ID"] == expense_id, ["Date", "Category", "Description", "Amount"]] = [
            new_date, new_category, new_description, new_amount
        ]
        df.to_csv(FILE_NAME, index=False)
        print("✅ Expense updated successfully!\n")

    except FileNotFoundError:
        print("No data found. Try adding an expense first.")

def delete_expense():
    """Delete an expense by ID."""
    try:
        df = pd.read_csv(FILE_NAME)
        if df.empty:
            print("No expenses to delete.")
            return

        print(df.to_string(index=False))
        expense_id = int(input("\nEnter the ID of the expense to delete: "))

        if expense_id not in df["ID"].values:
            print("❌ Expense not found.")
            return

        df = df[df["ID"] != expense_id]
        df.to_csv(FILE_NAME, index=False)
        print("🗑️ Expense deleted successfully!\n")

    except FileNotFoundError:
        print("No data found. Try adding an expense first.")

def summary_report():
    """Show total and category-wise spending summary + chart."""
    try:
        df = pd.read_csv(FILE_NAME)
        if df.empty:
            print("No data to summarize.")
            return
        
        total = df["Amount"].sum()
        print("\n💰 Total Spending: ₦{:.2f}".format(total))
        print("\n📊 Spending by Category:")
        summary = df.groupby("Category")["Amount"].sum()
        print(summary.to_string())

        # Optional bar chart
        show_chart = input("\nWould you like to see a bar chart? (y/n): ").lower()
        if show_chart == "y":
            summary.plot(kind="bar", color="skyblue", figsize=(8, 5))
            plt.title("Spending by Category")
            plt.xlabel("Category")
            plt.ylabel("Total Amount (₦)")
            plt.xticks(rotation=30)
            plt.tight_layout()
            plt.show()

        print()
    except FileNotFoundError:
        print("No data to summarize. Try adding an expense first.")

def main():
    initialize_file()
    while True:
        print("==== Expense Tracker ====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Edit Expense")
        print("4. Delete Expense")
        print("5. View Summary Report")
        print("6. Exit")

        choice = input("Choose an option: ")
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            edit_expense()
        elif choice == "4":
            delete_expense()
        elif choice == "5":
            summary_report()
        elif choice == "6":
            print("Goodbye! 👋")
            break
        else:
            print("Invalid choice, try again.\n")

if __name__ == "__main__":
    main()
