from functions.get_file_content import get_file_content
from config import MAX_CHARS

# Test One: calculator, lorem.txt
return_string = get_file_content("calculator", "lorem.txt")
length_check = len(return_string)
print(f'Length of Returned String: {length_check}')
if length_check > MAX_CHARS:
    print(return_string[MAX_CHARS:])

# Test Two: calculator, main.py
print(get_file_content("calculator", "main.py"))

# Test Three: calculator, pkg/calculator.py
print(get_file_content("calculator", "pkg/calculator.py"))

# Test Four: calculator, /bin/cat (Return Error)
print(get_file_content("calculator", "/bin/cat"))

# Test Five: calculator, pkg/does_not_exist.py (Return Error)
print(get_file_content("calculator", "pkg/does_not_exist.py"))