from psycopg2 import connect, pool
import os
import logging

logger = logging.getLogger(__name__)

class DbManager():
    """
    Class to manage the connection pool to the PostgreSQL database.
    It uses the psycopg2 library to manage the connection pool.
    """

    def __init__(self):
        self.connection_pool = None


    def start_connection_pool(self)->pool.SimpleConnectionPool:
        """
        Create a connection pool to the PostgreSQL database.
        This function initializes a connection pool with the specified parameters.
        It uses the psycopg2 library to manage the connection pool.
        """
        global connection_pool
        try:
            connection_pool = pool.SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT'),
                database=os.getenv('DB_NAME'),
            )
            if connection_pool:
                logger.info("Connection pool created successfully")
                self.connection_pool = connection_pool
            
        except Exception as e:
            logger.error(f"Error creating connection pool: {e}")


    def get_connection_from_pool(self):
        try:
            conn = self.connection_pool.getconn()
            if conn:
                logger.info(f"Connection obtained from pool: {conn}")
                return conn
        except Exception as e:
            logger.info(f"Error getting connection from pool: {e}")
            return None

    def release_connection(self, conn):
        """
        Release the connection back to the pool.
        """
        if conn:
            self.connection_pool.putconn(conn)
            logger.info(f"Connection released back to pool: {conn}")
        else:
            logger.error("Connection is None, cannot release to pool")
