import os
import sqlite3
import time
from parser import Parser
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

Window.size = (1080, 1920)

class MainScreen(Screen):
    def start_parse(self):
        data = Parser()
        data.get_data()
        data.parse_data()

    def clear(self):
        try:
            os.remove('data.json')
            os.remove('companies.db')
        except:
            pass

class AnotherScreen(Screen):
    rows = ListProperty([("Id", "Name", "Price")])

    def get_data(self):
        try:
            conn = sqlite3.connect('companies.db')
            c = conn.cursor()
            c.execute('''SELECT * FROM companies''')
            self.rows = c.fetchall()
        except:
            pass


class ScreenManagement(ScreenManager):
    def viewDB_screen(self):
        name = str(time.time())
        s = AnotherScreen(name=name)
        self.add_widget(s)
        self.current = name
        s.get_data()
        os.remove('companies.db')

presentation = Builder.load_file("app.kv")


class MainApp(App):
    def build(self):
        return presentation

MainApp().run()