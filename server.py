import socket
import select

HEADER_LENGTH = 10
HOST = ('localhost', 10000)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind(HOST)
server.listen()
print('listening')

sockets_list = [server]
clients_list = {}


def receive_msg(client: socket.socket):
    try:
        msg_header = client.recv(HEADER_LENGTH)
        if not len(msg_header):
            return False

        msg_length = int(msg_header.decode('UTF-8').strip())
        return {
            'header': msg_header,
            'data': client.recv(msg_length),
        }

    except:
        return False


while True:
    rs, _, es = select.select(sockets_list, [], sockets_list)
    for _socket in sockets_list:
        if _socket == server:
            client, addr = server.accept()
            user = receive_msg(client)
            if user is False:
                continue
            sockets_list.append(client)
            clients_list[client] = user
            data = user['data']
            print(f'new connection from {addr} with {data.decode("UTF-8")}')

        else:
            msg = receive_msg(client)
            print(msg)
            if msg is False:
                print(f'connection from {addr} has been interrupted')
                sockets_list.remove(_socket)
                del clients_list[_socket]
                continue

            user = clients_list[_socket]

            for client in clients_list:
                if client is not _socket:
                    client.send(user["header"]+user["data"]+msg["header"]+msg["data"])

        for _socket in es:
            sockets_list.remove(_socket)
            del clients_list[_socket]


