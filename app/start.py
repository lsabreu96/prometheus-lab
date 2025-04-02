import logging
from db import DbManager

logger = logging.getLogger(__name__)


def startup():

    global db_manager
    db_manager = DbManager()
    db_manager.start_connection_pool()    
    conn = db_manager.get_connection_from_pool()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cadastro (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100),
            idade INT
        )
    """)
    conn.commit()

    cursor.close()
    db_manager.release_connection(conn)

    return db_manager