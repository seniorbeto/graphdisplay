# graphdisplay

## Resumen

graphdisplay es un paquete de python elaborado e ideado por Alberto Penas Díaz, cuya finalidad es facilitar la visualización de grafos a los alumnos de Estructuras de Datos y Algoritmos. 
Actualmente solo soporta la visualización de grafos implementados a través de un diccionario, tal y como se aportan como código base en la asignatura. 

## ¿Quieres contribuir?

Este es un proyecto de código abierto hecho por y para estudiantes así que cualquier ayuda, comentario o sugerencia es bienvenido. La mejor manera de contribuir es añadir los bugs que os encontréis 
en el apartado de Issues pero también estoy completamente abierto a responder cualquier duda o ayuda desde mi correo personal (disponible en mi perfil de github). ¡Muchas gracias de antemano!

## Método de uso 

Para instalar la librería, basta con escribir el siguiente comando en la terminal: `pip install graphdisplay`, con esta, se instalarán también otras dependencias, ya sean las librerías 
tkinter y math (que muchas veces vienen instaladas por defecto en python). 

Una vez instalado, se debe importar el paquete desde donde se esté trabajando con: `from graphdisplay import GraphGUI`. Una vez hecho esto, se debe instanciar un grafo de tipo diccionario
para finalmente introducirlo como argumento al instanciar un objeto de tipo GraphGUI, el cual mostrará en una ventana el grafo y ofrecerá la posibildad de mover los vértices con el ratón 
para una mejor visualización. **Al desplazar los vértices por la pantalla y fijar su posición, si se cierra la ventana y se vuelve a abrir, el grafo seguirá con la forma con la que se ha movido
antes.**. Cabe destacar que, únicamente es necesario especificar como argumento el grafo que se quiere representar pero además hay otros ajustes que pueden ser útiles a la hora de mostrar 
grafos grandes y complejos:
+ graph: es el objeto de tipo grafo que se va a representar 
+ node_radius: el radio de cada vértice del grafo, por defecto es 40 y puede tomar cualquier valor entero entre 10 y 100
+ scr_width: el tamaño en píxeles del ancho de la ventana, por defecto es 600 y puede tomar cualquier valor entero entre 200 y 1000
+ scr_width: el tamaño en píxeles de la altura de la ventana, por defecto es 600 y puede tomar cualquier valor entero entre 200 y 1000

Dicho esto, algunos ejemplos de uso podrían ser los siguientes:
```python
g = Graph([1, 2, 3])
g.add_edge(1, 2)
g.add_edge(2, 3)

# Para representar el grafo con todos los valores por defecto
GraphGUI(g)

# Para ajustar el radio de los nodos a 32, el ancho y largo de la pantalla a 700
GraphGUI(g, 32, 700, 700)

# Para ajustar únicamente el ancho de la pantalla a 200 píxeles
GraphGUI(g, scr_width=200)
```

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

<img src="https://user-images.githubusercontent.com/94072018/236611009-de477dd9-d2dd-4247-80fa-dfc3e7a86a4b.png" width="400" height="400">

Sabiendo cómo instanciar grafos, podemos ahora representar objetos algo más complicados ajustando un poco los parámetros de la instancia GraphGUI. En este caso: `GraphGUI(my_gragph, 30, 1000, 1000)`

<img src="https://user-images.githubusercontent.com/94072018/236611227-2b812c07-7eac-4922-85a5-17cb6e13daea.png" width="550" height="550">

