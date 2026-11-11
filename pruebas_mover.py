from juego.tablero import Tablero

tablero = Tablero()
tablero.mostrar()

movido = False
for origen in range(1, 8):
    for destino in range(1, 8):
        if not movido and origen != destino:
            movido, mensaje = tablero.mover_columna(origen, destino, 1)
            if movido:
                print()
                print("Se movió de la columna", origen, "a la columna", destino)

if not movido:
    print("En este reparto no había ningún movimiento posible, corre otra vez")

print()
tablero.mostrar()