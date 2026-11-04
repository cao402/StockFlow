from datos import (STOCK_INICIAL, PEDIDOS, REPOSICIONES, NUM_TERMINALES, NUM_REVISORES, NUM_CAJAS)
import threading
import time

def pedidos():
    with semaforo:
        for pedido in PEDIDOS:
            for stock in STOCK_INICIAL:
                if pedido[1]==stock:
                        with lock:
                            if STOCK_INICIAL[stock]>=pedido[2]:
                                STOCK_INICIAL[stock]-=pedido[2]
                            break 
        print("Caja terminada")
        print(f"Numero de espacios disponibles en el semaforo: {semaforo._value}")    
        

hilos=[]
lock = threading.Lock()
semaforo = threading.Semaphore(NUM_TERMINALES)

for _ in range(NUM_CAJAS):
    hilo = threading.Thread(
        target=pedidos, args=(),
    )
    hilos.append(hilo)

for i in hilos:
    i.start()
