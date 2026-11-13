from estructuras.nodo import Nodo


class Pila:
    """Pila (LIFO): el último en entrar es el primero en salir."""

    def __init__(self):
        """Crea una pila vacía.
        Complejidad: O(1).
        """
        self.tope = None
        self.tamano = 0

    def apilar(self, dato):
        """Pone un dato encima de la pila.
        Recibe: dato. Devuelve: nada.
        Complejidad: O(1), solo se toca el tope.
        """
        nuevo = Nodo(dato)
        nuevo.siguiente = self.tope
        self.tope = nuevo
        self.tamano += 1

    def desapilar(self):
        """Quita y devuelve el dato de arriba.
        Recibe: nada. Devuelve: el dato, o None si la pila está vacía.
        Complejidad: O(1), solo se toca el tope.
        """
        if self.esta_vacia():
            return None
        dato = self.tope.dato
        self.tope = self.tope.siguiente
        self.tamano -= 1
        return dato

    def ver_tope(self):
        """Mira el dato de arriba sin quitarlo.
        Recibe: nada. Devuelve: el dato, o None si está vacía.
        Complejidad: O(1).
        """
        if self.esta_vacia():
            return None
        return self.tope.dato

    def esta_vacia(self):
        """Recibe: nada. Devuelve: True si no hay datos, False si hay.
        Complejidad: O(1).
        """
        return self.tope is None

    def obtener_tamano(self):
        """Recibe: nada. Devuelve: cuántos datos hay en la pila.
        Complejidad: O(1), el tamaño se lleva en un contador.
        """
        return self.tamano