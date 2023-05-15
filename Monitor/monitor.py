import grpc
import messages_pb2
import messages_pb2_grpc
import accesoAWS
import random
from clases_ec2 import Manager
from google.protobuf.json_format import MessageToDict

#comando para proto: python -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. messages.proto

uso = []

def monitor():
  global uso

  if not manager.pool:
    for i in range(2):
      manager.crearInstanciaEC2('ami-0b6c5e19de6b71814')
  else:
    for instancia in manager.pool:
      try:
        conexionInstancia = gRPC(manager.pool[instancia][1], 'EstaVivo')
        uso.append(conexionInstancia.usoCPU)
      except:
        conexionInstancia = 'EstaMuerto'   

    promedioUso = sum(uso)/len(uso)

    if promedioUso >= 70:
      manager.crearInstanciaEC2(accesoAWS.ami_template)
      for instancia in manager.pool:
        try:
          conexionInstancia = gRPC(manager.pool[instancia][1], 'Evento')
        except:
          conexionInstancia = 'EstaMuerto'

    if promedioUso <= 20:
      tupla = random.choice(manager.pool)
      IP = tupla[1]
      manager.eliminarInstanciaEC2(IP)
      for instancia in manager.pool:
        try:
          conexionInstancia = gRPC(manager.pool[instancia][1], 'Evento')
        except:
          conexionInstancia = 'EstaMuerto'

def gRPC(IP, peticion):
  channel = grpc.insecure_channel(f'{IP}:8080')
  stub = messages_pb2_grpc.messageServiceStub(channel)
  response = stub.message(messages_pb2.instructionRequest(estado = peticion))
  response  = MessageToDict(response)
  return response

if __name__ == "__main__":
  manager = Manager()
  while True:
    monitor()