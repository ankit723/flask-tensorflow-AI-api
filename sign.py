import mysql.connector

mydb= mysql.connector.connect(host ='localhost', user='root', password= '.mjo9876')
cursor= mydb.cursor()
cursor.execute('use kelvin_user')

def signup(details):
    global cursor
    cursor.execute('select Username from user_base_details')
    res = cursor.fetchall()
    for record in res:
        for username in record:
            if username==details[0]:
                return "username_exists"
            else:
                break
    
    cursor.execute("insert into user_base_details(Username, Name, Password, Email) values (%s, %s, %s, %s)", details)
    mydb.commit()
    return (f"Successfully Created Account Iris Welcomes You {details[1]}Your Authentication Token is {details[0]}_{details[2]}")


def signin(details):
    global cursor
    cursor.execute("select email, password from user_base_details where email = '%s'"%details[0])
    res = cursor.fetchall()
    if len(res)>0:
        for record in res:
            if record[1]==details[1]:
                return "True"
            return "False"
    return "False"
    
def signin_username(details):
    global cursor
    cursor.execute("select username, password from user_base_details where username = '%s'"%details[0])
    res = cursor.fetchall()
    if len(res)>0:
        for record in res:
            if record[1]==details[1]:
                return "True"
            return "False"
    return "False"



def routecheck(email):
    global cursor
    cursor.execute("select username, password from user_base_details where email = '%s'"%email)
    res=cursor.fetchall()
    for record in res:
        apiId = f"{record[0]}_{record[1]}"
        return apiId
        
def routecheck_username(username):
    global cursor
    cursor.execute("select username, password from user_base_details where username = '%s'"%username)
    res=cursor.fetchall()
    for record in res:
        apiId = f"{record[0]}_{record[1]}"
        return apiId
                

        