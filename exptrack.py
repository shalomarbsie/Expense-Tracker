import shutil
import sys
import os
import csv
from datetime import datetime

month_to_int = {
        'january': 1,
        'february': 2,
        'march': 3,
        'april': 4,
        'may': 5,
        'june': 6,
        'july': 7,
        'august': 8,
        'september': 9,
        'october': 10,
        'november': 11,
        'december': 12
    }

currency = None
file_path = "path\\to\\your\\current\\or\\source\\directory\\expenses.csv"
destination_path = "path\\to\\your\\export\\destination\\directory\\expensescopy.csv"
file_name = "expenses.csv"
current_datetime = datetime.now()
current_year = current_datetime.year
current_month = current_datetime.month
timestamp = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

if not os.path.isfile(file_path):
    expense_headline = [
        ["Expense Number", "Expense Type", "Expense Amount", "Date and Time", "Category"]
    ]   
    with open(file_name, "w", newline='') as expenses:
        writer = csv.writer(expenses)
        writer.writerows(expense_headline)
        
def add_expense(expense_type, expense_amount, expense_category):
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

    rows.append([expense_number, expense_type, expense_amount, timestamp, expense_category])
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
            updated_category = input("enter new category: ")
            row[1] = updated_expense
            row[2] = updated_amount
            row[4] = updated_category
            row[3] = timestamp
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

def summarize_total_expenses():
    total_expenses = 0
    with open(file_name, 'r') as expenses:
        reader = csv.reader(expenses)
        rows = list(reader)

    for row in rows:
        if row[2] != 'Expense Amount':
            expense_amount = int(row[2])
            total_expenses += expense_amount
    
    print(f"total expenses: {total_expenses}")

def summarize_monthly_expenses(month):    
    int_month = month_to_int.get(month.lower(), None)
    if int_month is None:
        print(f"Invalid month: {month}")
        return

    monthly_expense = 0
    with open(file_name, 'r') as expenses:
        reader = csv.reader(expenses)
        rows = list(reader)
    
    for row in rows:
        if row[3] != "Date and Time":
            timestamp_dt = datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S")
            if timestamp_dt.year == current_year:
                if timestamp_dt.month == int_month:
                    monthly_expense += int(row[2])

    return monthly_expense

def add_category(expense_category):
    with open('category.txt', 'a+') as categories:
        for category in categories:
            if category == expense_category:
                print(f"category /{expense_category}/ already exists, please enter another category")
        
        categories.write(expense_category)

def view_categories(expense_category):
    with open(file_name, 'r') as expenses:
        reader = csv.reader(expenses)
        rows = list(reader)

    for row in rows:
        if row[4] == expense_category:
            print(row)
    
def set_budget(budget):
    for key, val in month_to_int.items():
        if val == current_month:
            string_month = key
    
    monthly_expense = summarize_monthly_expenses(string_month)
    leftover_budget = budget - monthly_expense
    if leftover_budget < 0:
        print(f"Warning! you have surpassed your budget by {-leftover_budget} {currency}'s for {string_month}: budget leftover = {leftover_budget}")
    elif leftover_budget < 100:
        print(f"Warning! you have less than 100 {currency}'s left for {string_month}: budget leftover = {leftover_budget}")
    elif leftover_budget < 250:
        print(f"Warning! you have less than 250 {currency}'s left for {string_month}: budget leftover = {leftover_budget}")
    elif leftover_budget < 500:
        print(f"Warning! you have less then 500 {currency}'s left for {string_month}: budget leftover = {leftover_budget}")
    
    print
 
def export_file():
    shutil.copy(file_path, destination_path)
    print(f"{file_name} exported to {destination_path}")

def clear_expenses():
    try:
        os.remove(file_name)
        print(f"File '{file_name}' has been deleted.")
    except FileNotFoundError:
        print(f"The file '{file_name}' does not exist.")
    except PermissionError:
        print(f"Permission denied to delete the file '{file_name}'.")
    except Exception as e:
        print(f"Error deleting file: {e}")