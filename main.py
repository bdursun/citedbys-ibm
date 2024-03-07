# main.py
from orchestrator.orchestrator import *
import datetime


def main():
    print("CitedBys!")


# ------------------------------------#
    # VARIABLES
    # client_id= 0


# ------------------------------------#
    # CREATE A NEW CLIENT

    # create a new client
    # email and name required!!!
    # Orchestrator.create_client(
    #             email= "dohauni@uni.com",
    #             name= "doha university",
    #             short_name="du",
    #             department_name="finance",
    #             department_short_name="duf",
    #             status="new",
    #             client_data_sheet_link="",
    #             department_subscribed=1,
    #             applicant_subscribed=0,
    #             peer_subscribed=1,
    #             journal_subscribed=0,
    #             department_data_last_update=None,
    #             journal_data_last_update=None,
    #             data_update_period="monthly")

# ------------------------------------#
    # GET CLIENT INFORMATION

    # get client's info with id
    # client = Orchestrator.get_info_client(2)
    # for column in ClientInformation.__table__.columns:
    #     print(f'{column.name}: {getattr(client, column.name)}')

    # get all clients info and print
    # clients = Orchestrator.get_all_info_client()
    # for client in clients:
    #     for column in ClientInformation.__table__.columns:
    #         print(f'{column.name}: {getattr(client, column.name)}')

# ------------------------------------#
    # UPDATE CLIENT INFORMATION

    # change client information on database, all args is required

    # Orchestrator.update_client_information(2, 'column', new_value)

# ------------------------------------#

    # REMOVE FROM CITEDBYS.DB

    # tablename= ""

    # remove client with id
    # Orchestrator.remove_one_client(client_id)

    # Orchestrator.remove_all_client()

# ------------------------------------#

    # DAILY UPDATE

    # Orchestrator.daily_update()
# ------------------------------------#

    # Manual Update with Client ID
    # client_id= 2
    # Orchestrator.manual_update(client_id)
# ------------------------------------#


if __name__ == '__main__':
    main()
