# TFG Distribution and Generation System of Custom Props in Blender

## Descripción:

Extensión de Blender para distribuir y generar modelos 3D proceduralmente. El objetivo es permitir crear objetos base, ya sean casas, barriles, etc …, de estilo low-poly y que éstos sean personalizados inicialmente modificando parámetros propios del objeto. 

Por otro lado, que exista la posibilidad de distribuir objetos concretos sobre mallas proporcionadas por el usuario, siguiendo unas reglas concretas de distribución.

El propósito del proyecto es explorar la generación procedural de mallas, y de manera secundaria, facilitar trabajo en Game Jams y que el proceso de obtener recursos sencillos para un juego se agilice.

## Description:

Blender extension to distribute and generate 3D models procedurally. The goal is to create base objects, whether houses, barrels, etc ..., mainly in a low-poly style which can be customized by modifying the object's own parameters. 

On the other hand, there is the possibility of distributing specific objects on meshes provided by the user, following specific distribution rules.

The purpose of the project is to explore the procedural generation of meshes, and secondly, to facilitate work in Game Jams and to speed up the process of obtaining simple resources for a game.

Trabajo de fin de grado por José Daniel Rave Robayo, Daniel Illanes Morillas y Sergio José Alfonso Rojas

## Notas Instalación
Es necesario instalar aima (y tener instalado Python). Para ello ejecutar el siguiente comando desde cualquier cmd.
~~~ 
pip install aima3
~~~
Se habrá añadido una carpeta llamada _"aima3"_ al directorio _site-packages_ de la carpeta python el cual se encuentra en la carpeta fuente de Python.
(Ejecutando where python mostrara la localización del ejecutable python).
Por ej, debería estar en:
~~~
"C:\Users\user_name\AppData\Local\Programs\Python\Python310\Lib\site-packages"
~~~
En dicha ruta, copiar la carpeta _aima3_ a la carpeta de python que usa Blender para ejecutar el código: debería ser la carpeta de Blender cuya ruta sería tal que : _Blender-X.X/python/lib/site-packages_. 
Si sólo se tiene una versión de Blender instalada, y dicha carpeta coincide con la versión, ya no hay que hacer nada más.

En caso de no saber dónde se encuentra la ruta de python que usa Blender, o si se tiene más de una versión de Blender instalada, realizar los siguientes pasos:

- Abrir la versión de Blender deseada.
- Abrir la pestaña _Scripting_ (barra de pestañas superior).
- Crear un nuevo fichero usando el boton _+ New_.
- Copiar y pegar el siguiente código, y ejecutarlo dándole al bóton RUN situado arriba a la derecha o usar el atajo de teclado _Alt + P_.

~~~
import site

usersitepackagespath = site.getsitepackages()

print("Path: ", usersitepackagespath)
~~~

Abrir Toggle System Console desde arriba a la izquierda _Window -> Toggle System Console_,  para así poder ver el texto impreso por el código anterior. El texto debería mostrar la carpeta de python que ésta versión de Blender usa.
