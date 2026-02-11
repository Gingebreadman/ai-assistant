from functions.get_file_content import get_file_content
from config import MAX_CHARS

def print_result(title, result):
    print(title)
    print(f"Length: {len(result)}")
    print("Ending snippet:")
    print(result[-200:])  # show last 200 chars so we can see truncation message
    print()

if __name__ == "__main__":
    # 1. Large lorem file (should truncate)
    lorem = get_file_content("calculator", "lorem.txt")
    print_result("Result for lorem.txt:", lorem)

    # 2. Normal files
    print("Result for main.py:")
    print(get_file_content("calculator", "main.py"))
    print()

    print("Result for pkg/calculator.py:")
    print(get_file_content("calculator", "pkg/calculator.py"))
    print()

    # 3. Outside working directory
    print("Result for /bin/cat:")
    print(get_file_content("calculator", "/bin/cat"))
    print()

    # 4. Nonexistent file
    print("Result for pkg/does_not_exist.py:")
    print(get_file_content("calculator", "pkg/does_not_exist.py"))
    print()
