import grpc
import messages_pb2
import messages_pb2_grpc
import random
from concurrent import futures

valorInicial = 30

class messageService(messages_pb2_grpc.messageServiceServicer):
    def message(self, request, context):
        if request.estado == 'EstaVivo':
            CPU = usoCPU()
            return messages_pb2.messageResponse(respuesta = "estoyVivo", usoCPU = CPU)

def usoCPU():
    # 0 significa que la CPU va a disminuir
    # 1 significa que la CPU va a aumentar
    global valorInicial
    opcion = random.randint(0, 1)

    if valorInicial > 0 and valorInicial < 100:
        if opcion == 0:
            valorInicial -= 1
        else:
            valorInicial += 1
    else:
        valorInicial = 30
    return valorInicial

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    messages_pb2_grpc.add_messageServiceServicer_to_server(messageService(), server)
    server.add_insecure_port(f'[::]:8080')
    server.start()
    server.wait_for_termination()