import os
import re

def find_files_with_locators(directory):
    files_with_locators = []
    extracted_locators=[]
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.robot'):
                file_path = os.path.join(root, file)

                with open(file_path, 'r') as f:
                    content = f.read()

                    # Check if the file contains a variable section
                    if '*** Variables ***' in content:
                        # Extract the variable section
                        variable_section = content.split('*** Variables ***', 1)[1]

                        # Use regular expression to find potential locators
                        locators = re.findall(r'\$\{.*?\}', variable_section)

                        # Check if any of the potential locators match the expected pattern
                        for locator in locators:
                            if re.match(r'\$\{\w+\}.*', locator):
                                extracted_locators.append(locator)
                                files_with_locators.append(file_path)
                                break

    return files_with_locators


# Specify the directory path to search for Robot Framework files
directory_path = './'

# Call the function to find files with locators
result = find_files_with_locators(directory_path)

# Print the files that contain locators
if result:
    print("Files with locators:")
    for file_path in result:
        print(file_path)
else:
    print("No files with locators found.")