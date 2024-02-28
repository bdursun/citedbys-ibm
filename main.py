# main.py
from orchestrator.orchestrator import *


def main():
    print("CitedBys!")



#------------------------------------#
    #VARIABLES
    #client_id= 0



#------------------------------------#
    #CREATE A NEW CLIENT

    ##create a new client
    # email and name required!!!
    # create_client(
    #             email= "DOHA@gmail.com",
    #             name= "DOHA",
    #             short_name="DH",
    #             department_name="Business School",
    #             department_short_name="BS",
    #             status="new",
    #             client_data_sheet_link="",
    #             department_subscribed=1,
    #             applicant_subscribed=0,
    #             journal_subscribed=0,
    #             department_data_last_update="",
    #             applicant_data_last_update="",
    #             journal_data_last_update="",
    #             data_update_period="monthly")

#------------------------------------#
    #GET CLIENT INFORMATION

    ##get client's info with id
    # get_info_client(client_id)


    ##get all clients info
    # get_all_info_client()
#------------------------------------#
    #UPDATE CLIENT INFORMATION

    ##change client information on database, all args is required

    # update_client_information(client_id, column, new_value)

#------------------------------------#

    #REMOVE FROM CITEDBYS.DB

    #tablename= ""

    ##remove client with id
    #remove_client(client_id)

    ##remove everyone from table
    #remove_client(tablename)

    ##remove table
    #remove_client(tablename)
#------------------------------------#

    #DAILY UPDATE

    # daily_update()
#------------------------------------#

    #Manual Update with Client ID
    client_id= 6
    manual_update(client_id)




# import json

# def get_field_names(json_file_path):
#     with open(json_file_path, 'r', encoding='utf-16') as file:
#         data = json.load(file)
#     return data['person']['publications']
# json_file_path = "output_test.json"
# field_names = get_field_names(json_file_path)
# for field_names2 in field_names:
#     for key,values in field_names2.items():
#         print(key," :  ",values)
#         print('\n')
#     print("-------------------------")



# ----------



# def get_field_names(json_data):
#     field_names = []

#     # Recursive function to traverse nested JSON structure
#     def traverse(data, prefix=''):
#         if isinstance(data, dict):
#             for key, value in data.items():
#                 new_prefix = f"{prefix}.{key}" if prefix else key
#                 traverse(value, new_prefix)
#         elif isinstance(data, list):
#             for i, item in enumerate(data):
#                 new_prefix = f"{prefix}[{i}]" if prefix else f"[{i}]"
#                 traverse(item, new_prefix)
#         else:
#             field_names.append(prefix)

#     traverse(json_data)
#     return field_names

# json_file_path = "output_test.json" 

# with open(json_file_path, 'r',encoding='utf-16') as file:
#     json_data = json.load(file)

# field_names = get_field_names(json_data)
# print(field_names)
if __name__ == '__main__':
    main()