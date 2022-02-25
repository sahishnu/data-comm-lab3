import socket, requests
from flask import Flask
from flask import request

app = Flask(__name__)
_host_ = '0.0.0.0'
_port_ = 8080
bufferSize = 1024

@app.route('/')
def hello_world():
    return 'User Server'

@app.route('/fibonacci')
def fibonacci():
    # hostname & port of fib server to query
    hostname = request.args.get('hostname', default=None, type=str)
    fs_port = request.args.get('fs_port', default=None, type=str)
    # fib seq number to query
    seq_number = request.args.get('number', default=None, type=str)
    # authoritative server ip & port to query
    as_ip = request.args.get('as_ip', default=None, type=str)
    as_port = request.args.get('as_port', default=None, type=str)

    if hostname is None or fs_port is None or seq_number is None or as_ip is None or as_port is None:
        return 'Invalid request', 400

    # Create a UDP socket on client
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # Send message to server using created socket
    message = (
        "TYPE=A\n"
        "NAME=" + hostname + "\n"
    )
    print("Sending message to authoritative server: " + message)
    UDPClientSocket.sendto(str.encode(message), (as_ip, int(as_port)))

    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msg = str(msgFromServer[0], 'utf-8')
    print("Received message from authoritative server:\n" + msg)
    fields = msg.split('\n')
    for field in fields:
        if field.startswith('VALUE'):
            value = field.split('=')[1]
            answer = requests.get('http://' + value + ':' + fs_port + '/fibonacci?number=' + seq_number)
            print(answer.text)
            return 'Fibonacci(' + seq_number + ') = ' + answer.text, 200

    return msg, 200

app.run(host=_host_,
        port=_port_,
        debug=True)