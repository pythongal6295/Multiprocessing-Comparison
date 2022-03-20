from loguru import logger
import pymongo

# logger.remove()
# logger.add('log_{time}.log')


class UserStatusCollection():
    '''
    Contains a collection of User Status objects
    '''
    def __init__(self, db):
        self.database = db['StatusUpdates']
        logger.info('New UserStatusCollection object was initialized.')

    def add_status(self, status_id, user_id, status_text, user_collection):
        '''
        Adds a new status to the collection
        '''
        query = user_collection.database.find_one({'_id':user_id})
        try:
            query['_id']
            logger.info(f'{user_id} was found.')
        except TypeError:
            logger.warning(f'This user, {user_id}, does not exist')
            return False
        else:
            try:
                new_user_status = {'_id': status_id, 'user_id': user_id, 'status_text': status_text}
                self.database.insert_one(new_user_status)
                logger.info(f'Added a new status to StatusCollection database with status_id: {status_id}')
                return True
            except pymongo.errors.DuplicateKeyError:
                logger.warning("This status id already exists.")
                return False


    def modify_status(self, status_id, user_id, status_text):
        '''
        Modifies an existing status
        '''
        query = self.database.find_one({'_id':status_id})
        try:
            query['_id']
        except TypeError:
            logger.warning(f'This status_id, {status_id}, does not exist')
            return False
        self.database.update_one({'_id': status_id}, {'$set': {'user_id': user_id, 'status_text': status_text}})
        logger.info(f'{status_id} was modified with {user_id}, {status_text}')
        return True


    def delete_status(self, status_id):
        '''
        Deletes an existing status
        '''
        query = self.database.find_one({'_id':status_id})
        try:
            query['_id']
        except TypeError:
            logger.warning(f'This status, {status_id}, does not exist')
            return False
        self.database.delete_one({'_id': status_id})
        logger.info(f'{status_id} was deleted from database.')
        return True


    def search_status(self, status_id):
        '''
        Searches for status data
        '''
        query = self.database.find_one({'_id':status_id})
        try:
            query['_id']
            logger.info(f'{status_id} was found.')
            logger.info(f'users_status.py: {query}')
            return query
        except TypeError:
            logger.warning(f'This status_id, {status_id}, does not exist')
            return False
