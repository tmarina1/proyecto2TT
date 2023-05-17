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
      try:
        manager.crearInstanciaEC2(accesoAWS.ami_template)
        manager.verPool()
      except:
        conexionInstancia = 'Error en  creacción instancias iniciales'
  else:
    for instancia in manager.pool:
      try:
        conexionInstancia = gRPC(instancia[1], 'EstaVivo')
        uso.append(conexionInstancia["usoCPU"])
      except:
        conexionInstancia = 'Error en envio de EstaVivo a instancia'   
    if uso:
        promedioUso = sum(uso)/len(uso)
        print(promedioUso)
        uso = []

        if promedioUso >= 70:
          print('creando')
          manager.crearInstanciaEC2(accesoAWS.ami_template)
          manager.verPool()
          for instancia in manager.pool:
            try:
              conexionInstancia = gRPC(instancia[1], 'Evento')
              print(conexionInstancia)
            except:
              conexionInstancia = 'Error en envio de evento crear instancia'
              print(conexionInstancia)
        if promedioUso < 19:
          if len(manager.pool) == 2:
              for instancia in manager.pool:
                try:
                  conexionInstancia = gRPC(instancia[1], 'Evento')
                except:
                  conexionInstancia = 'Error en envio de evento'
          else:
            print('borrando')
            tupla = random.choice(manager.pool)
            IDinstancia = tupla[0]
            manager.eliminarInstanciaEC2(IDinstancia)
            valTupla = manager.pool.index(tupla)
            manager.pool.pop(valTupla)
            manager.verPool()
            for instancia in manager.pool:
              try:
                conexionInstancia = gRPC(instancia[1], 'Evento')
              except:
                conexionInstancia = 'Error en envio de evento eliminar instancia'
                print(conexionInstancia)

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