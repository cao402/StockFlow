from datos import (STOCK_INICIAL, PEDIDOS, REPOSICIONES, NUM_TERMINALES, NUM_REVISORES, NUM_CAJAS)
import threading
import time

def pedidos():

    with semaforo:
        for pedido in PEDIDOS:
            for stock in STOCK_INICIAL:
                if pedido[1]==stock:
                    with condition:
                        if STOCK_INICIAL[stock]<pedido[2]:
                            hilo_reposicion =  threading.Thread(target=reposicion, args=(stock,),)
                            hilo_reposicion.start()
                            while hilo_reposicion.is_alive():
                                condition.wait()
                        STOCK_INICIAL[stock]-=pedido[2]
                        break 
        print("Caja terminada")
        print(f"Numero de espacios disponibles en el semaforo: {semaforo._value}")    

def reposicion(dato):
    with condition:
        for repuesto in REPOSICIONES:
            if repuesto[1]==dato:
                STOCK_INICIAL[dato]+=repuesto[2]
                break
        condition.notify_all()
                    

hilos=[]
lock = threading.Lock()
semaforo = threading.Semaphore(NUM_TERMINALES)
condition = threading.Condition()

for _ in range(NUM_CAJAS):
    hilo = threading.Thread(
        target=pedidos, args=(),
    )
    hilos.append(hilo)


for i in hilos:
    i.start()
