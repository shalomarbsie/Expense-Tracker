# Expense-Tracker
- PROPERTY OF: Shalom Arbsie Gugsa

- Basic Overview: this is a command line program that helps keep track of your expenses
- some features include:
    a. expense management
    b. budget management
    c. currency options
    d. categorization of expenses
    e. exporting of expenses into a CSV(excel) file
 
- Known issues: setting up your expense file, configuration file, categories files, etc. multiple times can lead to errors in processing them by the code, here is their general format:

configuration file(txt file):

file_name=expenses.csv
file_path=C\\path\\to\\the\\directory\\you're\\running\\this\\program\\in\\expenses.csv (remember to apply file paths in according with your OS system)
category_name=categories.txt
currency=USD
leftover_budget=5000 (leftover_budget=NULL if you haven't set a budget yet)

expenses file(csv file):

ID,Expense Type, Expense Amount,Date and Time, Category
1,rent,1500.0,2025-03-28 16:20:46,home
...

categories file(txt.file):

home
food
entertainment
...

- instructions to run: this program runs on command line arguments which have specifications in the main.py file
