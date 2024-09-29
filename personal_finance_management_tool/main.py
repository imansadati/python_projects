import json
import csv
import sys
import matplotlib.pyplot as plt


class User:

    def __init__(self, name) -> None:
        self.name = name
        self.balance = 0
        self.income = 0
        self.expenses = 0
        self.transactions = []

    def add_income(self, amount):
        self.income += amount
        self.balance += amount
        self.transactions.append({'type': 'Income', 'amount': amount})
        print(f"Income of ${amount} added.")

    def add_expense(self, amount, category):
        if amount > self.balance:
            print('Insufficient balance!')
        else:
            self.expenses += amount
            self.balance -= amount
            self.transactions.append(
                {'type': 'Expense', 'amount': amount, 'category': category})
            print(f"Expense of ${amount} added under {category}.")

    def view_balance(self):
        return f"Current balance: ${self.balance}"


def save_transactions(user):
    with open(f'{user.name}_transactions.json', 'w') as file:
        json.dump(user.transactions, file)
    print("Transactions saved.")


def load_transactions(user):
    try:
        with open(f'{user.name}_transactions.json', 'r') as file:
            user.transactions = json.load(file)
            print("Transactions loaded.")
    except FileNotFoundError:
        print("No previous transactions found.")


def generate_spending_report(user):
    categories = {}
    for transaction in user.transactions:
        if transaction['type'] == 'Expense':
            category = transaction['category']
            amount = transaction['amount']
            if category in categories:
                categories[category] += amount
            else:
                categories[category] = amount

    labels = categories.keys()
    sizes = categories.values()

    # Creating the pie chart
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    # Equal aspect ratio ensures the pie is drawn as a circle.
    plt.axis('equal')
    plt.title(f"Spending Report for {user.name}")
    plt.show()


class Budget:

    def __init__(self, user, budget_limit):
        self.user = user
        self.budget_limit = budget_limit

    def check_budget(self):
        if self.user.expense > self.budget_limit:
            print(
                f"Warning: You have exceeded your budget of ${self.budget_limit}!")
        else:
            print(f"You are within your budget of ${self.budget_limit}.")


def generate_monthly_report(user):
    with open(f'{user.name}_monthly_report.csv', 'w', newline='')as file:
        writer = csv.writer(file)
        writer.writerow(['Type', 'Amount', 'Category'])
        for transaction in user.transactions:
            writer.writerow(
                [transaction['type'], transaction['amount'], transaction.get('category', 'N/A')])
    print("Monthly report generated.")


def main():
    # Initialize the user
    print("Welcome to Personal Finance Manager")
    name = input("Please enter your name: ")
    user = User(name)

    # Load previous transactions
    load_choice = input(
        "Do you want to load your previous transactions? (y/n): ").lower()
    if load_choice == 'y':
        load_transactions(user)

    while True:
        print("\nMain Menu:")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Balance")
        print("4. Generate Spending Report")
        print("5. Save Transactions")
        print("6. Load Transactions")
        print("7. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            amount = float(input("Enter income amount: "))
            user.add_income(amount)

        elif choice == '2':
            amount = float(input("Enter expense amount: "))
            category = input(
                "Enter expense category (e.g., food, rent, entertainment): ")
            user.add_expense(amount, category)

        elif choice == '3':
            print(user.view_balance())

        elif choice == '4':
            print("Generating spending report...")
            generate_spending_report(user)

        elif choice == '5':
            save_transactions(user)

        elif choice == '6':
            load_transactions(user)

        elif choice == '7':
            print("Exiting Personal Finance Manager. Goodbye!")
            sys.exit()

        else:
            print("Invalid option, please choose a valid menu item.")


if __name__ == "__main__":
    main()
