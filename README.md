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
asignatura, por lo que también son importables (`from graphdisplay import BinarySearchTree, Graph, GraphGUI, AVLTree`).
Una vez instalada, se debe instanciar un grafo o árbol para finalmente introducirlo como argumento al generar un objeto de tipo GraphGUI, el cual mostrará en una ventana el grafo y ofrecerá la posibildad de mover los vértices con el ratón.
**ES MUY IMPORTANTE** que éste parámetro sea implementado en base al código base de la asignatura. Si alguno
de los atributos de las clases cambiase de nombre, es muy probable que el programa no funcionara correctamente. Para más información, consultar el [respositorio oficial de la asignatura](https://github.com/isegura/EDA)
o utilizar la implementación de grafos que viene por defecto con el paquete.
Además de una serie de funcionalidades accesibles en la barra superior, ya sean una pestaña de información adicional, otra pestaña de funcionalidades sobre el grafo y un menú desplegable que 
gestiona el almacenado de grafos.

Dicho esto, algunos ejemplos de uso podrían ser los siguientes:

+ Para representar el siguiente grafo:

     <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/CPT-Graphs-directed-weighted-ex1.svg/722px-CPT-Graphs-directed-weighted-ex1.svg.png' width='25%'/>
    
    Se podría disponer del siguiente código:
    ```python
    from graphdisplay import GraphGUI, Graph
    
    # Implementaremos el grafo de la siguiente imagen:
    # https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/CPT-Graphs-directed-weighted-ex1.svg/722px-CPT-Graphs-directed-weighted-ex1.svg.png
    
    labels = ['A', 'B', 'C', 'D', 'E']
    g = Graph(labels)
    
    g.addEdge('A', 'C', 12)  # A->(12)C
    g.addEdge('A', 'D', 60)  # A->(60)D
    g.addEdge('B', 'A', 10)  # B->(10)A
    g.addEdge('C', 'B', 20)  # C->(20)B
    g.addEdge('C', 'D', 32)  # C->(32)D
    g.addEdge('E', 'A', 7)   # E->(7)A
    
    # Para representar el grafo 
    if __name__ == "__main__":
        GraphGUI(g)
    ```

    <img src='https://github.com/seniorbeto/graphdisplay/assets/94072018/9210f5d4-4903-45ea-9bb8-e625890adac3' width='30%'/>
  
+ Ejemplo con árboles binarios de búsqueda:

    Para representar el siguiente árbol:

    <img src='https://github.com/seniorbeto/graphdisplay/assets/94072018/1418ef2c-3215-4d88-93ce-3d1c67c4a58e' width='70%'/>
    
    Se dispondría del siguiente código:
    ```python
    from graphdisplay import GraphGUI, BinarySearchTree
    
    labels = [12, 4, 16, 2, 10, 14, 19, 1, 8, 13, 18, 20, 6, 24]
    tree = BinarySearchTree()
    for i in labels:
        tree.insert(i)
       
    # Para representar el árbol
    if __name__ == "__main__":
        GraphGUI(tree)
    ```
    
    <img src='https://github.com/seniorbeto/graphdisplay/assets/94072018/1e87b61d-d6fd-4635-bdf0-136509250de7' width='60%'/>

## ⚡️Funcionalidades
Como ya se ha mencionado, una de las principales características de la aplicación consiste en la posibilidad de mover los vértices del grafo dentro de la ventana. Además,
éstos conservarán su posición si se cierra la ventana y se vuelve a abrir. Así mismo, es posible abrir varias ventanas al mismo tiempo 
instanciando varios objetos de tipo GraphGUI en el mismo programa. Es por esto que el sistema de autoguardado depende de en qué parte del programa se generen estos objetos GraphGUI.
Por ejemplo, si se han generado dos grafos A y B y ha llamado primero al A y luego al B, si se vuelve a ejecutar el programa pero esta vez llamando primero al B, el sistema
tratará de cargar el último estado del grafo A en el B. Para evitar esto, es recomendable generar una guardado permanente (pulsando el botón file>save y nombrando el guardado) para
después poder cargarlo (file>load) en cualquier momento.

Cabe destacar además, que las funcionalidades han sido testeadas únicamente en linux y en windows, variando las funcionalidades de la aplicación entre los sitemas. Por ejemplo,
al generar un objeto GraphGUI en windows, si no se ha instanciado dentro de la cláusula `if __name__ == "__main__":` saltará un _Warning_, cosa que no pasará en Linux. Por otra parte,
Windows permite generar sub-árboles presionando con el click derecho del ratón en un vértice (dicho árbol se generará en una nueva ventana), funcionalidad que no está disponible en linux debido al 
issue #16


## 🎯Ejemplos de uso


```python
from graphdisplay import GraphGUI, Graph

my_gragph = Graph(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'Z', 'N', 'O', 'P', 'Q'])
my_gragph.addEdge('A', 'B', 4)
my_gragph.addEdge('B', 'C', 8)
my_gragph.addEdge('C', 'A', 100)
my_gragph.addEdge('D', 'E', 7)
my_gragph.addEdge('E', 'F', 10)
my_gragph.addEdge('F', 'G', 5)
my_gragph.addEdge('G', 'Z', 6)
my_gragph.addEdge('A', 'H', 2)
my_gragph.addEdge('B', 'I', 3)
my_gragph.addEdge('C', 'J', 4)
my_gragph.addEdge('D', 'K', 5)
my_gragph.addEdge('E', 'L', 6)
my_gragph.addEdge('F', 'D', 3)
my_gragph.addEdge('G', 'H', 9)
my_gragph.addEdge('H', 'Z', 2)
my_gragph.addEdge('I', 'J', 1)
my_gragph.addEdge('J', 'A', 6)
my_gragph.addEdge('K', 'L', 5)
my_gragph.addEdge('L', 'M', 4)
my_gragph.addEdge('M', 'H', 3)
my_gragph.addEdge('N', 'O', 2)
my_gragph.addEdge('O', 'P', 1)
my_gragph.addEdge('P', 'Q', 7)
my_gragph.addEdge('H', 'A', 20)
my_gragph.addEdge('K', 'B', 7)
my_gragph.addEdge('H', 'N', 9)
my_gragph.addEdge('Q', 'D', 40)

if __name__ == "__main__":
    GraphGUI(g)
```

Y nos mostrará la ventana (reordenando los vértices):

<img src="https://github.com/seniorbeto/graphdisplay/assets/94072018/24120c29-839d-483c-a150-fefb678911f1" width="70%">

De la misma manera, un ejemplo de display de un árbol binario de búsqueda: 

<img src="https://github.com/seniorbeto/graphdisplay/assets/94072018/1fb39e40-52a0-4512-b52e-c613b96d1f79" width="200%">
