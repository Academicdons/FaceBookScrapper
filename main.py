import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDialog
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import pickle
import os


class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("resources/UIFiles/welcomePage.ui", self)
        self.login.clicked.connect(self.goToLogin)
        

    def goToLogin(self):

        if self.usernameField.text() == "" or self.passwordField.text() == "" or self.threadsField.text() == "":
            errorMessage = "Only Headless option can be left Blank"
            self.errorsField.setText(errorMessage)

        self.usernameValue = self.usernameField.text()

        self.passwordValue = self.passwordField.text()

        if self.headlessField.isChecked():
            self.stateValue = "Headless"
        else:
            self.stateValue = "NotHeadless"

        self.threadCountValue = int(self.threadsField.text())

        self.scrollsValue = int(self.scrollsField.text())

        self.valuesGotten = {
            "username": f"{self.usernameValue}",
            "password": f"{self.passwordValue}",
            "state": f"{self.stateValue}",
            "threadCount": f"{self.threadCountValue}",
            "scrolls": f"{self.scrollsValue}",
        }
        # save function
        #Create an empty variable

        empty_list = ""
        with open('resources/PickleFiles/logins.pkl', 'wb') as f:
            pickle.dump(empty_list, f)
            f.close()
        with open('resources/PickleFiles/logins.pkl', 'wb') as f:
            pickle.dump(self.valuesGotten, f)
            f.close()
        
        inputScreen = inputFacebookLinks()
        widget.addWidget(inputScreen)
        widget.setCurrentIndex(widget.currentIndex()+1)


class inputFacebookLinks(QDialog):
    def __init__(self):
        super(inputFacebookLinks, self).__init__()
        loadUi("resources/UIFiles/runbot.ui", self) 
        self.startButton.clicked.connect(self.saveFBLInks)
    
    def saveFBLInks(self):
        self.sendemails = self.sendEmails.toPlainText() 
        self.userFBLinks = self.editArea.toPlainText()

        
        empty_list = ""
        self.sendemails = self.sendemails
        with open('resources/PickleFiles/mailsToSend.pkl', 'wb') as f:
            pickle.dump(empty_list, f)
            f.close()
        

        with open('resources/PickleFiles/mailsToSend.pkl', 'wb') as f:
            pickle.dump(self.sendemails, f)
            f.close()

        #Save the Urls found
        with open('resources/PickleFiles/facebookUrlsList.pkl', 'wb') as f:
            pickle.dump(empty_list, f)
            f.close()
        with open('resources/PickleFiles/facebookUrlsList.pkl', 'wb') as f:
            pickle.dump(self.userFBLinks, f)
            f.close()
        
        runbot = runBot()
        widget.addWidget(runbot)
        widget.setCurrentIndex(widget.currentIndex()+1)

class runBot(QDialog):
    def __init__(self):
        super(runBot, self).__init__()
        loadUi("resources/UIFiles/home.ui", self)
        self.p = None
        self.editArea.setReadOnly(True)
        self.editArea.insertPlainText("Welcome and Witness some magic...")
        self.start_process()
        self.exitButton.clicked.connect(self.killBot)

    def killBot(self):

        app.closeAllWindows()


    def message(self, s):
        self.editArea.appendPlainText(s)

    def start_process(self):
        if self.p is None:  # No process running.
            self.message("\n Executing process")
            self.p = QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running.
            self.p.readyReadStandardOutput.connect(self.handle_stdout)
            self.p.readyReadStandardError.connect(self.handle_stderr)
            self.p.stateChanged.connect(self.handle_state)
            self.p.finished.connect(self.process_finished)  # Clean up once complete.
            self.p.start("python3", ['scripts/facebook.py'])

    def handle_stderr(self):
        data = self.p.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        # Extract progress if it is in the data.
        # progress = simple_percent_parser(stderr)
        # if progress:
        #     self.progress.setValue(progress)
        self.message(stderr)

    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.message(stdout)

    def handle_state(self, state):
        states = {
            QProcess.NotRunning: 'Task Completed',
            QProcess.Starting: 'Starting',
            QProcess.Running: 'Running',
        }
        state_name = states[state]
        self.message(f"\n State changed: {state_name}")

    def process_finished(self):
        self.message("\n Process finished. You can click on Login to restart with a new list")
        self.p = None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    welcome = WelcomeScreen()
    widget = QtWidgets.QStackedWidget()
    widget.setWindowIcon(QIcon('resources/icon/icon.png'))
    widget.addWidget(welcome)
    widget.setFixedHeight(605)
    widget.setFixedWidth(1024)

    title = "FBWhoozupBot Pro+"
    widget.setWindowTitle(title)

    widget.setWindowFlag(Qt.FramelessWindowHint)
    widget.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")
