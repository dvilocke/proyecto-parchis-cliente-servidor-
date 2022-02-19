import zmq


#aqui va a estar mandando
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

socket.send_string('hola desde el cliente')
r = socket.recv()
print(r['hola'])

#cambiemos los papeles

socket_servidor = context.socket(zmq.REP)
socket_servidor.bind('tcp://*:7777')

r = socket_servidor.recv()
print(r)
socket_servidor.send_string('hola soy el cliente, pero me volvi servidor')
