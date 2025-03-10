import argparse
import sys
import os
import csv
import datetime


file_path = "C:\\Users\\Shalom Arbsie\\projects\\personal\\Expense-Tracker\\expenses.csv"
file_name = "expenses.csv"
current_datetime = datetime.datetime.now()
timestamp = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

if not os.path.exists(file_path):
    expense_headline = [
        ["Expense Number", "Expense Type", "Expense Amount", "Date and Time"]
    ]   
    with open(file_name, "w", newline='') as expenses:
        writer = csv.writer(expenses)
        writer.writerows(expense_headline)
        
def add_expense(expense_type, expense_amount):
    with open(file_name, 'r', newline='') as expenses:
        reader = csv.reader(expenses)
        rows = list(reader)
    
    repeat_checker = False
    for row in rows:
        if row[1] == expense_type and not repeat_checker:
            choice = input(f"expense /{expense_type}/ already exists, do you wish to add expense again?(y/n)")
            if choice == "n" or choice == "N":
                sys.exit()
            elif choice == "y" or choice == "Y":
               repeat_checker = True
               break

    if rows[-1][0] == "Expense Number":
        expense_number = 1
    else:
        buffer = int(rows[-1][0])
        expense_number = buffer + 1
        rows[-1][0] = str(expense_number)

    rows.append([expense_number, expense_type, expense_amount, timestamp])
    with open(file_name, "a", newline='') as expenses:
        writer = csv.writer(expenses)
        writer.writerow(rows[-1])

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
    
    with open(file_name, 'w', newline='') as expenses:
        writer = csv.writer(expenses)
        writer.writerows(rows)

def delete_expense(expense_type):
    expense_deleted = False
    with open(file_name, 'r', newline='') as expenses:
        reader = csv.reader(expenses)
        rows = list(reader)
    
    new_rows = []
    for row in rows:
        if expense_deleted is True:
            expense_number = int(row[0])
            expense_number -= 1
            row[0] = str(expense_number)
        
        if row[1] == expense_type and not expense_deleted:
            expense_deleted = True
        else:
            new_rows.append(row)
    
    with open(file_name, 'w', newline='') as expenses:
        writer = csv.writer(expenses)
        writer.writerows(new_rows)

def view_expenses():
    with open(file_name, 'r') as expenses:
        reader = csv.reader(expenses)
        rows = list(reader)
    
    for row in rows:
        print(row)

def summarize_expenses():
    total_expenses = 0
    with open(file_name, 'r') as expenses:
        reader = csv.reader(expenses)
        rows = list(reader)

    for row in rows:
        if row[2] != 'Expense Amount':
            expense_amount = int(row[2])
            total_expenses += expense_amount
    
    print(f"total expenses: {total_expenses}")

add_expense('dog food', 200)
add_expense('rent', 1500)
add_expense('groceries', 700)
summarize_expenses()