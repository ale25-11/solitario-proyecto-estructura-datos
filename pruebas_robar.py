from juego.tablero import Tablero

tablero = Tablero()
primera = tablero.robar()
print("Primera carta:", primera.como_texto())

for _ in range(23):
    tablero.robar()

de_nuevo = tablero.robar()
print("Robo número 25:", de_nuevo.como_texto())
print("¿Es la misma que la primera?", primera is de_nuevo)