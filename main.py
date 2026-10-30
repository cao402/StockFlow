from datos import (STOCK_INICIAL, PEDIDOS, REPOSICIONES, NUM_TERMINALES, NUM_REVISORES, NUM_CAJAS)
import threading

def pedidos():
    for pedido in PEDIDOS:
        for stock in STOCK_INICIAL:
            if pedido[1]==stock:
                if STOCK_INICIAL[stock]>=pedido[2]:
                    STOCK_INICIAL[stock]-=pedido[2]
                break 
    print("Caja terminada")

hilos=[]

for _ in range(NUM_CAJAS):
    hilo = threading.Thread(
        target=pedidos, args=(),
    )
    hilos.append(hilo)

for i in hilos:
    i.start()

