## Automate your Python testing

`gentests` is a command line utility which generates a pytest file in your tests/ folder.

It leverages the Chain framework to prompt gpt to create this pytest file using an exemplar (example_pytest.py).

### Usage

`python gentests.py <python_file.py>` -> generates test_python_file.txt in your tests/ directory.

You then edit the txt file to be proper python and save as a python file.

### Next steps
- iterate on quality of output
- validate output so you can directly generate python files (using Instructor module)