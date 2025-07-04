from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
import os

def main():
    print(get_file_content("calculator", "main.py"))
    print(get_file_content("calculator", "pkg/calculator.py"))
    print(get_file_content("calculator", "/bin/cat"))









if __name__ == "__main__":
    main()