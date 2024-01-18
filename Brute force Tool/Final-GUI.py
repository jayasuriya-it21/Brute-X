import sys
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QPushButton,
    QTextBrowser,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QFileDialog,
)
from PyQt5.QtCore import Qt

class BruteForceGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Brute-X")
        self.setGeometry(100, 100, 900, 750)

        self.initUI()

    def initUI(self):

        self.title_label = QLabel("Brute-X", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.set_hacking_font(self.title_label)

        self.center_layout = QVBoxLayout()
        self.center_layout.addWidget(self.title_label)

        # Create a horizontal layout for the login inputs and labels
        self.login_layout = QHBoxLayout()
        self.login_url_label = QLabel("Login Page URL:          ", self)
        self.login_url_label.setStyleSheet("font-size: 16px; font-weight: bold; font-family: 'Courier New'")
        self.login_url_entry = QLineEdit(self)
        self.login_layout.addWidget(self.login_url_label)
        self.login_layout.addWidget(self.login_url_entry)
        self.center_layout.addLayout(self.login_layout)

        self.username_layout = QHBoxLayout()
        self.username_label = QLabel("Username:                ", self)
        self.username_label.setStyleSheet("font-size: 16px; font-weight: bold; font-family: 'Courier New'")
        self.username_entry = QLineEdit(self)
        self.username_layout.addWidget(self.username_label)
        self.username_layout.addWidget(self.username_entry)
        self.center_layout.addLayout(self.username_layout)

        # Create a horizontal layout for the wordlist input and "Browse" button
        self.wordlist_layout = QHBoxLayout()
        self.wordlist_label = QLabel("Wordlist File (optional):", self)
        self.wordlist_label.setStyleSheet("font-size: 16px; font-weight: bold; font-family: 'Courier New';")
        self.wordlist_entry = QLineEdit(self)
        self.browse_button = QPushButton("Browse", self)
        self.wordlist_layout.addWidget(self.wordlist_label)
        self.wordlist_layout.addWidget(self.wordlist_entry)
        self.wordlist_layout.addWidget(self.browse_button)
        self.center_layout.addLayout(self.wordlist_layout)

        self.button_layout = QHBoxLayout()
        self.test_button = QPushButton("Test Passwords", self)
        self.break_button = QPushButton("Break", self)
        self.button_layout.addWidget(self.test_button)
        self.button_layout.addWidget(self.break_button)
        self.center_layout.addLayout(self.button_layout)

        # Create a vertical layout for the "Valid login found" message
        self.valid_login_layout = QVBoxLayout()
        self.valid_login_label = QLabel("", self)
        self.valid_login_label.setAlignment(Qt.AlignCenter)
        self.valid_login_label.setStyleSheet("font-size: 30px; font-weight: bold; font-family: 'Courier New'")
        self.valid_login_layout.addWidget(self.valid_login_label)
        self.center_layout.addLayout(self.valid_login_layout)

        self.output_text = QTextBrowser(self)
        self.output_text.setStyleSheet("font-size: 16px; font-family: 'Courier New';")
        self.center_layout.addWidget(self.output_text)

        script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the script directory
        self.wordlist_file_path = os.path.join(script_dir, "wordlist.txt")  # Join with filename

        self.break_operation_flag = False  # Initialize the break flag
        self.test_in_progress = False  # Initialize the test in progress flag
        self.password_found = None  # Initialize the found password variable

        self.center_widget = QWidget()
        self.center_widget.setLayout(self.center_layout)
        self.setCentralWidget(self.center_widget)

        # Apply styles to input boxes
        input_styles = """
            QLineEdit {
                padding: 12px 20px;
                margin: 8px 0;
                border: 1px solid #000000;
                font-family: 'Times New Roman', Times, serif;
                border-radius: 23px;
                font-size: 16px;
            }

            QLineEdit:hover {
                border-color: #0099ff;
            }
        """
        self.login_url_entry.setStyleSheet(input_styles)
        self.username_entry.setStyleSheet(input_styles)
        self.wordlist_entry.setStyleSheet(input_styles)

        # Apply styles to buttons
        button_styles = """
            QPushButton {
                padding: 12px 20px;
                background-color: #3300ff;
                color: white;
                font-family: 'Times New Roman', Times, serif;
                border: none;
                border-radius: 21px;
                font-size: 16px;
            }

            QPushButton:hover {
                background-color: #25b800;
                color: black;
            }
        """
        self.browse_button.setStyleSheet(button_styles)
        self.test_button.setStyleSheet(button_styles)
        self.break_button.setStyleSheet(button_styles)

        self.browse_button.clicked.connect(self.browse_wordlist)
        self.test_button.clicked.connect(self.start_or_resume_test)  # Updated the click event
        self.break_button.clicked.connect(self.break_operation)

    def set_hacking_font(self, widget):
        font = widget.font()
        font.setFamily("Courier New")  # Use a monospace font
        font.setPointSize(28)  # Set the font size
        font.setBold(True)  # Make the font bold
        widget.setFont(font)

    def browse_wordlist(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Select Wordlist File", "", "Text Files (*.txt);;All Files (*)"
        )
        if filepath:
            self.wordlist_entry.setText(filepath)

    def start_or_resume_test(self):
        if self.test_in_progress:
            self.output_text.insertHtml(
                '<span style="color: red;">Test Password operation is already in progress.</span><br><br>'
            )
            return

        login_page_url = self.login_url_entry.text()
        username = self.username_entry.text()
        wordlist_file_path = self.wordlist_entry.text() or "wordlist.txt"

        if not login_page_url or not username:
            self.output_text.insertHtml(
                '<span style="color: red;">Please enter both Login Page URL and Username.</span><br><br>'
            )
            return

        with open(wordlist_file_path, "r") as f:
            wordlist = [line.strip() for line in f.readlines()]

        self.break_operation_flag = False  # Reset the break flag
        self.valid_login_label.hide()  # Hide the valid login label

        try:
            response = requests.get(login_page_url, timeout=5)  # Timeout set to 5 seconds
        except requests.exceptions.RequestException as e:
            self.output_text.insertHtml(
                f'<span style="color: red;">URL Connection to {login_page_url} timed out. ({str(e)})</span><br><br>'
            )
            return

        if response.status_code != 200:
            self.output_text.insertHtml(
                f'<span style="color: red;">URL {login_page_url} not found or returned a {response.status_code} status code.</span><br><br>'
            )
            return

        page_content = response.content
        soup = BeautifulSoup(page_content, "html.parser")

        login_form = soup.find("form", method="POST")
        if login_form:
            login_action = login_form.get("action")
            login_url = urljoin(login_page_url, login_action)
        else:
            self.output_text.insertHtml(
                f'<span style="color: red;">Login form not found.</span><br><br>'
            )
            return

        self.test_in_progress = True  # Set the test in progress flag

        for password in wordlist:
            # Check if the "Break" button is pressed
            if self.break_operation_flag:
                self.output_text.insertHtml(
                    '<span style="color: orange;">Operation was manually stopped.</span><br><br>'
                )
                self.valid_login_label.hide()
                self.test_in_progress = False  # Reset the test in progress flag
                break

            data = {"username": username, "password": password}
            response = requests.post(login_url, data=data)

            try:
                response_json = response.json()
                if response_json.get("success"):
                    self.output_text.insertHtml(
                        f'<span style="color: green;">Valid login found: {username}:{password}</span><br><br>'
                    )
                    self.valid_login_label.setText(f'<span style="color: green;">Password found: {password}')
                    self.valid_login_layout.setAlignment(Qt.AlignCenter)
                    self.valid_login_label.show()
                    self.test_in_progress = False  # Reset the test in progress flag
                    break
            except:
                if "Welcome" in response.text:
                    self.output_text.insertHtml(
                        f'<span style="color: green;">Valid login found: {username}:{password}</span><br><br>'
                    )
                    self.valid_login_label.setText(f'<span style="color: green;">Password found: {password}')
                    self.valid_login_layout.setAlignment(Qt.AlignCenter)
                    self.valid_login_label.show()
                    self.test_in_progress = False  # Reset the test in progress flag
                    break

                self.output_text.insertHtml(
                    f'Trying Password: {password}<br>'
                    f'<span style="color: red;">Password : {password} - NOT MATCH</span><br><br>'
                )
                self.output_text.ensureCursorVisible()
                QApplication.processEvents()  # Update the GUI to show the progress
                time.sleep(0)  # add a delay of 0.5 seconds between requests

    def break_operation(self):
        if self.test_in_progress:
            self.break_operation_flag = True
        else:
            self.output_text.insertHtml(
                '<span style="color: orange;">No test operation in progress to break.</span><br><br>'
            )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = BruteForceGUI()
    gui.show()
    sys.exit(app.exec_())
 