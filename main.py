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
    #             email= "webofscience@wos.com",
    #             name= "web of science",
    #             short_name="wos",
    #             department_name="web of science",
    #             department_short_name="wos",
    #             status="new",
    #             client_data_sheet_link="",
    #             department_subscribed=0,
    #             applicant_subscribed=0,
    #             peer_subscribed=0,
    #             journal_subscribed=1,
    #             department_data_last_update="",
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
    client_id= 2
    manual_update(client_id)




# import json

# def get_field_names(json_file_path):
#     with open(json_file_path, 'r', encoding='utf-16') as file:
#         data = json.load(file)
#     return data['matched_publications'][0].keys()
# json_file_path = "journal template.json"
# field_names = get_field_names(json_file_path)
# print(field_names)



# ----------

if __name__ == '__main__':
    main()