from matplotlib import pyplot as plt

from Moudles.Clustring.KMeanClusterer import KMeansClusterer
from Moudles.Functions.DistanceFunctions import *
from Moudles.Utils.utils import *
from modular_distance_utils import *
from Moudles.Clustring.Elbow import elbow_method

# name of labeled file name. label is last coloumn
LABLED_FILE_NAME = "dataset1/labeled_data.csv"

# max value for each feature by index
MIXED_DATA_MEAN_VALUES = [15, 4, 2, 2, 2, 2, 2, 2, 2, 4, 4, 3, 4, 4, 8, 3, 2, 2, 8, 4]

MIXED_DATA_TYPE_OF_FIELDS = [False, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
                             True, True,
                             True, True, True]

mixed_data = [numpy.array(f) for f in csv_to_nested_list("dataset1\labeled_data_numeric.csv")]


# # check elbow for mixed data
# k=elbow_method(mixed_distance,mixed_data,MIXED_DATA_MEAN_VALUES,MIXED_DATA_TYPE_OF_FIELDS)
#
# clusterer = KMeansClusterer(num_means=k, distance=mixed_distance, repeats=9, mean_values=MIXED_DATA_MEAN_VALUES,
#                             type_of_fields=MIXED_DATA_TYPE_OF_FIELDS)
# clusterer.cluster(mixed_data)
#
# clusterer.store_model("storage.json")
#


def action1():
    print("")
    load_user_distance_functions("user_functions_stage_area")
    print("functions load successfully")


def action2():
    print("")
    view_all_user_functions()


def action3():
    print("")
    view_all_user_functions()
    user_input = input("choose a number from above")
    delete_user_function(int(user_input))


def action4():
    print("")
    view_all_user_functions()
    user_input = input("choose a number from above")

    chosen_function = get_function_reference(int(user_input))

    k = elbow_method(chosen_function, mixed_data, MIXED_DATA_MEAN_VALUES, MIXED_DATA_TYPE_OF_FIELDS)

    clusterer = KMeansClusterer(num_means=k, distance=chosen_function, repeats=9, mean_values=MIXED_DATA_MEAN_VALUES,
                                type_of_fields=MIXED_DATA_TYPE_OF_FIELDS)
    clusterer.cluster(mixed_data)

    clusterer.store_model("storage.json")


# Define a dictionary that maps user input to functions
actions = {
    '1': action1,
    '2': action2,
    '3': action3,
    '4': action4
}

refresh_functions_list()

while True:
    # Prompt the user for input
    print("")
    user_input = input(
        "for uploading a new function, press 1. \n for viewing all existing functions -2. \n for deleting a function "
        "- 3 \n for running model with chosen function - 4  ")

    if user_input == 'q':
        # Exit the loop if the user enters 'q'
        break

    # Look up the corresponding function based on user input
    action = actions.get(user_input)

    # Call the function, if it exists
    if action:
        action()
    else:
        print("Invalid input")
