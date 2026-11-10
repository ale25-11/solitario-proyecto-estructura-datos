import random

from estructuras.pila import Pila
from juego.carta import Carta


class Baraja:
    """Baraja de 52 cartas guardada en una pila."""

    def __init__(self):
        """Crea una baraja nueva con las 52 cartas en orden."""
        self.mazo = Pila()
        self.crear()

    def crear(self):
        """Apila las 52 cartas (4 palos, valores del 1 al 13).
        Recibe: nada. Devuelve: nada.
        """
        for palo in ("corazones", "diamantes", "treboles", "picas"):
            for valor in range(1, 14):
                self.mazo.apilar(Carta(valor, palo))

    def barajar(self, veces=7):
        """Baraja el mazo usando pilas: lo parte en dos al azar y lo junta al azar.
        Recibe: veces, cuántas rondas de mezcla hacer.
        Devuelve: nada.
        """
        for _ in range(veces):
            izquierda = Pila()
            derecha = Pila()
            while not self.mazo.esta_vacia():
                carta = self.mazo.desapilar()
                if random.randint(0, 1) == 0:
                    izquierda.apilar(carta)
                else:
                    derecha.apilar(carta)
            while not izquierda.esta_vacia() or not derecha.esta_vacia():
                if izquierda.esta_vacia():
                    self.mazo.apilar(derecha.desapilar())
                elif derecha.esta_vacia():
                    self.mazo.apilar(izquierda.desapilar())
                elif random.randint(0, 1) == 0:
                    self.mazo.apilar(izquierda.desapilar())
                else:
                    self.mazo.apilar(derecha.desapilar())

    def sacar_carta(self):
        """Saca la carta de arriba del mazo.
        Recibe: nada. Devuelve: la carta, o None si el mazo está vacío.
        """
        return self.mazo.desapilar()

    def cantidad(self):
        """Recibe: nada. Devuelve: cuántas cartas quedan en el mazo."""
        return self.mazo.obtener_tamano()