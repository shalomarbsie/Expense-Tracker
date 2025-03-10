import argparse
import os
import csv
import datetime

expense_data = [
    ["Expense Number", "Expense Type", "Expense Amount", "Date and Time"]
]

file_path = "C:\\Users\\Shalom Arbsie\\projects\\personal\\Expense-Tracker\\expenses.csv"
file_name = "expenses.csv"
current_datetime = datetime.datetime.now()
timestamp = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

if not os.path.exists(file_path):
    with open(file_name, "w", newline='') as expenses:
        writer = csv.writer(expenses)
        writer.writerows(expense_data)
        
def add_expense(expense_type, expense_amount):
    for expense in expense_data:
        if expense[1] == expense_type:
            choice = input("expense already exists, do you wish to add expense again?(y/n)")
            if choice == "n" or choice == "N":
                return
    
    if not isinstance(expense_data[-1][0], int):
        expense_number = 1
    else:
        expense_number = expense_data[-1][0] + 1
    
    expense_data.append([expense_number, expense_type, expense_amount, timestamp])
    with open(file_name, "a") as expenses:
        writer = csv.writer(expenses)
        writer.writerow(expense_data[-1])
        for expense in expense_data:
            print(expense)

def update_expense(expense_type):
    found = False
    with open(file_name, 'r', newline='') as expenses:
        reader = csv.reader(expenses)
        rows = list(reader)

    for row in rows:
        if row[1] == expense_type:
            updated_expense = input("enter new expense: ")
            updated_amount = input("enter new amount: ")
            row[1] = updated_expense
            row[2] = updated_amount
            found = True
            break
   
    if not found:
        print("expense type not found")
        return
    
    with open(file_name, 'w') as expenses:
        writer = csv.writer(expenses)
        writer.writerows(rows)








        