from estructuras.cola import Cola
from estructuras.lista_circular import ListaCircular
from estructuras.doble_lista_enlazada import DobleListaEnlazada
from juego.baraja import Baraja


class Tablero:
    """Tablero del solitario: 7 columnas y un mazo de robo."""

    def __init__(self):
        """Crea el tablero y reparte las cartas."""
        self.columnas = []
        for _ in range(7):
            self.columnas.append(DobleListaEnlazada())
        self.mazo_robo = ListaCircular()
        self.nodo_robo = None
        self.repartir()

    def repartir(self):
        """Baraja, pone las cartas en una cola y las reparte.
        La columna 1 recibe 1 carta, la 2 recibe 2, y así hasta la 7.
        La última carta de cada columna queda boca arriba.
        Las cartas que sobran van al mazo de robo.
        Recibe: nada. Devuelve: nada.
        """
        baraja = Baraja()
        baraja.barajar()
        fila = Cola()
        while baraja.cantidad() > 0:
            fila.encolar(baraja.sacar_carta())
        for numero in range(7):
            for posicion in range(numero + 1):
                carta = fila.desencolar()
                if posicion == numero:
                    carta.boca_arriba = True
                self.columnas[numero].insertar_final(carta)
        while not fila.esta_vacia():
            self.mazo_robo.insertar_final(fila.desencolar())
    def robar(self):
        """Avanza a la siguiente carta del mazo de robo y la deja boca arriba.
        Al pasar la última carta, vuelve a la primera (lista circular).
        Recibe: nada. Devuelve: la carta, o None si el mazo está vacío.
        """
        if self.mazo_robo.esta_vacia():
            return None
        if self.nodo_robo is None:
            self.nodo_robo = self.mazo_robo.cabeza
        else:
            self.nodo_robo = self.nodo_robo.siguiente
        carta = self.nodo_robo.dato
        carta.boca_arriba = True
        return carta        

    def mostrar(self):
        """Imprime el tablero en pantalla.
        Las cartas boca abajo se ven como [?].
        Recibe: nada. Devuelve: nada.
        """
        for numero in range(7):
            texto = "Columna " + str(numero + 1) + ": "
            actual = self.columnas[numero].cabeza
            while actual is not None:
                carta = actual.dato
                if carta.boca_arriba:
                    texto += carta.como_texto() + " | "
                else:
                    texto += "[?] | "
                actual = actual.siguiente
            print(texto)
        print("Mazo de robo:", self.mazo_robo.obtener_tamano(), "cartas")