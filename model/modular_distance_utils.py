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







def refresh_functions_list():
    # Load the module as a spec
    global function_list
    spec = importlib.util.spec_from_file_location(".", DISTANCE_FUNCTIONS_PATH)

    # Load the module from the spec
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Get a list of all functions defined in the module, as tuples of (name, function)
    function_list = [(name, obj) for name, obj in inspect.getmembers(module, inspect.isfunction)]




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