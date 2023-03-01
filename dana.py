import distance_functions_controller

controller = distance_functions_controller.Distance_Functions_Controller()

path = "user_functions_stage_area/mixed_distance.py"
controller.add_function(file_dir=path, name="mixed distance")

# import base64
# with open("main.py", 'r') as source_file:
#     contents = source_file.read()
#
# encoded_string = base64.b64encode(contents.encode('utf-8'))
# print(encoded_string)
# decoded_string = base64.b64decode(encoded_string).decode('utf-8')
# print(decoded_string)
# #
# message_bytes = contents.encode('ascii')
# base64_bytes_function = base64.b64encode(message_bytes)
#
# decoded_data=base64.decode(base64_bytes_function, "ascii")
# print(decoded_data)
#
