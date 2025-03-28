import argparse
import os
import supportmodule as s
import sys

def main():
    parser = argparse.ArgumentParser(description='this script is used to help maintain user expenses')
    parser.add_argument("action", choices= [
        "add", "update", "view", "delete", "summarize", 
        "summarize_monthly", "add_category", "view_categories", 
        "set_budget", "export", "clear"], 
        help="main action to pick")
    parser.add_argument('--type', type=str, help="what the expense is, example: rent")
    parser.add_argument('--amount', type=float, help='currency amount of added expense')
    parser.add_argument('--category', type=str, help='existing category of added expense')
    parser.add_argument('--month', type=str, help='enter string month')
    parser.add_argument('--budget', type=float, help='limit for money to be spent per month')
    parser.add_argument('--export_path', type=str, help='location to export file to',)
    args = parser.parse_args()

    s.load_configuration()

    try:
        with open(s.CONFIG_FILE, 'r') as config:
            configuration = list(config)
            count = 0
            config_content = False
            buffer_file_name = ""
            buffer_file_path = ""
            buffer_category_name = ""
            buffer_currency = ""
            buffer_budget = ""
            for con in configuration:
                con = list(con)
                for c in con:
                    if config_content and c != '\n':
                        if count == 0:
                            buffer_file_name += c
                        elif count == 1 and c != '\n':
                            buffer_file_path += c
                        elif count == 2 and c != '\n':
                            buffer_category_name += c
                        elif count == 3 and c != '\n':
                            buffer_currency += c
                        elif count == 4 and c != '\n':
                            buffer_budget += c
                    if c == '=':
                        config_content = True
                count += 1
                config_content = False
        
        s.file_name = buffer_file_name
        s.file_path = buffer_file_path
        s.category_name = buffer_category_name
        s.currency = buffer_currency
        s.leftover_budget = buffer_budget

    except FileNotFoundError:
        s.file_name = input("Enter file name (e.g., expenses.csv): ")
        s.update_configuration("file name", s.file_name)
        
        s.file_path = input("Enter current file path (e.g., C:/Users/Default/): ")
        s.update_configuration("file path", s.file_path)
        
        s.category_name = input("Enter categories file name (e.g., categories.txt): ")
        s.update_configuration("category name", s.category_name)
        
        currency_check = False
        while not currency_check:
            s.currency = input("Enter valid currency (e.g. USD)")
            if s.currency not in s.valid_currencies:
                print(f"Invalid currency: {buffer_currency}. Please use a valid ISO 4217 code.")
                print(f"valid currencies include: {s.valid_currencies}")
            else:
                s.update_configuration("currency", s.currency)
                currency_check = True
        
        s.update_configuration("budget", "NULL")


    if args.action == "add":
        if not args.type or not args.amount or not args.category:
            sys.exit("please enter proper format when using the add argument\nexample case: [py main.py add --type rent --amount 1500 --category home]")
        
        s.add_expense(args.type, args.amount, args.category)
    
    elif args.action == "update":
        if not args.type:
            sys.exit("please enter proper format when using update argument\nexample case: [py main.py update --type rent")
        
        s.update_expense(args.type)
    
    elif args.action == "delete":
        if not args.type:
            sys.exit("please enter proper format when using delete argument\nexample case: [py ExpenseTracker.py delete --type rent]")

        s.delete_expense(args.type)
    
    elif args.action == "view":
        s.view_expenses()
    
    elif args.action == "summarize":
        s.summarize_total_expenses()
    
    elif args.action == "summarize_monthly":
        if not args.month:
            sys.exit("please enter proper format when using summarize_monthly argument\nexample case: [py main.py summarize_monthly --month February]")
        
        s.summarize_monthly_expenses(args.month)
    
    elif args.action == "add_category":
        if not args.category:
            sys.exit("please enter proper format when using add_category argument\nexample case: [py main.py add_category --category groceries]")

        s.add_category(args.category)
    
    elif args.action == "view_categories":
        s.view_categories()
    
    elif args.action == "set_budget": 
        if not args.budget:
            sys.exit("please enter proper format when using set_budget argument\nexample case: [py main.py set_budget --budget 1500]")
        
        s.set_budget(args.budget)
    
    elif args.action == "export":
        if not args.export_path:
            sys.exit('"please enter proper format when using export argument\nexample case: [py main.py export --export_path "C:path\\to\\export\\location" (for Windows systems, apply file paths in accordance with your OS system)')
            
        s.export_file(s.file_path, args.export_path)

    elif args.action == "clear":
        confirmation = input("are you sure you want to clear all expenses, they will not be recoverable[Y/N]")
        
        if confirmation.upper() == 'Y':
            print('clearing expenses...')
            s.clear_expenses()
        elif confirmation.upper() == 'N':
            print('cancelling...')
            sys.exit()
        else:
            print("please enter the proper input[Y/N]")
            sys.exit()
    
    else:
        print("please enter the proper command line arguments")
        
if __name__ == '__main__':
    main()