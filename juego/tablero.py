from estructuras.pila import Pila
from estructuras.cola import Cola
from estructuras.lista_circular import ListaCircular
from estructuras.doble_lista_enlazada import DobleListaEnlazada
from juego.baraja import Baraja


class Tablero:
    """Tablero del solitario: 7 columnas, mazo de robo y 4 fundaciones."""

    def __init__(self):
        """Crea el tablero y reparte las cartas."""
        self.palos = ("corazones", "diamantes", "treboles", "picas")
        self.columnas = []
        for _ in range(7):
            self.columnas.append(DobleListaEnlazada())
        self.fundaciones = []
        for _ in range(4):
            self.fundaciones.append(Pila())
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

    def _quitar_carta_robo(self):
        """Saca del mazo de robo la carta que está a la vista.
        El marcador retrocede un puesto, así el próximo robo avanza a la carta que sigue.
        Recibe: nada. Devuelve: la carta que se sacó.
        """
        carta = self.nodo_robo.dato
        anterior = self.mazo_robo.ultimo
        actual = self.mazo_robo.cabeza
        for _ in range(self.mazo_robo.obtener_tamano()):
            if actual is self.nodo_robo:
                break
            anterior = actual
            actual = actual.siguiente
        self.mazo_robo.eliminar(carta)
        if self.mazo_robo.esta_vacia():
            self.nodo_robo = None
        else:
            self.nodo_robo = anterior
        return carta

    def _cabe_en_columna(self, carta, lista_destino):
        """Revisa si una carta puede ir al final de una columna.
        Recibe: la carta y la columna (lista) de destino.
        Devuelve: una pareja (se_puede, mensaje).
        """
        if lista_destino.esta_vacia():
            if carta.valor != 13:
                return False, "Una columna vacía solo acepta K"
            return True, ""
        carta_destino = lista_destino.ultimo.dato
        if carta.valor != carta_destino.valor - 1:
            return False, "La carta debe valer uno menos que la de destino"
        if carta.color() == carta_destino.color():
            return False, "La carta debe ser de color contrario"
        return True, ""

    def _cabe_en_fundacion(self, carta):
        """Revisa si una carta puede ir a la fundación de su palo.
        Recibe: la carta. Devuelve: una pareja (se_puede, mensaje).
        """
        fundacion = self.fundaciones[self.palos.index(carta.palo)]
        if fundacion.esta_vacia():
            if carta.valor != 1:
                return False, "La fundación empieza con el A"
        elif carta.valor != fundacion.ver_tope().valor + 1:
            return False, "La carta debe valer uno más que la de la fundación"
        return True, ""

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

        se_puede, mensaje = self._cabe_en_columna(carta_base, lista_destino)
        if not se_puede:
            return False, mensaje

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

    def mover_a_fundacion(self, columna):
        """Manda la última carta de una columna a su fundación, si las reglas lo permiten.
        La fundación de cada palo empieza con el A y sube de uno en uno.
        Recibe: columna (de 1 a 7).
        Devuelve: una pareja (se_movio, mensaje). se_movio es True o False.
        """
        if columna < 1 or columna > 7:
            return False, "Las columnas van del 1 al 7"
        lista = self.columnas[columna - 1]
        if lista.esta_vacia():
            return False, "La columna está vacía"
        carta = lista.ultimo.dato
        if not carta.boca_arriba:
            return False, "Esa carta está boca abajo"

        se_puede, mensaje = self._cabe_en_fundacion(carta)
        if not se_puede:
            return False, mensaje

        lista.eliminar(carta)
        self.fundaciones[self.palos.index(carta.palo)].apilar(carta)
        if not lista.esta_vacia():
            lista.ultimo.dato.boca_arriba = True
        return True, "Carta enviada a la fundación"

    def mover_robo_a_columna(self, destino):
        """Baja la carta robada a una columna, si las reglas lo permiten.
        Recibe: destino (columna de 1 a 7).
        Devuelve: una pareja (se_movio, mensaje). se_movio es True o False.
        """
        if self.nodo_robo is None:
            return False, "Primero roba una carta"
        if destino < 1 or destino > 7:
            return False, "Las columnas van del 1 al 7"
        lista_destino = self.columnas[destino - 1]
        carta = self.nodo_robo.dato
        se_puede, mensaje = self._cabe_en_columna(carta, lista_destino)
        if not se_puede:
            return False, mensaje
        self._quitar_carta_robo()
        lista_destino.insertar_final(carta)
        return True, "Carta movida a la columna"

    def mover_robo_a_fundacion(self):
        """Manda la carta robada a su fundación, si las reglas lo permiten.
        Recibe: nada.
        Devuelve: una pareja (se_movio, mensaje). se_movio es True o False.
        """
        if self.nodo_robo is None:
            return False, "Primero roba una carta"
        carta = self.nodo_robo.dato
        se_puede, mensaje = self._cabe_en_fundacion(carta)
        if not se_puede:
            return False, mensaje
        self._quitar_carta_robo()
        self.fundaciones[self.palos.index(carta.palo)].apilar(carta)
        return True, "Carta enviada a la fundación"

    def ha_ganado(self):
        """Recibe: nada. Devuelve: True si las 4 fundaciones llegaron a K (13 cartas)."""
        for fundacion in self.fundaciones:
            if fundacion.obtener_tamano() != 13:
                return False
        return True

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
        if self.nodo_robo is None:
            print("Carta a la vista: ninguna")
        else:
            print("Carta a la vista:", self.nodo_robo.dato.como_texto())
        print("Fundaciones:")
        for indice in range(4):
            fundacion = self.fundaciones[indice]
            if fundacion.esta_vacia():
                tope = "vacía"
            else:
                tope = fundacion.ver_tope().como_texto()
            print("  " + self.palos[indice] + ": " + tope)