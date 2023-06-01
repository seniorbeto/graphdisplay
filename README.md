<p align="center">
  <img width="200" src="https://github.com/seniorbeto/graphdisplay/assets/94072018/181477f3-b0e5-4efd-8e4f-2e7bad5c4d66" alt="logo">
  <h1 align="center" style="margin: 0 auto 0 auto;">GraphDisplay</h1>
  <h4 align="center" style="margin: 0 auto 0 auto;">An intuitive GUI for visualizing graphs</h4>
</p>

## 💡Resumen

graphdisplay es un paquete de python elaborado e ideado por Alberto Penas Díaz, cuya finalidad es facilitar la visualización de grafos y árboles a los alumnos de Estructuras de Datos y Algoritmos. 

## ⚡️¿Quieres contribuir?

Este es un proyecto de código abierto hecho por y para estudiantes así que cualquier ayuda, comentario o sugerencia es bienvenido. La mejor manera de contribuir es añadir los bugs que os encontréis 
en el apartado de Issues pero también estoy completamente abierto a responder cualquier duda o ayuda desde mi correo personal (disponible en mi perfil de github). ¡Muchas gracias de antemano!

## 📐Método de uso

Para instalar la librería, basta con escribir el siguiente comando en la terminal: `pip install graphdisplay`, con esta, se instalarán también otras dependencias, ya sean las librerías 
tkinter y math (que muchas veces vienen instaladas por defecto en python). 

Una vez instalado, se debe importar el paquete desde donde se esté trabajando con: `from graphdisplay import GraphGUI`. La librería también incluye la implementación oficial de grafos y árboles de la 
asignatura, por lo que también son importables.
Una vez instalada, se debe instanciar un grafo o árbol para finalmente introducirlo como argumento al generar un objeto de tipo GraphGUI, el cual mostrará en una ventana el grafo y ofrecerá la posibildad de mover los vértices con el ratón. 
Junto con el grafo, el resto de argumentos son los siguientes: 
+ graph: es el objeto de tipo grafo/árbol que se va a representar **ES MUY IMPORTANTE** que éste sea implementado en base al código base de la asignatura. Si alguno
de los atributos de las clases cambiase de nombre, es muy probable que el programa no funcionara correctamente. Para más información, consultar el [respositorio oficial de la asignatura](https://github.com/isegura/EDA) o utilizar la implementación de grafos que viene por defecto con el paquete.
+ node_radius: el radio de cada vértice del grafo, por defecto es 40 y puede tomar cualquier valor entero entre 10 y 100
+ theme: el tema de la ventana, por defecto es 'brown' y no voy a mencionarlos todos porque hay muchos.

Dicho esto, algunos ejemplos de uso podrían ser los siguientes:
```python
from graphdisplay import GraphGUI, Graph

g = Graph([1, 2, 3])
g.addEdge(1, 2)
g.addEdge(2, 3)

# Para representar el grafo con todos los valores por defecto
GraphGUI(g)

# Para ajustar el radio de los nodos a 32, y el tema a 'dark'
GraphGUI(g, node_radius=32, theme='dark')
```
Ejemplo con árboles binarios de búsqueda:
```python
from graphdisplay import GraphGUI, BinarySearchTree
from random import randint

tree = BinarySearchTree()
for _ in range(80):
    tree.insert(randint(1, 1000))
   
GraphGUI(tree)
```

## ⚡️Funcionalidades
Como ya se ha mencionado, una de las principales características de la aplicación consiste en la posibilidad de mover los vértices del grafo dentro de la ventana. Además,
éstos conservarán su posición si se cierra la ventana y se vuelve a abrir. Así mismo, es posible abrir varias ventanas al mismo tiempo 
instanciando varios objetos de tipo GraphGUI en el mismo programa. Es por esto que el sistema de autoguardado depende de en qué parte del programa se generen estos objetos GraphGUI.
Por ejemplo, si se han generado dos grafos A y B y ha llamado primero al A y luego al B, si se vuelve a ejecutar el programa pero esta vez llamando primero al B, el sistema
tratará de cargar el último estado del grafo A en el B. Para evitar esto, es recomendable generar una guardado permanente (pulsando el botón save y nombrando el guardado) para
después poder cargarlo en cualquier momento.

Cabe destacar además, que las funcionalidades han sido testeadas únicamente en linux y en windows, variando las funcionalidades de la aplicación entre los sitemas. Por ejemplo,
al generar un objeto GraphGUI en windows, si no se ha instanciado dentro de la cláusula `if __name__ == "__main__":` saltará un _Warning_, cosa que no pasará en Linux. Por otra parte,
Windows permite generar sub-árboles presionando con el click derecho del ratón en un vértice (dicho árbol se generará en una nueva ventana), funcionalidad que no está disponible en linux debido al 
issue #16
## 🎯Ejemplos de uso

Para instanciar un grafo de tipo diccionario, se debe hacer de la siguiente manera: 

```python
from graphdisplay import GraphGUI, Graph

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

<img src="https://github.com/seniorbeto/graphdisplay/assets/94072018/0abc6d79-120e-470f-8d9b-7035e38def40" width="400" height="400">

Sabiendo cómo instanciar grafos y reorganiando un poco los vértices, podemos ahora representar objetos algo más complicados ajustando un poco los parámetros de la instancia GraphGUI. En este caso: `GraphGUI(my_gragph, 25, theme="la gran ola")`

<img src="https://github.com/seniorbeto/graphdisplay/assets/94072018/a1edfcbf-4cec-4b08-98c6-709b87b7892d" width="800" height="500">

De la misma manera, un ejemplo de display de un árbol binario de búsqueda: 

<img src="https://github.com/seniorbeto/graphdisplay/assets/94072018/3afa798a-28c3-4c6f-9357-8d849018dfa5" width="1000" height="480">
