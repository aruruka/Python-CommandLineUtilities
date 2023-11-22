import os
import sys

def find_files(files_to_find, starting_point):
    result = {}
    with open(files_to_find, 'r') as file:
        file_list = file.readlines()
    for file in file_list:
        file = file.strip()
        if file:
            file_path = os.path.join(starting_point, file)
            result[file] = "exist" if os.path.exists(file_path) else "not exist"
    return result

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python file_finder.py <file_list_path> <starting_point>")
        sys.exit(1)

    import argparse

    parser = argparse.ArgumentParser(description='Find files from a starting point.')
    parser.add_argument('files_to_find', type=str, help='Path to the file containing the list of files')
    parser.add_argument('starting_point', type=str, help='Starting point to search for files')
    args = parser.parse_args()

    result = find_files(args.files_to_find, args.starting_point)
    
    print("Result of existence of files:")
    for file_path, status in result.items():
        print(f"- {file_path} --> {status}")