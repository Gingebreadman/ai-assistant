from functions.get_files_info import get_files_info

def print_result(title, result):
    print(title)
    for line in result.split("\n"):
        print("  " + line)
    print()

if __name__ == "__main__":
    # 1. Current directory inside calculator
    result1 = get_files_info("calculator", ".")
    print_result("Result for current directory:", result1)

    # 2. pkg directory
    result2 = get_files_info("calculator", "pkg")
    print_result("Result for 'pkg' directory:", result2)

    # 3. Attempt to escape working directory
    result3 = get_files_info("calculator", "/bin")
    print_result("Result for '/bin' directory:", result3)

    # 4. Attempt to escape via ..
    result4 = get_files_info("calculator", "../")
    print_result("Result for '../' directory:", result4)
