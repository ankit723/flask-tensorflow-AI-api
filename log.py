from getpass import getpass
import mysql.connector

mydb= mysql.connector.connect(host ='localhost', user='root', password= '.mjo9876')

print('connected')

cursor= mydb.cursor()
cursor.execute('use kelvin_user')

def create_logs(log):
    global cursor
    cursor.execute("insert into user_chat_logs(ChatInput, ChatOutput, Error, Username) values (%s, %s, %s, %s)", log)
    mydb.commit()
    return ('Logging Successfull')



