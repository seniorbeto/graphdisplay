import pathlib
from setuptools import find_packages, setup
from graphdisplay.general_config import *

HERE = pathlib.Path(__file__).parent

VERSION = VERSION
PACKAGE_NAME = 'graphdisplay'
AUTHOR = 'Alberto Penas Díaz'
AUTHOR_EMAIL = 'albertopenasdiaz@gmail.com'
URL = 'https://github.com/seniorbeto'

LICENSE = 'MIT' #Tipo de licencia
DESCRIPTION = 'Librería para representar visualmente grafos de tipo diccionario'
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8')
LONG_DESC_TYPE = "text/markdown"


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
    classifiers=['Programming Language :: Python',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7']
)