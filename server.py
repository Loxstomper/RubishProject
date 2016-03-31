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


def create_table():
    db_c.execute('CREATE TABLE IF NOT EXISTS rubbish(date TEXT, day TEXT, time TEXT, sound TEXT)')


def get_get_data_add_to_db():

    global s
    conn, addr = s.accept()

    data = conn.recv(2048)  # buffer of 2048 bytes
    print('Received data from: ', addr)
    global rubbish_time
    rubbish_time = data.decode()
    print(rubbish_time)

    data = conn.recv(2048)  # buffer of 2048 bytes
    global sound
    sound = data.decode()
    print(rubbish_time)

    # server side creations no point wasting cpu cycles on the one in the bin
    date = str(time.strftime('%d-%m-%Y'))
    day = str(time.strftime('%A'))

    # have to reconnect to database because i close connection every iteration
    global db
    global db_c
    db = sqlite3.connect('rubbish.db')
    db_c = db.cursor()

    # add to db and save
    db_c.execute("INSERT INTO rubbish(date, day, time, sound) VALUES (?, ?, ?, ?)",
                 (date, day, rubbish_time, sound))
    print("Added values to database: ", date, ",", day, ",", rubbish_time, ",", sound)
    db.commit()
    print('Saved changes to database.')

    # close connection to db
    db_c.close()
    db.close()
    print('Closed the database.')
    print('Waiting for a connection...\n')

# Program

# set up server
try:
    s.bind((host, port))
except socket.error as e:
    print(str(e))

s.listen(5)  # max of 5 connections simultaneously
print("waiting for a connection...\n")

# create the table if it doesnt exist
create_table()

while True:
    get_get_data_add_to_db()




