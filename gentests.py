"""
Command line utility which takes a python file as input and generates a pytest test file.

`gentests example_script.py` -> generates `tests/test_example_script.txt`

You then can edit the file and save as pytests file.
"""

from Chain import Chain, Prompt, Model  # import the Chain class
import argparse                         # so we can parse command line arguments
import os                               # so we can mkdir

system_prompt = """
You are a new SDET (Software Development Engineer in Test) who has joined my team.
You are skilled both in software development and software testing, and are really good at writing test cases.
You are an expert in Python programming, in particular the Pytest framework.

You will be pair programming with a developer who is writing python scripts, and your job will be to write
test cases for the scripts with maximum code coverage.

For every script you are given, you need to generate the corresponding pytest file with a test function for each
function defined in the script.

Here is an example pytest file that you can use as a model for future pytest files:
=================================================================
{{ example_pytest_file }}
=================================================================
""".strip()

pytest_prompt = """
The developer you are working with has written a python script that needs to be tested.

Here is the script:

=================================================================
{{ script }}
=================================================================

Please generate the pytest file that will test this script.
""".strip()

if __name__ == "__main__":
    # Parse the command line arguments
    parser = argparse.ArgumentParser(description='Generate pytest test files from python scripts.')
    parser.add_argument('script', type=str, nargs="?", help='The python script that needs to be tested.')
    args = parser.parse_args()
    print(args.script)
    if args.script is None:
        print("Please provide a python script to test.")
        exit(1)
    else:
        try:
            with open(args.script, 'r') as f:
                script = f.read()
        except FileNotFoundError:
            print(f"File not found: {args.script}")
            exit(1)
    # create a "tests/" folder if none exists
    try:
        os.mkdir('tests')
    except FileExistsError:
        pass
    # load our exemplar pytest file
    with open('/home/bianders/Brian_Code/gentests/example_pytest.py', 'r') as f:
        example_pytest = f.read()
    # Initialize our messages list with a system prompt
    messages = Chain.create_messages(Prompt(system_prompt), input = {'example_pytest_file': script})
    # build our chain
    prompt = Prompt(pytest_prompt)
    model = Model('gpt')
    chain = Chain(prompt, model)
    # run the chain
    r = chain.run(messages = messages, input = {'script': script})
    print(r.content)
    # write the output to a file in 'tests/' directory
    ## grab filename; remove the '.py' extension
    filename = args.script[:-3]
    with open(f'tests/test_{filename}.txt', 'w') as f:
        f.write(r.content)
