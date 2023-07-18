"""
This script launches the app and its gui interfaces.
All the elements of the gui is defined and outlined on this script.
"""
#Kivy
from kivy.app import App
from kivy.uix.label import Label



## Create the main app and its gui interface and functionalities
class MainApp(App):
    """
    This is the main class of the gui interface.
    It is responsible for the gui and all its functionalities.
    
    """

    def build(self):
        # Put a temporary plaveholder text on the gui interface
        return Label(text='Placeholder')



## On app launch, initialize the gui interface
if __name__ == '__main__':
    MainApp().run()
