import grpc
import messages_pb2
import messages_pb2_grpc
import accesoAWS
from clases_ec2 import Manager
from google.protobuf.json_format import MessageToDict

#comando para proto: python -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. messages.proto


def monitor():
  hola = gRPC('54.204.115.132', 'EstaVivo')
  print(hola)

def gRPC(IP, peticion):
  channel = grpc.insecure_channel(f'{IP}:8080')
  stub = messages_pb2_grpc.messageServiceStub(channel)
  response = stub.message(messages_pb2.instructionRequest(estado = peticion))
  response  = MessageToDict(response)
  return response

if __name__ == "__main__":
  monitor()