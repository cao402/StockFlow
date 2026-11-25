from datosviejo import (STOCK_INICIAL, PEDIDOS, REPOSICIONES, NUM_TERMINALES, NUM_REVISORES, NUM_CAJAS)
import threading
import time

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
    global resumen_cajas
    global momento_parada
    pedidos_antes=[]
    pedidos_en_curso=[]
    pedidos_tras=[]

    with semaforo:
        for pedido in PEDIDOS:
            if parada.is_set()==False:
                momento_parada=False
                pedidos_en_curso.append(pedido[0])
            parada.wait()

            inventario.reducir_stock(pedido[1], pedido[2])
            print("pedido hecho")    
            time.sleep(0.1)        

            if momento_parada:
                pedidos_antes.append(pedido[0])
            else:
                pedidos_tras.append(pedido[0])

        print("Caja terminada")
        print(f"Numero de espacios disponibles en el semaforo: {semaforo._value}")   
    print()
    resumen_cajas[threading.current_thread().name]=[pedidos_antes, pedidos_en_curso, pedidos_tras]

def revision():
    print(f"{threading.current_thread().name} espera de {1}")
    time.sleep(1)
    barrera.wait()
    print("Se termino la revision de todos los datos")

def controlador():
        time.sleep(3)
        parada.clear()
        print("Se inicia el evento parada")
        time.sleep(4)
        print("se reanudo los pedidos")
        parada.set()

resumen_cajas={}
hilos=[]
hilos_revison=[]
barrera = threading.Barrier(NUM_REVISORES)
semaforo = threading.Semaphore(NUM_TERMINALES)
parada=threading.Event()
parada.set()
momento_parada=True


for i in range(NUM_CAJAS):
    hilo = threading.Thread(
        target=pedidos, args=(), name=f"Caja {i+1}"
    )
    hilos.append(hilo)

for i in range(NUM_REVISORES):
    hilo = threading.Thread(
        target=revision, args=(), name=f"Revision - {i+1}:"   
    )
    hilos_revison.append(hilo)

hilo_controlador=threading.Thread(
        target=controlador, args=(),   
    )

for i in hilos:
    i.start()

hilo_controlador.start()

for i in hilos:
    i.join()

total=0
antes=0
mientras=0
tras=0
for caja in resumen_cajas:
    numero_pedidos=0
    texto=f"{caja}  "
    for pedido in range(len(resumen_cajas[caja])):
        texto+=f"{len(resumen_cajas[caja][pedido])} * "

        if pedido==0:
            antes+=len(resumen_cajas[caja][pedido])
        elif pedido==1:
            mientras+=len(resumen_cajas[caja][pedido])
        elif pedido==2:
            tras+=len(resumen_cajas[caja][pedido])

        for mini_pedido in resumen_cajas[caja][pedido]:
            texto+=f"{mini_pedido}, "
            numero_pedidos+=1
        texto+="    "
    texto+=f"{numero_pedidos}"
    total+=numero_pedidos
    print(texto)

print(f"""
        Antes       El curso al puasar      Tras reaudar    Total
TOTAL   {antes}         {mientras}                       {tras}              {total}""")

for i in hilos_revison:
    i.start()