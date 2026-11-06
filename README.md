# StockFlow

El programa sirve para tomar un stock y ir haciendo peticiones para modificar el stock si llega el stock a vaciarse se repondra, al finalizar se haran 4 revisiones del stock.

El programa se ejecuta automaticamente, al iniciarlo se genera todo.

Tenemos 2 archivos, que seria datos.py donde se encuentran el stock, las peticiones, los repuestos y por ultimo a cantidad de cajas a llenar, de revisar y relleacion de cajas.

Una condicion de carrera ocurre cuando multiples hilos intentan acceder y modificar un mismo recurso compartido de forma simultanea sin la debida coordinacion, provocando que el resultado final dependa del orden impredecible de ejecucion de los hilos.

El proyecto utiliza varias primitivas de sincronizacion provistas por el modulo threading de Python para controlar la concurrencia:
Un Lock asegura que solo un hilo a la vez pueda acceder a una seccion critica de codigo.
El RLock es una variante del Lock que permite a un mismo hilo adquirir el candado multiples veces sin bloquearse a si mismo.
El Condition se utiliza asociada al RLock para permitir que los hilos se suspendan a la espera de que ocurra un evento o cambio de estado.
El Semaphore limita el numero de hilos que pueden acceder a un recurso delimitado en paralelo.
La Barrier permite establecer un punto de sincronizacion colectiva donde un grupo de hilos debe detenerse hasta que todos hayan alcanzado dicho punto.

La refactorizacion con el rlock es necesario porque que un mismo hilo adquiera el mismo cerrojo varias veces.

Un deadlock o interbloqueo es una situacion en la que dos o mas hilos quedan bloqueados indefinidamente esperando mutuamente recursos que los otros hilos poseen. En este programa existe un riesgo potencial de interbloqueo en el metodo reducir_stock. 