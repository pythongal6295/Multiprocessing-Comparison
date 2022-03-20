'''
Classes for user information for the
social network project
'''
# pylint: disable=R0903

from loguru import logger
import pymongo


class UserCollection():
    '''
    Contains a collection of Users objects
    '''

    def __init__(self, db):
        #Try #1/4
        #self.database = db['UserAccounts']

        #Try #2
        #self.database = pymongo.MongoClient().db


        #Try #3-8
        self.database = db

        logger.info('New UserCollection object was initialized.')


    def add_user(self, user_id, email, user_name, user_last_name):
        '''
        Adds a new user to the collection
        '''
        try:
            new_user = {'_id': user_id, 'email': email, 'user_name': user_name, 'user_last_name': user_last_name}
            self.database.insert_one(new_user)
            logger.info(f'Added a new user to UserCollection database with user_id: {user_id}')
            return True
        except pymongo.errors.DuplicateKeyError:
            logger.warning("This user already exists.")
            return False


    def modify_user(self, user_id, email, user_name, user_last_name):
        '''
        Modifies an existing user
        '''
        query = self.database.find_one({'_id':user_id})
        try:
            query['_id']
        except TypeError:
            logger.warning(f'This user, {user_id}, does not exist')
            return False
        self.database.update_one({'_id': user_id}, {'$set': {'email': email, 'user_name': user_name, 'user_last_name': user_last_name}})
        logger.info(f'{user_id} was modified with {email}, {user_name}, {user_last_name}')
        return True


    def delete_user(self, user_id):
        '''
        Deletes an existing user
        '''
        query = self.database.find_one({'_id':user_id})
        try:
            query['_id']
        except TypeError:
            logger.warning(f'This user, {user_id}, does not exist')
            return False
        self.database.delete_one({'_id': user_id})
        logger.info(f'{user_id} was deleted from database.')
        return query


    def search_user(self, user_id):
        '''
        Searches for user data
        '''

        query = self.database.find_one({'_id': user_id})
        try:
            query['_id']
            logger.info(f'{user_id} was found.')
            logger.info(f'users.py: {query}')
            return query
        except TypeError:
            logger.warning(f'This user, {user_id}, does not exist')
            return False
