# Imports
import time
import socket
import threading

# host and port variables

HOST = '127.0.0.1'

PORT = 1234 # you can use any port between 0 to 65535

LISTNER_LIMIT = 5

active_clients = [] # list of all connected clients

# function to keep on listening for messages

def listen_to_messages(client, username):
    
    # listen for messages
    while True:
        try:
            msg = client.recv(2048).decode('utf-8')
            if msg != '':

                final_msg = username + '~' + msg 
                send_msg_all(final_msg)

            else:
                print(f"Message is empty from client : {username}")
        except:
            print("Something went wrong")


# function to send message to a single client

def send_msg_to_client(client, message):

    client.sendall(message.encode())

# function to send messeges to all connected clients

def send_msg_all(msg):

    for user in active_clients:

        # using user[1] to get the client object from the list of tuples
        send_msg_to_client(user[1], msg)

# function to handle clients

def client_handler(client):
    # server will listen for client messeges that will have a username and message
    while True:

        username = client.recv(2048).decode('utf-8')  # recv is used to recieve the msg and 2048 is max size

        if username != '':
            active_clients.append((username, client))
            prompt_message = "SERVER~" + f"{username} added to the chat"
            send_msg_all(prompt_message)
            break
        else:
            print("Client username is empty")

    threading.Thread(target=listen_to_messages, args=(client, username, )).start()




# main function

def main():
    # creating the sockett class object
    # AF_INET : using IPv4 addresses
    # SOCK_STREAM : for using TCP packets for communication
    # SOCK_DGRAM : for using UDM protocol
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # creating a try catch block

    try:
        # provide the server with an address in form of HOST id and PORT
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")

    # set server limit
    server.listen(LISTNER_LIMIT)

    # Creating a while to listen to client connection
    while True:
        client, address = server.accept()  # address is a tuple in form (HOST,PORT)
        print(f"Successfully connected to client {address[0]} {address[1]}" )


        # using threading to conccurently run the client_handler fuction

        threading.Thread(target=client_handler, args=(client, )).start()


if __name__ == "__main__":
    main()

