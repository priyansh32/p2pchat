import socket
import threading
from queue import Queue

# Peer 1: 100.10.14.205
# Peer 2: 10.53.164.197

# Each peer has two sockets: one acts as a server and one as a client.
# The server socket is used to listen for connections from the other peer.
# The client socket is used to send messages to the other peer.
# the client socket is dynamically created each time a connection is made.

# two threads are implemented: one to listen to messages from the other peer and one to send messages to the other peer.
# the two threads are started when the server socket is bound and listening for connections.

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()

PORT = 12000
PORT2 = 12001

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', PORT))
server_socket.listen(1)

# Input the IP address of the other peer:
print("To establish a connection with the other peer, enter the IP address of the other peer:")
peer = input('Input the IP address of the other peer: ')


def listen_for_messages():
    while True:
        conn, address = server_socket.accept()
        message = conn.recv(1024)
        print('Peer: ' + message.decode())
        # respond to the other peer success
        conn.send('success'.encode())
        conn.close()
        if message.decode() == 'exit':
            print('Peer has disconnected!')
            exit_chat()
            break


def send_messages():
    while True:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((peer, PORT2))
        message = input()
        client_socket.send(message.encode())
        print('\033[1A' + 'You: ' + message + '\033[K')
        # client_socket.close()
        if message == 'exit':
            client_socket.close()
            break


def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    while True:
        x = queue.get()
        if x == 1:
            listen_for_messages()
        if x == 2:
            send_messages()

        queue.task_done()


def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()


def exit_chat():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((peer, PORT2))
    client_socket.send('exit'.encode())
    client_socket.close()


create_workers()
create_jobs()
