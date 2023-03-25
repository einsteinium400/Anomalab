import importlib
import os
import ast
#import astor
import inspect
import re
#import ..distanceFunctions.DistanceFunctions
## Get locations
# get the absolute path of the current working directory
current_dir = os.path.abspath(os.getcwd())
# get the absolute path of the 'distancefunctions' directory
distancefunctions_dir = os.path.join(current_dir, 'distancefunctions')
distancefunctions_abs_path = os.path.abspath(distancefunctions_dir)
distancefunctions_file = os.path.join(distancefunctions_abs_path, 'DistanceFunctions.py')

print (f'distancefunctions_abs_path is: {distancefunctions_abs_path}')
print (f'distancefunctions_file is: {distancefunctions_file}')

DISTANCE_FUNCTIONS_PATH = distancefunctions_file
function_list = []
# DISTANCE_FUNCTIONS_PATH = "../distanceFunctions/DistanceFunctions.py"


def load_user_distance_functions(content):
    # Initialize a list to hold the AST nodes for the function definitions
    with open(DISTANCE_FUNCTIONS_PATH, 'a') as target_file:
        # Write the string to the target file
       target_file.write(content)

    # Define a regular expression pattern to match function definitions
    pattern = re.compile(r'^\s*def\s+(\w+)\s*\(', re.MULTILINE)

    # Search the source code for the function definition
    match = pattern.search(content)

    if match:
        function_name = match.group(1)
        print(function_name)  # Outputs function name
    else:
        print("Function not found in file.")

    refresh_functions_list()

    return function_name
#    refresh_functions_list()




    # function_nodes = []

    # # Iterate over all Python files in the directory
    # for root, dirs, files in os.walk(source_dir):
    #     for file in files:
    #         if file.endswith(".py"):
    #             # Get the full path of the file
    #             file_path = os.path.join(root, file)

    #             # Open the file and extract the function definitions
    #             with open(file_path, "r") as f:
    #                 source = f.read()
    #                 module = ast.parse(source)
    #                 for node in module.body:
    #                     #if isinstance(node, ast.FunctionDef):
    #                     if isinstance(node, ast.FunctionDef):
    #                         function_nodes.append(node)

    # # Write the AST nodes to a new file
    # with open(DISTANCE_FUNCTIONS_PATH, "a") as outfile:
    #     outfile.write(astor.to_source(ast.Module(body=function_nodes)))

    # # refresh distance function module
    # importlib.reload(Moudles.Functions.DistanceFunctions)
    # print (function_list)

    # todo: update in mongoDB

# # Define the source and destination file paths
# source_file = 'subtraction.py'
# dest_file = 'dest.py'


# filename = 'dest.py'
# function_name = 'subtraction'

#def delete_user_function(function_name):

    #function_name=get_function_name(function_index)
    #
    #
    # # Load the module dynamically and get the source code for the function
    # module = __import__(os.path.splitext(DISTANCE_FUNCTIONS_PATH)[0])
    # function_source = inspect.getsource(getattr(module, function_name))
    #
    # # Open the file in read mode to read its contents
    # with open(DISTANCE_FUNCTIONS_PATH, 'r') as f:
    #     lines = f.readlines()
    #
    # # Open the file in write mode to modify its contents
    # with open(DISTANCE_FUNCTIONS_PATH, 'w') as f:
    #     i = 0
    #     while i < len(lines):
    #         # Check if the current line defines the function to be deleted
    #         if lines[i].startswith('def ' + function_name):
    #             # Remove all lines that define the function
    #             while i < len(lines) and (lines[i].startswith('def ') or lines[i].startswith(' ')):
    #                 i += 1
    #         else:
    #             # Write the line to the modified file
    #             f.write(lines[i])
    #             i += 1
    #
    # # refresh distance function module
    # importlib.reload(DISTANCE_FUNCTIONS_PATH)
    # refresh_functions_list()


def refresh_functions_list():
    # Load the module as a spec
    global function_list
    spec = importlib.util.spec_from_file_location(".", DISTANCE_FUNCTIONS_PATH)

    # Load the module from the spec
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Get a list of all functions defined in the module, as tuples of (name, function)
    function_list = [(name, obj) for name, obj in inspect.getmembers(module, inspect.isfunction)]

    # Print the list of function tuples
    print(function_list)


def view_all_user_functions():
    for i in range(len(function_list)):
        print(i, "-", function_list[i][0])


def get_function_reference(index):
    return function_list[index][1]

def get_function_name(index):
    return function_list[index][0]
# refresh_functions_list()

def get_function_by_name(name):
    for tpl in function_list:
        if tpl[0] == name:
            return tpl[1]