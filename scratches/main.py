import importlib
import os
import sys

# Add the path to the directory containing the modules to the system path
sys.path.insert(0, "user_function")
#
# # Load the modules containing the functions
# addition_module = importlib.import_module("addition")
# subtraction_module = importlib.import_module("subtraction")
#
# # Get the functions from the modules
# addition_function = getattr(addition_module, "addition")
# subtraction_function = getattr(subtraction_module, "subtraction")
#
# # Use the functions
# print(addition_function(2, 3))  # Output: 5
# print(subtraction_function(5, 3))  # Output: 2

functions_list = []

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

print(functions_list)

