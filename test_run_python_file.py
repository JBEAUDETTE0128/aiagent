from functions.run_python_file import run_python_file

# Prints calculator's usage instructions
print(run_python_file("calculator", "main.py"))

# Should run the calculator (Note: Poorly Rendered)
print(run_python_file("calculator", "main.py", ["3 + 5"]))

# Should run calculator's tests successfully
print(run_python_file("calculator", "tests.py"))

# Should return an error (Outside directory)
print(run_python_file("calculator", "../main.py"))

# Should return an error (Doesn't Exist)
print(run_python_file("calculator", "nonexistent.py"))

# Should return an error (Not a Python file)
print(run_python_file("calculator", "lorem.txt"))
