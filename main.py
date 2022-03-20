
from loguru import logger
import pymongo
import users
import user_status as us
import pandas as pd
import multiprocessing as mp
import time
import queue
#import socialnetwork_model as snm
#import pysnooper


# logger.remove()
# logger.add("log_{time}.log")


def init_user_collection(db):
    '''
    Creates and returns a new instance
    of UserCollection
    '''
    usercollection_obj = users.UserCollection(db)
    logger.info('new UserCollection object initialized.')

    return usercollection_obj

def init_status_collection(db):
    '''
    Creates and returns a new instance
    of UserStatusCollection
    '''
    userstatuscol_obj = us.UserStatusCollection(db)

    return userstatuscol_obj


def import_csv_in_chunks(filename, size=100):
    '''
    Imports CSV file in chunks of a defined size
    '''
    chunks = pd.read_csv(filename, chunksize=size, iterator=True)
    logger.info('Chunked data from CSV file')
    return chunks

def load_users_helper_func(data_to_add, data_that_is_done):
    '''
    Takes one chunk of data at a time and adds it to the database
    '''

    #Try #1
    #db_client = pymongo.MongoClient().user_collection.database
    
    #Try #2 
    #db = snm.main()
    #new_user_collection = init_user_collection(db)
    
    #Try #3
    #user_collection = init_user_collection(my_db)
    
    #Try #4
    # db = snm.main()
    # my_db = db['UserAccounts']
    # db_client = MongoClient().my_db
    
    #Try #5
    # my_db = MongoClient().socialnetwork 
    # user_collection = init_user_collection(my_db)
    
    
    #Try #6
    # mongo = snm.MongoDBConnection()

    # with mongo:
    #     db = mongo.connection.social_network
    
    # user_collection = init_user_collection(db)
    
    #Try #7
    # mongo = snm.MongoDBConnection()

    # with mongo:
    #     db = mongo.connection.social_network
    
    # my_db = db['UserAccounts']
    
    #Try #8
    client = client = pymongo.MongoClient(host='127.0.0.1', port=27017)
    
    db = client.social_network
    
    collection = db['UserAccounts']
    
    logger.info('Established a connection with MongoDB')
    
    while True:
        try:
            chunk = data_to_add.get_nowait()
        except queue.Empty:
            logger.info('data_to_add queue is empty')
            break
        else:
            logger.info('Almost about to add all the users')
            #logger.info(chunk)
            for row in chunk:
                #Try #6/#7/#8
                new_user = {'_id': row[0], 'email': row[1], 'user_name': row[2], 'user_last_name': row[3]}
                try:
                    collection.insert_one(new_user)
                except pymongo.errors.DuplicateKeyError:
                    logger.warning("This user already exists.")
                #Try #2/#4/#5
                #user_collection.add_user(user_id=row[0], user_name=row[1], user_last_name=row[2], email=row[3])
                
                #Try #1
                #new_user_collection.add_user(user_id=row[0], user_name=row[1], user_last_name=row[2], email=row[3])
            data_that_is_done.put(chunk)
            logger.info('chunk added to database')
            while not data_that_is_done.empty():
                data_that_is_done.get()
                #logger.info(data_that_is_done.get())
    return True

    
#@pysnooper.snoop()
def load_users(filename):
    '''
    Opens a CSV file with user data, chunks it, and
    adds it to the UserAccounts collection in MongoDB
    '''
    t = time.time()
    #Each chunk is one task
    #Number of logical cores on my computer is 12
    number_of_processes = 8
    data_to_add = mp.Queue()
    data_that_is_done = mp.Queue()
    processes = []
    
    data_chunks = import_csv_in_chunks(filename)
    for chunk in data_chunks:
        #Can I put a function in put() instead? Say a call to the helper function
        data_to_add.put(chunk)
        
    for w in range(number_of_processes):
        p = mp.Process(target=load_users_helper_func, args=(data_to_add, data_that_is_done))
        processes.append(p)
        p.start()
    
    for p in processes:
        logger.info('About to join processes together')
        p.join()

        
    print(time.time() - t)
    return True
        
        
def load_status_updates_helper_func(data_to_add, data_that_is_done):
    '''
    Takes one chunk of data at a time and adds it to the database
    '''
    client = client = pymongo.MongoClient(host='127.0.0.1', port=27017)
    
    db = client.social_network
    
    collection_1 = db['StatusUpdates']
    collection_2 = db['UserAccounts']
    
    while True:
        try:
            chunk = data_to_add.get_nowait()
        except queue.Empty:
            break
        else:
            for row in chunk:
                status_id = row[0] 
                user_id = row[1]
                status_text = row[2]
                query = collection_2.find_one({'_id':user_id})
                try:
                    query['_id']
                    logger.info(f'{user_id} was found.')
                except TypeError:
                    logger.warning(f'This user, {user_id}, does not exist')
                    return False
                else:
                    try:
                        new_status = {'_id': status_id, 'user_id': user_id, 'status_text': status_text}
                        collection_1.insert_one(new_status)
                    except pymongo.errors.DuplicateKeyError:
                        logger.warning("This status id already exists.")
                while not data_that_is_done.empty():
                    data_that_is_done.get()
    return True

def load_status_updates(filename):
    '''
    Opens a CSV file with user status data, chunks it, and
    adds it to the StatusUpdates collection in MongoDB
    '''
    t = time.time()
    #Each chunk is one task
    #Number of logical cores on my computer is 12
    number_of_processes = 8
    data_to_add = mp.Queue()
    data_that_is_done = mp.Queue()
    processes = []

    data_chunks = import_csv_in_chunks(filename)
    for chunk in data_chunks:
        data_to_add.put(chunk)
        
    for w in range(number_of_processes):
        p = mp.Process(target=load_users_helper_func, args=(data_to_add, data_that_is_done))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()

    print(time.time() - t)
    return True


def add_user(user_id, email, user_name, user_last_name, user_collection):
    '''
    Creates a new instance of User and stores it in user_collection
    (which is an instance of UserCollection)

    Requirements:
    - user_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
    user_collection.add_user() returns False).
    - Otherwise, it returns True.
    '''
    add_user_return = user_collection.add_user(user_id, email, user_name, user_last_name)
    return add_user_return


def update_user(user_id, email, user_name, user_last_name, user_collection):
    '''
    Updates the values of an existing user

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    '''
    update_user_return = user_collection.modify_user(user_id, email, user_name, user_last_name)
    return update_user_return


def delete_user(user_id, user_collection):
    '''
    Deletes a user from user_collection.

    Requirements:
    - Returns False if there are any errors (such as user_id not found)
    - Otherwise, it returns True.
    '''
    delete_user_return = user_collection.delete_user(user_id)
    return delete_user_return


def search_user(user_id, user_collection):
    '''
    Searches for a user in user_collection
    (which is an instance of UserCollection).

    Requirements:
    - If the user is found, returns the corresponding
    User instance.
    - Otherwise, it returns None.
    '''
    search_user_return = user_collection.search_user(user_id)
    logger.info(f'main.py: {search_user_return}')
    return search_user_return


def add_status(user_id, status_id, status_text, status_collection, user_collection):
    '''
    Creates a new instance of UserStatus and stores it in user_collection
    (which is an instance of UserStatusCollection)

    Requirements:
    - status_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
    user_collection.add_status() returns False).
    - Otherwise, it returns True.
    '''
    add_status_return = status_collection.add_status(status_id, user_id, status_text, user_collection)
    return add_status_return


def update_status(status_id, user_id, status_text, status_collection):
    '''
    Updates the values of an existing status_id

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    '''
    update_status_return = status_collection.modify_status(status_id, user_id, status_text)
    return update_status_return


def delete_status(status_id, status_collection):
    '''
    Deletes a status_id from user_collection.

    Requirements:
    - Returns False if there are any errors (such as status_id not found)
    - Otherwise, it returns True.
    '''
    delete_status_return = status_collection.delete_status(status_id)
    return delete_status_return


def search_status(status_id, status_collection):
    '''
    Searches for a status in status_collection

    Requirements:
    - If the status is found, returns the corresponding
    UserStatus instance.
    - Otherwise, it returns None.
    '''
    search_status_return = status_collection.search_status(status_id)
    return search_status_return
