# graphdisplay

## Resumen

graphdisplay es un paquete de python elaborado e ideado por Alberto Penas Díaz, cuya finalidad es facilitar la visualización de grafos a los alumnos de Estructuras de Datos y Algoritmos. 
Actualmente solo soporta la visualización de grafos implementados a través de un diccionario, tal y como se aportan como código base en la asignatura. 

## Método de uso 

Para instalar la librería, basta con escribir el siguiente comando en la terminal: `pip install graphdisplay`, con esta, se instalarán también otras dependencias, ya sean las librerías 
tkinter y math (que muchas veces vienen instaladas por defecto en python). 

Una vez instalado, se debe importar el paquete desde donde se esté trabajando con: `from graphdisplay import GraphGUI`. Una vez hecho esto, se debe instanciar un grafo de tipo diccionario
para finalmente introducirlo como argumento al instanciar un objeto de tipo GraphGUI, el cual mostrará en una ventana el grafo y ofrecerá la posibildad de mover los vértices con el ratón 
para una mejor visualización. 

Además, también es posible generar este tipo de grafos a través de la librería. Importándolo con `from graphdisplay import Graph`, se puede instanciar un objeto de tipo Graph, pasándole como
argumento una lista de los vértices del grafo para después, añadirle las aristas con el método `add_edge`, con los vértices que conecta la arista además del valor/coste de la arista.

## Ejemplo de uso

Para instanciar un grafo de tipo diccionario, se debe hacer de la siguiente manera: 

```python
labels = ['A', 'B', 'C', 'D', 'E']
    g = Graph(labels)

    # Now, we add the edges
    g.add_edge('A', 'C', 12)  # A->(12)C
    g.add_edge('A', 'D', 60)  # A->(60)D
    g.add_edge('B', 'A', 10)  # B->(10)A
    g.add_edge('C', 'B', 20)  # C->(20)B
    g.add_edge('C', 'D', 32)  # C->(32)D
    g.add_edge('E', 'A', 7)   # E->(7)A
    g.add_edge('A', 'E', 50)  # A->(50)E
```

Si queremos mostrar la pantalla, basta con instanciar un objeto de tipo GraphGUI, pasándole como argumento el grafo que queremos mostrar: 

```python
    GraphGUI(g)
```
Y nos mostrará la ventana:

![image](https://user-images.githubusercontent.com/94072018/236173093-6d07ad94-0c74-4f00-ac2f-13fb797a2837.png)

A la cual, reorganizando los vértices, podemos llegar a la siguiente imagen (mucho más legible):
![image](https://user-images.githubusercontent.com/94072018/236172922-ae836f24-1131-4e83-baa8-cdda8e333989.png)
