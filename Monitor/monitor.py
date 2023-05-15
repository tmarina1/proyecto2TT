import grpc
import messages_pb2
import messages_pb2_grpc
import accesoAWS
import random
from clases_ec2 import Manager
from google.protobuf.json_format import MessageToDict

#comando para proto: python -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. messages.proto

def monitor():
  manager = Manager(1, 1)

  if manager.pool is None:
    for i in range(2):
      manager.crearInstanciaEC2('ami-0b6c5e19de6b71814')

  for instancias in manager.pool:
    try:
      conexionInstancia = gRPC(manager.pool[instancias][1])
    except:
      conexionInstancia = 'EstaMuerto'   

  if manager.promedioUsoCPU > 60:
    manager.crearInstanciaEC2(accesoAWS.ami_template)

  if manager.promedioUsoCPU < 20:
    tupla = random.choice(manager.pool)
    IP = tupla[1]
    manager.eliminarInstanciaEC2(IP)

def gRPC(IP):
  channel = grpc.insecure_channel(f'{IP}:8080')
  stub = messages_pb2_grpc.messageServiceStub(channel)
  response = stub.message(messages_pb2.instructionRequest(estado = 'EstaVivo'))
  response  = MessageToDict(response)
  return response

if __name__ == "__main__":
  monitor()