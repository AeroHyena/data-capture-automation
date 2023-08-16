"""
This module is responsible for accessing the MySQL
database to add and retrieve entries.
"""

import mysql.connector


class DatabaseManager:
    """
    A class for managing a database connection.

    This class is responsible for managing and manipulating a connetion to a provided database.

    Attributes:
        server (dict): A dictionary containing the keys and values neccessary 
                       for establishing a database connection
        connection: A variable containing anestablished connection to a server.
        cursor: A variable used to execute queries on a database.

    Methods:
        __init__(self, server: dict): Initializas the DatabaseManager 
                                      object with the given server keys.
        connect(self): Establlishes a connection to the provided server
        close_connection(self): Closes a connection if one is open.
        insert_data(self, data): Inserts the provided data into the database.
        retrieve_data(self, document_id): Retrieves data from the 
                                          database using the provided document_id.
        rerieve_newest_entry(self): Retrieves the most recent entry in the database.

    Usage Examples:
        data_5 = retrieve_data(11275)
        newest_entry = retrieve_newest_entry()

    Dependencies:
        mysql.connector

    Limitations:
        This class assumes the database in use is a MySQL database.
    """
    def __init__(self, server: dict):
        """
        Initialize the DatabaseManager instance.

        Parameters:
            server (dict): a dictionary containing database configuration parameters.
                           The dictionary should have keys 'host', 
                           'user', 'password' and 'database'.
        """
        self.server = server
        # Check if the required server data is provided
        if not (server["host"] and
                server["port"] and
                server["user"] and
                server["password"] and
                server["database"]):
            raise ValueError("Please provide the host, port,"
                             " user, password and database keys witin your server dictionary.")
        self.connection = None
        self.cursor = None


    def connect(self):
        """
        Establishes a connection to the provided database 
        and creates a cursor for query execution.
        """
        # connect to the database
        self.connection = mysql.connector.connect(
            host=self.server["host"],
            port=self.server["port"],
            user=self.server["user"],
            password=self.server["password"],
            database=self.server["database"]
        )
        print(f"connected to database at {self.server['host']}:"
              "{self.server['port']} as {self.server['user']}")

        # create the cursor variable for the execution of queries
        self.cursor = self.connection.cursor()
        print("created cursor for database connection")


    def close_connection(self):
        """
        Closes the database connection if any are present
        """
        if self.connection:
            self.connection.close()
            print("The connection to the database has been closed.")
        print("No database connection is found")


    def insert_data(self, data):
        """
        Create a new data entry into the database using the
        provided data. 
        Returns the unique ID of the data entry
        """
        insert_query = f"{data}"
        self.cursor.execute(insert_query)
        document_id = self.cursor.lastrowid

        print(f"data created at document no {document_id}")
        return document_id



    def retrieve_data(self, document_id):
        """
        Retrieve data using the specified ID.
        """
        query = f"SELECT * FROM weighbridge_data WHERE document_id = {document_id}"
        self.cursor.execute(query)
        data = self.cursor.fetchone()

        print(f"data retrieved for document no {document_id}")
        return data


    def rerieve_newest_entry(self):
        """
        Retrieve the ID fof the most recent data inserted
        """
        query = "SELECT * FROM weighbrighe_data ORDER BY created_at DESC LIMIT 1"
        self.cursor.execute(query)

        return self.cursor.fetchone()
