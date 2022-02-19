import zmq


#aqui va a estar escuchando
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
r = socket.recv()
print(r)
socket.send_json({
    'hola' : 'todos'
})

socket_cliente = context.socket(zmq.REQ)
socket_cliente.connect("tcp://localhost:7777")
socket_cliente.send_string('hola soy el servidor, pero actuo como cliente')
r = socket_cliente.recv()
print(r)





