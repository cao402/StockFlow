from datos import (STOCK_INICIAL, PEDIDOS, REPOSICIONES, NUM_TERMINALES, NUM_REVISORES, NUM_CAJAS)
import threading
import time
from random import randint

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
    print()

def reposicion(dato):
    with condition:
        for repuesto in REPOSICIONES:
            if repuesto[1]==dato:
                STOCK_INICIAL[dato]+=repuesto[2]
                break
        condition.notify_all()
                    
def revision():
    tiempo_espera=randint(2,5)
    print(f"{threading.current_thread().name} espera de {tiempo_espera}")
    time.sleep(tiempo_espera)
    barrera.wait()
    print("Se termino la revision de todos los datos")



hilos=[]
hilos_revison=[]
barrera = threading.Barrier(NUM_REVISORES)
lock = threading.Lock()
semaforo = threading.Semaphore(NUM_TERMINALES)
condition = threading.Condition()

for _ in range(NUM_CAJAS):
    hilo = threading.Thread(
        target=pedidos, args=(),
    )
    hilos.append(hilo)

for i in range(NUM_REVISORES):
    hilo = threading.Thread(
        target=revision, args=(), name=f"Revision - {i+1}:"   
    )
    hilos_revison.append(hilo)

for i in hilos:
    i.start()

for i in hilos:
    i.join()

for i in hilos_revison:
    i.start()