from estructuras.nodo import Nodo


class Cola:
    """Cola (FIFO): el primero en entrar es el primero en salir."""

    def __init__(self):
        """Crea una cola vacía.
        Complejidad: O(1).
        """
        self.frente = None
        self.final = None
        self.tamano = 0

    def encolar(self, dato):
        """Agrega un dato al final de la cola.
        Recibe: dato. Devuelve: nada.
        Complejidad: O(1), se usa la flecha al final sin recorrer la cola.
        """
        nuevo = Nodo(dato)
        if self.esta_vacia():
            self.frente = nuevo
            self.final = nuevo
        else:
            self.final.siguiente = nuevo
            self.final = nuevo
        self.tamano += 1

    def desencolar(self):
        """Quita y devuelve el dato del frente.
        Recibe: nada. Devuelve: el dato, o None si la cola está vacía.
        Complejidad: O(1), solo se toca el frente.
        """
        if self.esta_vacia():
            return None
        dato = self.frente.dato
        self.frente = self.frente.siguiente
        if self.frente is None:
            self.final = None
        self.tamano -= 1
        return dato

    def ver_frente(self):
        """Mira el dato del frente sin quitarlo.
        Recibe: nada. Devuelve: el dato, o None si está vacía.
        Complejidad: O(1).
        """
        if self.esta_vacia():
            return None
        return self.frente.dato

    def esta_vacia(self):
        """Recibe: nada. Devuelve: True si no hay datos, False si hay.
        Complejidad: O(1).
        """
        return self.frente is None

    def obtener_tamano(self):
        """Recibe: nada. Devuelve: cuántos datos hay en la cola.
        Complejidad: O(1), el tamaño se lleva en un contador.
        """
        return self.tamano