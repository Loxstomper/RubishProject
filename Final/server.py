import sqlite3
import socket
import time

# server
host = ''
port = 5555  # ask IT at school about what ports I can use
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # ipv4 / tcp connection

# database
db = sqlite3.connect('rubbish.db')
db_c = db.cursor()

# values
rubbish_id = ''
rubbish_name = ''
rubbish_time = ''
sound = ''


def create_table():
    # db_c.execute('CREATE TABLE IF NOT EXISTS rubbish(date TEXT, day TEXT, time TEXT, sound TEXT)')
    db_c.execute('CREATE TABLE IF NOT EXISTS rubbish(date TEXT, day TEXT, time TEXT, id INTEGER, name TEXT, sound TEXT)')


def get_data_add_to_db():

    global s
    conn, addr = s.accept()

    data = conn.recv(4096)  # buffer of 2048 bytes
    # print(data)
    print('Received data from: ', addr, '\n')
    global rubbish_id
    global rubbish_name
    global rubbish_time
    global sound
    data = str(data.decode())

    try:
        # rubbish_time, sound = data.split('~')
        rubbish_id, rubbish_name, sound = data.split('~')  # using ~ to split
        # rubbish_id = int(rubbish_id)
    except:
        pass

    # server side creations no point wasting cpu cycles on the one in the bin
    date = str(time.strftime('%d-%m-%Y'))
    day = str(time.strftime('%A'))
    rubbish_time = str(time.strftime('%I:%M:%S'))

    # have to reconnect to database because i close connection every iteration
    global db
    global db_c
    db = sqlite3.connect('rubbish.db')
    db_c = db.cursor()

    # add to db and save
    '''db_c.execute("INSERT INTO rubbish(date, day, time, sound) VALUES (?, ?, ?, ?)",
                 (date, day, rubbish_time, sound))'''

    db_c.execute("INSERT INTO rubbish(date, day, time, id, name, sound) VALUES (?, ?, ?, ?, ?, ?)",
                 (date, day, rubbish_time, rubbish_id, rubbish_name, sound))

    print("Added values to the database:")
    print("Date : ", date)
    print("Day  : ", day)
    print("ID   : ", rubbish_id)
    print("Name : ", rubbish_name)
    print("Time : ", rubbish_time)
    print("Sound: ", sound, "\n")
    db.commit()
    print('Saved changes to database.')

    # close connection to db
    db_c.close()
    db.close()
    print('Closed the database. \n')
    print('Waiting for a connection...\n')

# Program

# set up server
try:
    s.bind((host, port))
except socket.error as e:
    print(str(e))

s.listen(1)  # max of 5 connections simultaneously
print("waiting for a connection...\n")

# create the table if it doesnt exist
create_table()

while True:
    get_data_add_to_db()




