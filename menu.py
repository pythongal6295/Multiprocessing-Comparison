'''
Provides a basic frontend
'''
import sys
from datetime import date
from loguru import logger
import main
#import pysnooper
import socialnetwork_model as snm


logger.remove()
logger.add('log_' + str(date.today()) + '.log')

#@pysnooper.snoop()
def load_users():
    '''
    Loads user accounts from a file
    '''
    filename = input('Enter filename of user file: ')
    if not main.load_users(filename):
        print('An error occurred while trying to upload new users. Not all users may be loaded.')
    else:
        logger.info('Loaded the file.')
        print('The file has been loaded to the user database.')

def load_status_updates():
    '''
    Loads status updates from a file
    '''
    filename = input('Enter filename for status file: ')
    if not main.load_status_updates(filename):
        print('An error occurred while trying to upload new users. Not all statuses may be loaded.')
    else:
        print('The file has been loaded to the status database.')

def add_user():
    '''
    Adds a new user into the database
    '''
    user_id = input('User ID: ')
    email = input('User email: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')
    if not main.add_user(user_id, email, user_name, user_last_name, user_collection):
        print("An error occurred while trying to add new user")
    else:
        print("User was successfully added")

#@pysnooper.snoop()
def update_user():
    '''
    Updates information for an existing user
    '''
    user_id = input('User ID: ')
    email = input('User email: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')
    if not main.update_user(user_id, email, user_name, user_last_name, user_collection):
        print("An error occurred while trying to update user")
    else:
        print("User was successfully updated")

#@pysnooper.snoop()
def search_user():
    '''
    Searches a user in the database
    '''
    user_id = input('Enter user ID to search: ')
    result = main.search_user(user_id, user_collection)

    if not result:
        print("ERROR: User does not exist")
    else:
        print(f"User ID: {result['_id']}")
        print(f"Email: {result['email']}")
        print(f"Name: {result['user_name']}")
        print(f"Last name: {result['user_last_name']}")


def delete_user():
    '''
    Deletes user from the database
    '''
    user_id = input('User ID: ')
    if not main.delete_user(user_id, user_collection):
        print("ERROR: User does not exist")
    else:
        print("User was successfully deleted")
    
    for status in status_collection.database.find({'user_id': user_id}):
        status_id = status['_id']
        main.delete_status(status_id, status_collection)
    print('Associated statuses are deleted.')

def add_status():
    '''
    Adds a new status into the database
    '''
    status_id = input('Status ID: ')
    user_id = input('User ID: ')
    status_text = input('Status text: ')
    if not main.add_status(user_id, status_id, status_text, status_collection, user_collection):
        print("An error occurred while trying to add new status")
    else:
        print("New status was successfully added")

#@pysnooper.snoop()
def update_status():
    '''
    Updates information for an existing status
    '''
    status_id = input('Status ID: ')
    user_id = input('User ID: ')
    status_text = input('Status text: ')
    if not main.update_status(status_id, user_id, status_text, status_collection):
        print("An error occurred while trying to update status")
    else:
        print("Status was successfully updated")

def search_status():
    '''
    Searches a status in the database
    '''
    status_id = input('Enter status ID to search: ')
    result = main.search_status(status_id, status_collection)
    if not result:
        print("ERROR: Status does not exist")
    else:
        print(f"User ID: {result['user_id']}")
        print(f"Status ID: {result['_id']}")
        print(f"Status text: {result['status_text']}")

def delete_status():
    '''
    Deletes status from the database
    '''
    status_id = input('Status ID: ')
    if not main.delete_status(status_id, status_collection):
        print("An error occurred while trying to delete status")
    else:
        print("Status was successfully deleted")


def quit_program():
    '''
    Quits program
    '''
    snm.drop_data(user_collection, status_collection)
    sys.exit()

if __name__ == '__main__':
    db = snm.main()
    
    #I pulled the creation of the UserAccounts collection to see if this would fix
    #the problem where the program cannot find the newly uploaded data
    #It has not fixed the problem
    collection_1 = db['UserAccounts']
    user_collection = main.init_user_collection(collection_1)
    status_collection = main.init_status_collection(db)
    menu_options = {
        'A': load_users,
        'B': load_status_updates,
        'C': add_user,
        'D': update_user,
        'E': search_user,
        'F': delete_user,
        'G': add_status,
        'H': update_status,
        'I': search_status,
        'J': delete_status,
        'Q': quit_program
    }
    while True:
        user_selection = input("""
                            A: Load user database
                            B: Load status database
                            C: Add user
                            D: Update user
                            E: Search user
                            F: Delete user
                            G: Add status
                            H: Update status
                            I: Search status
                            J: Delete status
                            Q: Quit

                            Please enter your choice: """)
        if user_selection.upper() in menu_options:
            menu_options[user_selection.upper()]()
        else:
            print("Invalid option")
