# Solitario (Klondike) - Proyecto final de Estructuras de Datos

## Integrantes
- Jose Alejandro Jurado Bolaños
- Juan David Hernandez Hernandez

## Lenguaje y librerías
Python 3 (probado con Python 3.15). La interfaz gráfica usa Tkinter, que ya viene incluido con Python, así que no hay que instalar nada. También usa `random` de la biblioteca estándar. Además hay una versión en consola.

## Cómo ejecutarlo
1. Instalar Python 3 desde python.org (marcar "Add python.exe to PATH" al instalar).
2. Descargar este repositorio.
3. Abrir una terminal en la carpeta del proyecto.
4. Ejecutar la versión con ventana (recomendada):

```
python main_grafico.py
```

   O la versión en consola:

```
python main.py
```

## Cómo se gana y cómo se pierde
- **Se gana** cuando las 4 fundaciones (una por palo) llegan hasta la K.
- **Se pierde** si el jugador se rinde.
- El menú tiene una opción de **Demostración** con un tablero casi ganado, para ver la victoria rápido.

## Estructuras de datos
Las cinco estructuras están hechas desde cero con nodos y referencias, sin usar colecciones del lenguaje.

| Estructura | Archivo | Dónde se usa en el juego |
|---|---|---|
| Pila | `estructuras/pila.py` | Barajar, fundaciones y mover grupos de cartas |
| Cola | `estructuras/cola.py` | Repartir las cartas |
| Lista circular | `estructuras/lista_circular.py` | Mazo de robo |
| Doble lista enlazada | `estructuras/doble_lista_enlazada.py` | Las 7 columnas del tablero |
| Árbol binario de búsqueda | `estructuras/arbol_bst.py` | Mejores puntajes |

## Organización del código
- `estructuras/`: las 5 estructuras y sus nodos.
- `juego/`: las reglas del solitario (cartas, baraja, tablero, partida, puntajes y demo).
- `interfaz/`: la ventana gráfica (Tkinter). Solo dibuja y llama a los métodos del juego.
- `main_grafico.py`: arranca el juego con ventana.
- `main.py`: arranca el juego en consola.
- `pruebas_*.py`: pruebas de cada estructura y de las partes del juego.