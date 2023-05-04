import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '0.2.2' #Muy importante, deberéis ir cambiando la versión de vuestra librería según incluyáis nuevas funcionalidades
PACKAGE_NAME = 'graphdisplay' #Debe coincidir con el nombre de la carpeta
AUTHOR = 'Alberto Penas Díaz' #Modificar con vuestros datos
AUTHOR_EMAIL = 'albertopenasdiaz@gmail.com' #Modificar con vuestros datos
URL = 'https://github.com/seniorbeto' #Modificar con vuestros datos

LICENSE = 'MIT' #Tipo de licencia
DESCRIPTION = 'Librería para representar visualmente grafos de tipo diccionario' #Descripción corta
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8') #Referencia al documento README con una descripción más elaborada
LONG_DESC_TYPE = "text/markdown"


#Paquetes necesarios para que funcione la libreía. Se instalarán a la vez si no lo tuvieras ya instalado
INSTALL_REQUIRES = [
      'tk==0.1.1'
      ]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    #install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True,
    classifiers=['Programming Language :: Python',  # Clasificadores de compatibilidad con versiones de Python para tu paquete
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7']
)