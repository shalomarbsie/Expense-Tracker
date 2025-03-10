import os
file_name = 'expenses.csv'

try:
    os.remove(file_name)
    print(f"File '{file_name}' has been deleted.")
except FileNotFoundError:
    print(f"The file '{file_name}' does not exist.")
except PermissionError:
    print(f"Permission denied to delete the file '{file_name}'.")
except Exception as e:
    print(f"Error deleting file: {e}")