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
