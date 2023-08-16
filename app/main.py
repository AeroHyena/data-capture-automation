"""
This script launches the app and its gui interfaces.
All the elements of the gui is defined and outlined on this script.
"""

# Kivy
# from kivy.app import App
# from kivy.uix.label import Label

# Local modules
# import pdf_ocr
from apply_data import DatabaseManager


## Define your server keys as a dictionary and create a DatabaseManager class instance
server = {
    "port": 9005,
    "host": "10.101.85.25",
    "user": "root",
    "password": "123456", 
    "database": "mysqldb"  
}

database = DatabaseManager(server)

## Create the main app and its gui interface and functionalities
# class MainApp(App):
"""
    This is the main class of the gui interface.
    It is responsible for the gui and all its functionalities.
    
"""

    # def build(self):
        # Put a temporary placeholder text on the gui interface
        # return Label(text='Placeholder')



## On app launch, initialize the gui interface and establish a connection to the database
if __name__ == '__main__':
    # MainApp().run()

    try:
        database.connect()
    finally:
        database.close_connection()

