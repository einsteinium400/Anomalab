import importlib
import inspect
import os
import os
import ast
import astor
import inspect
import os
import ast
import astor
import inspect

functions_list = []


def add_all_user_functions(source_file, dest_file):
    # Get a list of all the function names in the source file

    # with open(source_file, 'r') as f:
    #     source_code = f.read()

    functions = [name for name, obj in
                 inspect.getmembers(__import__(os.path.splitext(source_file)[0]), inspect.isfunction)]

    # Copy each function to the destination file
    with open(dest_file, 'a') as f:
        for function_name in functions:
            function_source = inspect.getsource(getattr(__import__(os.path.splitext(source_file)[0]), function_name))
            f.write(function_source)

    refresh_functions_list()
    # todo: refresh functions list


# # Define the source and destination file paths
# source_file = 'subtraction.py'
# dest_file = 'dest.py'


# filename = 'dest.py'
# function_name = 'subtraction'

def delete_user_function(filename, function_name):
    # Load the module dynamically and get the source code for the function
    module = __import__(os.path.splitext(filename)[0])
    function_source = inspect.getsource(getattr(module, function_name))

    # Open the file in read mode to read its contents
    with open(filename, 'r') as f:
        lines = f.readlines()

    # Open the file in write mode to modify its contents
    with open(filename, 'w') as f:
        i = 0
        while i < len(lines):
            # Check if the current line defines the function to be deleted
            if lines[i].startswith('def ' + function_name):
                # Remove all lines that define the function
                while i < len(lines) and (lines[i].startswith('def ') or lines[i].startswith(' ')):
                    i += 1
            else:
                # Write the line to the modified file
                f.write(lines[i])
                i += 1
    refresh_functions_list()
    # TODO: re_generate functions list


def refresh_functions_list():
    for module in os.listdir("user_function"):
        m = importlib.import_module(module.rstrip('.py'))
        # Get a list of all the names defined in the module
        module_names = dir(m)
        # Filter the names to get only the functions
        function_names = [name for name in module_names if callable(getattr(m, name))]

        # go through all of the functions of this specific module and add each one
        for f in function_names:
            func = getattr(m, f)
            functions_list.append((func, f))


def view_all_user_functions():
    for i in list(enumerate(functions_list)):
        print(i[0], "-", i[1])


def new_add_func(source_dir):

    # Initialize a list to hold the AST nodes for the function definitions
    function_nodes = []

    # Iterate over all Python files in the directory
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".py"):
                # Get the full path of the file
                file_path = os.path.join(root, file)

                # Open the file and extract the function definitions
                with open(file_path, "r") as f:
                    source = f.read()
                    module = ast.parse(source)
                    for node in module.body:
                        if isinstance(node, ast.FunctionDef):
                            function_nodes.append(node)

    # Write the AST nodes to a new file
    with open("functions.py", "a") as outfile:
        outfile.write(astor.to_source(ast.Module(body=function_nodes)))


# Define the path to the directory containing the Python files
source_dir = "user_function"
new_add_func(source_dir)