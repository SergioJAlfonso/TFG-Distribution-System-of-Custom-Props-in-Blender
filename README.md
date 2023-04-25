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

***
<details open>
<summary><h2><u>1. Instalación Pseudo-automática</u></h2></summary>

Es necesario tener instalado [Python](https://www.python.org/downloads/) y añadido al environment path (opción a la hora de instalar python).

Descargar el add-on, descargar el auxiliar **PreparerSurfaceSpray.zip**, y abrir Blender en modo Administrador (click derecho sobre el programa y ```Ejecutar como administrador```).

Para instalar el add-on ir a _Edit_ -> _Preferencies_ -> Tab _Add-ons_. 

Presionar el botón superior derecho ```Install``` y buscar el .zip del add-on y clickar ```Install Add-on```.

Se deben esperar unos segundos a que se registre y aparezca en el buscador. En caso de que no aparezca, buscar "PreparerSurfaceSpray" y activarlo. 

Posteriormente desplegar la pestaña del add-on y aparecerá un botón de  ```Install Dependencies```. Se debe presionar y esperar a que salga el mensaje _(Already Installed)_.

Una vez hecho esto, realizar la misma instalación con el add-on  **SurfaceSpray.zip**.
</details>

***
<details>
<summary><h2><u>2. Instalación Manual</u></h2></summary>

Es necesario instalar aima (y tener instalado Python). Para ello ejecutar el siguiente comando desde cualquier ```cmd```.
~~~ 
pip install aima3
~~~

Se habrá añadido una carpeta llamada _"aima3"_ al directorio _site-packages_ (de la carpeta _python_) el cual se encuentra en la carpeta fuente de **Python**.

Ejecutando el siguiente código en una cmd, mostrará la localización del ejecutable python.

~~~ 
where python
~~~

Por ejemplo, debería estar encontrarse en una ruta similar a:
~~~
"C:\Users\user_name\AppData\Local\Programs\Python\Python310\Lib\site-packages"
~~~
A continuación, en dicha ruta copiar la carpeta _aima3_ a la carpeta de python que utiliza Blender: debería ser la carpeta de Blender cuya ruta sería tal que: 

~~~ 
Blender-X.X/python/lib/site-packages
~~~ 
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
</details>
