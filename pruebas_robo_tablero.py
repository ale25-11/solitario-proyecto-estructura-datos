from juego.tablero import Tablero
from juego.carta import Carta
from estructuras.lista_circular import ListaCircular

tablero = Tablero()

# Armamos un mazo de robo de prueba con 3 cartas conocidas
tablero.mazo_robo = ListaCircular()
tablero.mazo_robo.insertar_final(Carta(5, "corazones"))
tablero.mazo_robo.insertar_final(Carta(9, "picas"))
tablero.mazo_robo.insertar_final(Carta(1, "treboles"))
tablero.nodo_robo = None

# Ponemos un 6 de picas boca arriba al final de la columna 1
seis = Carta(6, "picas")
seis.boca_arriba = True
tablero.columnas[0].insertar_final(seis)

print(tablero.robar().como_texto())
print(tablero.mover_robo_a_columna(1))
print(tablero.mazo_robo.obtener_tamano())
print(tablero.robar().como_texto())
print(tablero.robar().como_texto())
print(tablero.mover_robo_a_fundacion())
print(tablero.mazo_robo.obtener_tamano())