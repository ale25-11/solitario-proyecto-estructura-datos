from estructuras.nodo_doble_lista_enlazada import NodoDobleListaEnlazada


class DobleListaEnlazada:
    """Doble lista enlazada: se puede recorrer hacia adelante y atrás."""

    def __init__(self):
        """Crea una lista vacía."""
        self.cabeza = None
        self.ultimo = None
        self.tamano = 0

    def esta_vacia(self):
        """Recibe: nada. Devuelve: True si no hay datos, False si hay."""
        return self.cabeza is None

    def obtener_tamano(self):
        """Recibe: nada. Devuelve: cuántos datos hay en la lista."""
        return self.tamano

    def insertar_inicio(self, dato):
        """Agrega un dato al principio de la lista.
        Recibe: dato. Devuelve: nada.
        """
        nuevo = NodoDobleListaEnlazada(dato)
        if self.esta_vacia():
            self.cabeza = nuevo
            self.ultimo = nuevo
        else:
            nuevo.siguiente = self.cabeza
            self.cabeza.anterior = nuevo
            self.cabeza = nuevo
        self.tamano += 1

    def insertar_final(self, dato):
        """Agrega un dato al final de la lista.
        Recibe: dato. Devuelve: nada.
        """
        nuevo = NodoDobleListaEnlazada(dato)
        if self.esta_vacia():
            self.cabeza = nuevo
            self.ultimo = nuevo
        else:
            nuevo.anterior = self.ultimo
            self.ultimo.siguiente = nuevo
            self.ultimo = nuevo
        self.tamano += 1

    def insertar_posicion(self, dato, posicion):
        """Agrega un dato en una posición (0 es el inicio).
        Recibe: dato y posicion.
        Devuelve: True si se pudo insertar, False si la posición no existe.
        """
        if posicion < 0 or posicion > self.tamano:
            return False
        if posicion == 0:
            self.insertar_inicio(dato)
            return True
        if posicion == self.tamano:
            self.insertar_final(dato)
            return True
        actual = self.cabeza
        for _ in range(posicion):
            actual = actual.siguiente
        nuevo = NodoDobleListaEnlazada(dato)
        anterior = actual.anterior
        nuevo.anterior = anterior
        nuevo.siguiente = actual
        anterior.siguiente = nuevo
        actual.anterior = nuevo
        self.tamano += 1
        return True

    def eliminar(self, dato):
        """Elimina la primera vez que aparece un dato.
        Recibe: dato. Devuelve: True si lo eliminó, False si no lo encontró.
        """
        actual = self.cabeza
        while actual is not None:
            if actual.dato == dato:
                if actual.anterior is None:
                    self.cabeza = actual.siguiente
                else:
                    actual.anterior.siguiente = actual.siguiente
                if actual.siguiente is None:
                    self.ultimo = actual.anterior
                else:
                    actual.siguiente.anterior = actual.anterior
                self.tamano -= 1
                return True
            actual = actual.siguiente
        return False

    def buscar(self, dato):
        """Busca un dato en la lista.
        Recibe: dato. Devuelve: su posición (0 es el inicio), o -1 si no está.
        """
        actual = self.cabeza
        posicion = 0
        while actual is not None:
            if actual.dato == dato:
                return posicion
            actual = actual.siguiente
            posicion += 1
        return -1

    def recorrer_adelante(self):
        """Muestra los datos del primero al último.
        Recibe: nada. Devuelve: nada (imprime en pantalla).
        """
        if self.esta_vacia():
            print("Lista vacía")
            return
        texto = ""
        actual = self.cabeza
        while actual is not None:
            texto += str(actual.dato)
            if actual.siguiente is not None:
                texto += " <-> "
            actual = actual.siguiente
        print(texto)

    def recorrer_atras(self):
        """Muestra los datos del último al primero.
        Recibe: nada. Devuelve: nada (imprime en pantalla).
        """
        if self.esta_vacia():
            print("Lista vacía")
            return
        texto = ""
        actual = self.ultimo
        while actual is not None:
            texto += str(actual.dato)
            if actual.anterior is not None:
                texto += " <-> "
            actual = actual.anterior
        print(texto)