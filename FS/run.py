from encodings import utf_8
import socket
from flask import Flask
from flask import request

app = Flask(__name__)
_host_ = '0.0.0.0'
_port_ = 9090
bufferSize = 1024

@app.route('/')
def hello_world():
    return 'Fibonacci Server'

# @app.route('/register', methods=['PUT'])
@app.route('/register')
def register():
  # hostname = request.form.get('hostname')
  # ip = request.form.get('ip')
  # as_ip = request.form.get('as_ip')
  # as_port = request.form.get('as_port')
  hostname = request.args.get('hostname')
  ip = request.args.get('ip')
  as_ip = request.args.get('as_ip')
  as_port = request.args.get('as_port')

  # Create a UDP socket on client
  UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
  # Send message to server using created socket
  message = (
    "TYPE=A\n"
    "NAME=" + hostname + "\n"
    "VALUE=" + ip + "\n"
    "TTL=10\n"
  )
  print("Sending message to authoritative server: " + message)
  UDPClientSocket.sendto(str.encode(message), (as_ip, int(as_port)))

  msgFromServer = UDPClientSocket.recvfrom(bufferSize)
  msg = str(msgFromServer[0], 'utf-8')
  print("Received message from authoritative server: " + msg)

  return msg, 201

@app.route('/fibonacci')
def fibonacci():
  number = request.args.get('number')
  try:
    number = int(number)
    return str(get_fib_num(number)), 200
  except ValueError:
    return 'Invalid input: Please provide a number', 400

# Function for nth Fibonacci number
def get_fib_num(n):

    # Check if input is 0 then it will
    # print incorrect input
    if n < 0:
        print("Incorrect input")

    # Check if n is 0
    # then it will return 0
    elif n == 0:
        return 0

    # Check if n is 1,2
    # it will return 1
    elif n == 1 or n == 2:
        return 1

    else:
        return get_fib_num(n-1) + get_fib_num(n-2)

app.run(host=_host_,
        port=_port_,
        debug=True)