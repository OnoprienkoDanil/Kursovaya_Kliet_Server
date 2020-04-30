import socket
import Data
import json
import pickle
import numpy as np

class ConClass:
 pass
print("hello")
PORT = 12008
HOST = ''
serv = socket.socket()
serv.bind((HOST, PORT))
serv.listen()
conn, addr = serv.accept()
print('Connect', addr)
db = Database.Database()
while True:
 data = conn.recv(4096)
 if data:
  try:
   data = data.decode('utf-8')
   arrayOfTables = db.getTableList()
   print(arrayOfTables)
   if data in arrayOfTables:
    table = db.getTable(data)
    conn.sendall(table)
  except:
   pass
   try:
    newTable = pickle.loads(data)
    db.updateTable(newTable)
   except:
   pass
