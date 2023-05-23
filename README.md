# TFG - Distribution of Custom Props in Blender

Trabajo de Fin de Grado por: 
* José Daniel Rave Robayo
* Daniel Illanes Morillas
* Sergio José Alfonso Rojas

***
<details open>
<summary><h2><u>Descripción</u></h2></summary>

### Español:

Extensión de Blender para distribuir modelos 3D proceduralmente. El objetivo es distribuir objetos concretos sobre mallas proporcionadas por el usuario, siguiendo unas reglas concretas de distribución.

El propósito del proyecto es explorar la distribución procedural de mallas para facilitar trabajo en Game Jams y que el proceso de obtener recursos sencillos para un juego se agilice.

### English:

Blender extension to distribute specific objects on meshes provided by the user, following specific distribution rules.

The purpose of the project is to explore the distribution of meshes to facilitate work in Game Jams and to speed up the process of obtaining simple resources for a game.
</details>


***
<details open>
<summary><h2><u>1. Instalación Pseudo-automática</u></h2></summary>

1. Es necesario tener instalado Python (para asegurar, instalarlo de todas formas, pinchando [aquí](https://www.python.org/downloads/)) y añadido al PATH (opción en el instalador de Python) ↓↓↓.

<!-- <img src="/imagesREADME/path.png" alt="Python Installation Image" width="1033" height="642"/> -->

![Descripción de la imagen](/imagesREADME/path.png)

## NOTA: En caso de instalarlo, esperar a que se instale completamente antes de proseguir.

El add-on se encuentra en el apartado [**Releases**](https://github.com/SergioJAlfonso/TFG-Distribution-and-Generation-System-of-Custom-Props-in-Blender/releases) a la derecha de Github.

2. Descargar de la **ÚLTIMA Release** el auxiliar **PreparerSurfaceSpray.zip**, y abrir Blender en modo Administrador (click derecho sobre el programa y ```Ejecutar como administrador```).

>**IMPORTANTE:** En caso de tener Blender desde **Steam**, ir a _C:\Program Files (x86)\Steam\steamapps\common\Blender_, y abrir el ejecutable .exe

Para instalar el add-on ir a _Edit_ -> _Preferencies_ -> pestaña _Add-ons_. 

3. Presionar el botón superior derecho ```Install``` y buscar el _.zip_ del add-on y clickar ```Install Add-on```.

Se deben esperar unos segundos a que se registre y aparezca en el buscador. En caso de que no aparezca, buscar "PreparerSurfaceSpray" y activarlo. 

4. Posteriormente desplegar la pestaña del add-on y aparecerá un botón de  ```Install Dependencies```. Se debe presionar y esperar a que salga el mensaje **_(Already Installed)_**. Es normal si el programa _No Responde_ debido a la instalación.

<img src="/imagesREADME/addon_installed.png" alt="Python Installation Image    " width="912" height="466"/>
<!-- ![Descripción de la imagen](/imagesREADME/addon_installed.png =912x466) -->

>**IMPORTANTE:** En caso que salte un error al presinar el botón, probar a volver a abrir Blender en **Modo Administrador**, o verificar que python está añadido al **PATH** (Environment Variable).

5. Una vez hecho esto, realizar la misma instalación con el add-on  **SurfaceSpray.zip** de la **ÚLTIMA Release**, obviando la parte de instalación de dependencias.
Una vez activado, salir del **menú de add-ons**. 

Presionar la tecla ```N``` sobre el 3D Viewport para mostrar el panel derecho de opciones. Se econtrará la pestaña ```SurfaceSpray```. 

**¡¡A disfrutar!!**
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
