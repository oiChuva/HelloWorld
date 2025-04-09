from queue import Queue
from arq_consultar_equipamento import consultar_equipamento

queue = Queue()

def process_queue():
    while True:
        numero_serie = queue.get()
        result = consultar_equipamento(numero_serie)
        if 'error' not in result:
            # Não faz nada aqui, porque o email já é enviado na função consultar_equipamento
            pass
            queue.task_done()