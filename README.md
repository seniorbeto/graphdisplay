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
para una mejor visualización. Cabe destacar que, únicamente es necesario especificar como argumento el grafo que se quiere representar pero además hay otros ajustes que pueden ser útiles a la hora de mostrar 
grafos grandes y complejos:
+ graph: es el objeto de tipo grafo que se va a representar **ES MUY IMPORTANTE** que el grafo que se introduce como argumento sea el implementado en base al código base de la asignatura. Si alguno
de los atributos cambiase de nombre, el programa no funcionaría correctamente. Para más información, consultar el [respositorio oficial de la asignatura](https://github.com/isegura/EDA) o utilizar la 
implementación de grafos que viene por defecto con el paquete.
+ node_radius: el radio de cada vértice del grafo, por defecto es 40 y puede tomar cualquier valor entero entre 10 y 100
+ scr_width: el tamaño en píxeles del ancho de la ventana, por defecto es 600 y puede tomar cualquier valor entero entre 200 y 1000
+ scr_width: el tamaño en píxeles de la altura de la ventana, por defecto es 600 y puede tomar cualquier valor entero entre 200 y 1000
+ theme: el tema de la ventana, por defecto es 'brown' y no voy a mencionarlos todos porque hay muchos y me da pereza.

Dicho esto, algunos ejemplos de uso podrían ser los siguientes:
```python
g = Graph([1, 2, 3])
g.addEdge(1, 2)
g.addEdge(2, 3)

# Para representar el grafo con todos los valores por defecto
GraphGUI(g)

# Para ajustar el radio de los nodos a 32, el ancho y largo de la pantalla a 700
GraphGUI(g, 32, 700, 700)

# Para ajustar únicamente el ancho de la pantalla a 200 píxeles
GraphGUI(g, scr_width=200)
```

Además, también es posible generar este tipo de grafos a través de la librería. Importándolo con `from graphdisplay import Graph`, se puede instanciar un objeto de tipo Graph, pasándole como
argumento una lista de los vértices del grafo para después, añadirle las aristas con el método `addEdge`, con los vértices que conecta la arista además del valor/coste de la arista.

## Funcionalidades
Como ya se ha mencionado, una de las principales características de la aplicación consiste en la posibilidad de mover los vértices del grafo dentro de la ventana. Además,
éstos conservarán su posición si se cierra la ventana y se vuelve a abrir. Así mismo, es posible abrir varias ventanas al mismo tiempo 
instaciando varios objetos de tipo GraphGUI en el mismo programa. Es por esto que el sistema de autoguardado depende de en qué parte del programa se generen estos objetos GraphGUI.
Por ejemplo, si se han generado dos grafos A y B y ha llamado primero al A y luego al B, si se vuelve a ejecutar el programa pero esta vez llamando primero al B, el sistema
tratará de cargar el último estado del grafo A en el B. Para evitar esto, es recomendable generar una guardado permanente (pulsando el botón save y nombrando el guardado) para
después poder cargarlo en cualquier momento.
## Ejemplo de uso

Para instanciar un grafo de tipo diccionario, se debe hacer de la siguiente manera: 

```python
labels = ['A', 'B', 'C', 'D', 'E']
g = Graph(labels)

# Now, we add the edges
g.addEdge('A', 'C', 12)  # A->(12)C
g.addEdge('A', 'D', 60)  # A->(60)D
g.addEdge('B', 'A', 10)  # B->(10)A
g.addEdge('C', 'B', 20)  # C->(20)B
g.addEdge('C', 'D', 32)  # C->(32)D
g.addEdge('E', 'A', 7)   # E->(7)A
g.addEdge('A', 'E', 50)  # A->(50)E
```

Si queremos mostrar la pantalla, basta con instanciar un objeto de tipo GraphGUI, pasándole como argumento el grafo que queremos mostrar: 

```python
    GraphGUI(g)
```
Y nos mostrará la ventana:

<img src="https://user-images.githubusercontent.com/94072018/236611009-de477dd9-d2dd-4247-80fa-dfc3e7a86a4b.png" width="400" height="400">

Sabiendo cómo instanciar grafos y reorganiando un poco los vértices, podemos ahora representar objetos algo más complicados ajustando un poco los parámetros de la instancia GraphGUI. En este caso: `GraphGUI(my_gragph, 25, 800, theme="ubuntu")`

<img src="https://user-images.githubusercontent.com/94072018/236917833-fa23fd9c-877f-43d8-9d03-2fd68fc6eb85.png" width="600" height="500">


