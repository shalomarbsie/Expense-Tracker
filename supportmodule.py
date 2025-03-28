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

valid_currencies = ["USD", "EUR", "JPY", "GBP", "AUD", "CAD", "CHF", "CNY"] 
CONFIG_FILE = "config.txt"
file_name = None
file_path = None
category_name = None
currency = None
leftover_budget = None
current_datetime = datetime.now()
current_year = current_datetime.year
current_month = current_datetime.month
timestamp = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

def load_configuration():
    global file_name, file_path, category_name, currency
    if not os.path.exists(CONFIG_FILE):
        return

    with open(CONFIG_FILE, 'r') as config:
        for line in config:
            key, value = line.strip().split("=")
            if key == "file_name":
                file_name = value
            elif key == "file_path":
                file_path = value
            elif key == "category_name":
                category_name = value
            elif key == "currency":
                currency = value

def save_configuration():
    with open(CONFIG_FILE, 'w') as config:
        if file_name:
            config.write(f"file_name={file_name}\n")
        if file_path:
            config.write(f"file_path={file_path}\n")
        if category_name:
            config.write(f"category_name={category_name}\n")
        if currency:
            config.write(f"currency={currency}\n")
        if leftover_budget:
            config.write(f"leftover_budget={leftover_budget}")

def update_configuration(key, value):
    global file_path, file_name, category_name, currency, leftover_budget

    if key == "file name":
        file_name = value
    elif key == "file path":
        file_path = value
    elif key == "category name":
        category_name = value
    elif key == "currency":
        currency = value
    elif key == "budget":
        leftover_budget = value

    save_configuration()
    expense_headline = [
        ["ID", "Expense Type", "Expense Amount", "Date and Time", "Category"]
    ]   
    with open(file_name, "w", newline='') as expenses:
        writer = csv.writer(expenses)
        writer.writerows(expense_headline)


def add_expense(expense_type, expense_amount, expense_category):
    global file_name
    file_exists = False
    while not file_exists:
        try:
            with open(file_name, 'r', newline='') as expenses:
                reader = csv.reader(expenses)
                rows = list(reader)
            file_exists = True
        except FileNotFoundError:
            file_name = input("enter file name: ")
            
    repeat_checker = False
    for row in rows:
        if row[1] == expense_type and not repeat_checker:
            while not repeat_checker:
                choice = input(f"expense /{expense_type}/ already exists, do you wish to add expense again?(y/n)")
                if choice.lower() == "n":
                    sys.exit()
                elif choice.lower() == "y":
                    repeat_checker = True
                else:
                    print("please enter proper input")

    if rows[-1][0] == "ID":
        expense_number = 1
    else:
        buffer = int(rows[-1][0])
        expense_number = buffer + 1
        rows[-1][0] = str(expense_number)
    
    category_exists = False
    with open(category_name, 'r') as categories:
        for category in categories:
            if category.strip() == expense_category:
                category_exists = True
    
        if not category_exists:
            print("please enter existing category")
            sys.exit()

    rows.append([expense_number, expense_type, expense_amount, timestamp, expense_category])
    with open(file_name, "a", newline='') as expenses:
        writer = csv.writer(expenses)
        writer.writerow(rows[-1])

def update_expense(expense_type):
    global file_name
    float_bool = False
    category_bool = False
    found = False
    with open(file_name, 'r', newline='') as expenses:
        reader = csv.reader(expenses)
        rows = list(reader)

    for row in rows:
        if row[1] == expense_type:
            updated_expense = input("enter new expense: ")
            
            while not float_bool:
                updated_amount = input("enter new amount: ")
                try:
                    updated_amount = float(updated_amount)
                    float_bool = True
                except ValueError:
                    print("please enter a valid amount\n")      
            
            while not category_bool:
                with open(category_name, 'r') as categories:
                    updated_category = input("enter new existing category: ") 
                    if updated_category not in [cat.strip() for cat in categories]:
                        print("please enter existing category")
                    else:
                        category_bool = True
                      
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
    if expense_type == "Expense Type":
        sys.exit("please don't attempt to delete the header")

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
    if not expense_deleted:
        print("expense not found")
        return 

    with open(file_name, 'w', newline='') as expenses:
        writer = csv.writer(expenses)
        writer.writerows(new_rows)

def view_expenses():
    with open(file_name, 'r') as expenses:
        reader = csv.reader(expenses)
        rows = list(reader)
    
    for row in rows:
        if row[0] == 'ID':
            pass
        else:
            print(row)

def summarize_total_expenses():
    total_expenses = 0
    with open(file_name, 'r') as expenses:
        reader = csv.reader(expenses)
        rows = list(reader)

    for row in rows:
        if row[2] not in rows[0]:
            expense_amount = float(row[2])
            total_expenses += expense_amount
    
    print(f"total expenses: {total_expenses}")

def summarize_monthly_expenses(month):    
    int_month = month_to_int.get(month.lower(), None)
    if int_month is None:
        print(f"Invalid month: {month}")
        sys.exit()

    monthly_expense = 0
    with open(file_name, 'r') as expenses:
        reader = csv.reader(expenses)
        rows = list(reader)
    
    for row in rows:
        if row[0] == "ID":
            pass
        else:
            if row[3] not in row[0]:
                timestamp_dt = datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S")
                if timestamp_dt.year == current_year:
                    if timestamp_dt.month == int_month:
                        monthly_expense += float(row[2])

    print(f"your total expenditure for {month} is currently {monthly_expense}")
    return monthly_expense

def add_category(expense_category):
    with open(category_name, 'a+') as categories:
        for category in categories:
            if category.strip() == expense_category.strip():
                print(f"category /{expense_category}/ already exists, please enter another category")
                return
        
        categories.write(expense_category + "\n")

def view_categories():
    with open(category_name, 'r') as categories:
        for category in categories:
            stripped_category = category.rstrip('\n')
            print(stripped_category)
    
def set_budget(budget):
    global currency, leftover_budget
    with open(CONFIG_FILE, 'r+') as configuration:
        config = list(configuration)
        if config[4] == "leftover_budget=NULL":
            pass
        else:
            choice = input("you have already set a budget, do you wish to change it?[Y/N]")
            if choice.upper() == "Y":
                configuration.seek(0)
                configuration.truncate()
                for con in config:
                    if con != config[4]:
                        configuration.write(con)
            else:
                sys.exit()
    
    try:
        budget = int(budget)
    except ValueError:
        print("please enter appropriate budget")
        sys.exit()

    if budget <= 0:
        print("budget must be a positive amount")
        sys.exit()

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
    
    with open(CONFIG_FILE, 'r+') as config:
        configuration = list(config)
        config.seek(0)
        config.truncate()
        for con in configuration:
            if con != 'leftover_budget=NULL':
                config.write(con)
        config.write(f"leftover_budget={leftover_budget}")
 
def export_file(old_path, new_path):
    shutil.copy(old_path, new_path)
    print(f"{old_path} exported to {new_path}")

def clear_expenses():
    try:
        os.remove(file_path)
        print(f"File '{file_name}' has been deleted.")
    except FileNotFoundError:
        print(f"The file '{file_name}' does not exist.")
    except PermissionError:
        print(f"Permission denied to delete the file '{file_name}'.")
    except Exception as e:
        print(f"Error deleting file: {e}")
