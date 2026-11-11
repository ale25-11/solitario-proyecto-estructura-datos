from estructuras.pila import Pila
from estructuras.lista_circular import ListaCircular
from estructuras.doble_lista_enlazada import DobleListaEnlazada
from juego.carta import Carta


def preparar_demo(tablero):
    """Deja el tablero casi ganado para mostrar la victoria en la sustentación.
    Cada fundación llega hasta la Q y las 4 K están en las columnas 1 a 4.
    Recibe: el tablero. Devuelve: nada.
    """
    tablero.columnas = []
    for _ in range(7):
        tablero.columnas.append(DobleListaEnlazada())
    tablero.fundaciones = []
    for _ in range(4):
        tablero.fundaciones.append(Pila())
    tablero.mazo_robo = ListaCircular()
    tablero.nodo_robo = None
    for numero in range(4):
        palo = tablero.palos[numero]
        for valor in range(1, 13):
            carta = Carta(valor, palo)
            carta.boca_arriba = True
            tablero.fundaciones[numero].apilar(carta)
        rey = Carta(13, palo)
        rey.boca_arriba = True
        tablero.columnas[numero].insertar_final(rey)