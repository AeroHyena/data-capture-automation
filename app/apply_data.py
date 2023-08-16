"""
This module is responsible for accessing the MySQL
database to add and retrieve entries.
"""

import mysql.connector


class DatabaseManager:
    def __init__(self, server: dict):
        """
        Initialize the DatabaseManager instance.

        Parameters:
            server (dict): a dictionary containing database configuration parameters.
                           The dictionary should have keys 'host', 'user', 'password' and 'database'.
        """ 
        self.server = server
        # Check if the required server data is provided
        if not (server["host"] and server["port"] and server["user"] and server["password"] and server["database"]):
            raise ValueError("Please provide the host, port, user, password and database keys witin your server dictionary.")
        self.connection = None
        self.cursor = None


    def connect(self):
        # connect to the database
        self.connection = mysql.connector.connect(
            host=self.server["host"],
            port=self.server["port"],
            user=self.server["user"],
            password=self.server["password"],
            database=self.server["database"]
        )
        print(f"connected to database at {server['host']}:{server['port']} as {server['user']}")

        # create the cursor variable for the execution of queries
        self.cursor = self.connection.cursor()
        print("created cursor for database connection")
    

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("The connection to the database has been closed.")


    def insert_data(data):
        """
        Create a new data entry into the database using the
        provided data. 
        Returns the unique ID of the data entry
        """
        insert_query = f"{data}"
    
        self.cursor.execute(insert_query)
        
        document_id = cursor.lastrowid

        print(f"data created at document no {document_id}")
        return document_id



    def retrieve_data(document_id):
        """
        Retrieve data using the specified ID.
        """
        query = f"SELECT * FROM weighbridge_data WHERE document_id = {document_id}"
        delf.cursor.execute(query)
        data = cursor.fetchone()

        print(f"data retrieved for document no {document_id}")
        return data


    def rerieve_last_entry():
        """
        Retrieve the ID fof the most recent data inserted
        """
        query = "SELECT * FROM weighbrighe_data ORDER BY created_at DESC LIMIT 1"
        self.cursor.execute(query)
        
        return self.cursor.fetchone()
        
