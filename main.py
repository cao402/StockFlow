from datos import (STOCK_INICIAL, PEDIDOS, REPOSICIONES, NUM_TERMINALES, NUM_REVISORES, NUM_CAJAS)
import threading
import time
from random import randint

class GestorInventario:
    def __init__(self, stock_inicial, reposiciones):
        self.stock = stock_inicial
        self.reposiciones = reposiciones
        self.lock = threading.RLock()
        self.condition = threading.Condition(self.lock)

    def reponer_stock(self, producto):
        with self.lock:
            for repuesto in self.reposiciones:
                if repuesto[1] == producto:
                    self.stock[producto] += repuesto[2]
                    break
            self.condition.notify_all()

    def reducir_stock(self, producto, cantidad):
        with self.lock:
            if self.stock[producto] < cantidad:
                hilo_reposicion = threading.Thread(target=self.ejecutar_reposicion, args=(producto,))
                hilo_reposicion.start()
                while hilo_reposicion.is_alive():
                    self.condition.wait()
            
            self.stock[producto] -= cantidad

    def ejecutar_reposicion(self, producto):
        with self.lock:
            self.reponer_stock(producto)

inventario = GestorInventario(STOCK_INICIAL, REPOSICIONES)

def pedidos():
    with semaforo:
        for pedido in PEDIDOS:
            inventario.reducir_stock(pedido[1], pedido[2])
        print("Caja terminada")
        print(f"Numero de espacios disponibles en el semaforo: {semaforo._value}")    
    print()
                    
def revision():
    tiempo_espera=randint(2,5)
    print(f"{threading.current_thread().name} espera de {tiempo_espera}")
    time.sleep(tiempo_espera)
    barrera.wait()
    print("Se termino la revision de todos los datos")

hilos=[]
hilos_revison=[]
barrera = threading.Barrier(NUM_REVISORES)
semaforo = threading.Semaphore(NUM_TERMINALES)

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