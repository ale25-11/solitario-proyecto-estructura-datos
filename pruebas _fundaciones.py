from juego.tablero import Tablero
from juego.carta import Carta

tablero = Tablero()

as_picas = Carta(1, "picas")
dos_picas = Carta(2, "picas")
cuatro_picas = Carta(4, "picas")
as_picas.boca_arriba = True
dos_picas.boca_arriba = True
cuatro_picas.boca_arriba = True

tablero.columnas[0].insertar_final(as_picas)
tablero.columnas[1].insertar_final(dos_picas)
tablero.columnas[2].insertar_final(cuatro_picas)

print(tablero.mover_a_fundacion(1))
print(tablero.mover_a_fundacion(2))
print(tablero.mover_a_fundacion(3))
print(tablero.ha_ganado())
tablero.mostrar()