import psycopg2
from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton, QLabel, QLineEdit, QMessageBox)
from PyQt5.QtGui import QIcon, QPixmap
import base64
from Addresses import icon_image
from General.SelectTibiaTab import SelectTibiaTab
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
# Fetch database configuration
DB_HOST = config['database']['host']
DB_PORT = config['database']['port']
DB_NAME = config['database']['name']
DB_USER = config['database']['user']
DB_PASSWORD = config['database']['password']


class LoginTab(QWidget):
    def __init__(self):
        super().__init__()

        # Load Icon
        self.setWindowIcon(QIcon(pixmap) if (pixmap := QPixmap()).loadFromData(base64.b64decode(icon_image)) else QIcon())

        # Set Title and Size
        self.setFixedSize(300, 150)
        self.setWindowTitle("EasyBot Login")

        # Instances
        self.main_window = None

        # Layout
        self.layout = QGridLayout(self)

        # Labels
        self.username_label = QLabel('Username:', self)
        self.password_label = QLabel('Password:', self)

        # Line Edits
        self.username_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        # Buttons
        self.login_button = QPushButton('Login', self)

        # Buttons Functions
        self.login_button.clicked.connect(self.check_login)

        # Add widgets to layout
        self.layout.addWidget(self.username_label, 0, 0)
        self.layout.addWidget(self.username_input, 0, 1)
        self.layout.addWidget(self.password_label, 1, 0)
        self.layout.addWidget(self.password_input, 1, 1)
        self.layout.addWidget(self.login_button, 2, 0, 1, 2)

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if self.verify_user_in_db(username, password):
            self.open_main_window()
        else:
            QMessageBox.warning(self, "Error", "Incorrect username or password")

    def verify_user_in_db(self, username, password):
        try:
            # Establish a connection to the PostgreSQL database
            connection = psycopg2.connect(
                host=DB_HOST,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                port=DB_PORT
            )

            cursor = connection.cursor()

            # Query to check if the username and password exist in the database
            query = """
                SELECT user_name, user_password, expiry_date - NOW() AS days_left
                FROM users
                WHERE user_name = %s AND user_password = %s;
            """
            cursor.execute(query, (username, password))

            result = cursor.fetchone()

            # Close the cursor and connection
            cursor.close()
            connection.close()

            # If a user is found, check the number of days left
            if result is not None:
                days_left = result[2].days  # Extract the days left from the query result
                QMessageBox.warning(self, "License", f"You still have: {days_left} days left")
            return result is not None

        except Exception as e:
            QMessageBox.warning(self, "Database Error", f"An error occurred: {e}")
            return False

    def open_main_window(self):
        # Close login window and open the main window
        self.close()
        self.main_window = SelectTibiaTab()
        self.main_window.show()
