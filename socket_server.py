import socket
import json
from datetime import datetime

data = {}

def save_message(message):
    timestamp = message['timestamp']
    data[timestamp] = {
        "username": message['username'],
        "message": message['message']
    }
    with open('front-init/storage/data.json', 'w') as f:
        json.dump(data, f)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('localhost', 5000))

    while True:
        message, addr = sock.recvfrom(1024)
        message_data = json.loads(message.decode('utf-8'))
        save_message(message_data)

if __name__ == '__main__':
    main()
