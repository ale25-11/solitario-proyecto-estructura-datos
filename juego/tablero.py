from estructuras.pila import Pila
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

    def mover_columna(self, origen, destino, cantidad):
        """Mueve un grupo de cartas de una columna a otra, si las reglas lo permiten.
        Recibe: origen y destino (columnas de 1 a 7) y cantidad de cartas
        a mover, contando desde el final de la columna de origen.
        Devuelve: una pareja (se_movio, mensaje). se_movio es True o False.
        """
        if origen < 1 or origen > 7 or destino < 1 or destino > 7:
            return False, "Las columnas van del 1 al 7"
        if origen == destino:
            return False, "Escoge dos columnas distintas"
        lista_origen = self.columnas[origen - 1]
        lista_destino = self.columnas[destino - 1]
        if cantidad < 1 or cantidad > lista_origen.obtener_tamano():
            return False, "No hay esa cantidad de cartas en la columna"

        nodo_base = lista_origen.ultimo
        for _ in range(cantidad - 1):
            nodo_base = nodo_base.anterior
        carta_base = nodo_base.dato
        if not carta_base.boca_arriba:
            return False, "Esa carta está boca abajo"

        if lista_destino.esta_vacia():
            if carta_base.valor != 13:
                return False, "Una columna vacía solo acepta K"
        else:
            carta_destino = lista_destino.ultimo.dato
            if carta_base.valor != carta_destino.valor - 1:
                return False, "La carta debe valer uno menos que la de destino"
            if carta_base.color() == carta_destino.color():
                return False, "La carta debe ser de color contrario"

        auxiliar = Pila()
        for _ in range(cantidad):
            carta = lista_origen.ultimo.dato
            lista_origen.eliminar(carta)
            auxiliar.apilar(carta)
        while not auxiliar.esta_vacia():
            lista_destino.insertar_final(auxiliar.desapilar())

        if not lista_origen.esta_vacia():
            lista_origen.ultimo.dato.boca_arriba = True
        return True, "Movimiento hecho"

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