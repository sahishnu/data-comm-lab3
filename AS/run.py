import socket
from socketserver import UDPServer
from flask import Flask

app = Flask(__name__)
_host_ = '0.0.0.0'
_port_ = 53533
bufferSize = 1024

# Create a UDP socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address & ip
UDPServerSocket.bind((_host_, _port_))

print("Server is configured to listen on port: " + str(_port_))

# Listen for incoming datagrams
while(True):
  bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
  message = bytesAddressPair[0]
  address = bytesAddressPair[1]
  msg = str(message, 'utf-8')

  print(msg)
  fields = msg.split('\n')
  value = None
  for field in fields:
    if field.startswith('TYPE'):
      type = field.split('=')[1]
    elif field.startswith('NAME'):
      name = field.split('=')[1]
    elif field.startswith('VALUE'):
      value = field.split('=')[1]
    elif field.startswith('TTL'):
      ttl = field.split('=')[1]

  # this is if querying for a name
  if value is None:
    print('Querying for NAME: ' + name)
    try:
      with open(name + '.txt', 'r') as f:
        fileContents = f.readlines()
        queryAnswer = '\n'.join(fileContents)
        # Send reply to client
        UDPServerSocket.sendto(str.encode(queryAnswer), address)
    except FileNotFoundError:
      print('File not found: ' + name)
      UDPServerSocket.sendto(
        str.encode("Error: " + name + ', not found'),
      address)

  # this is registering a value
  else:
    print('Registering NAME: ' + name + ', VALUE: ' + value)
    with open(name + '.txt', 'w') as f:
      for field in fields:
        f.write(field + '\n')
    # Send reply to client
    UDPServerSocket.sendto(
      str.encode("Succesfully registered" + name + ', value ' + value),
    address)

