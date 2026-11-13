class NodoDobleListaEnlazada:
    """Nodo con dos flechas: una al siguiente y otra al anterior."""

    def __init__(self, dato):
        """Crea un nodo.
        Recibe: dato, lo que se quiere guardar.
        Devuelve: nada (construye el objeto).
        Complejidad: O(1).
        """
        self.dato = dato
        self.siguiente = None
        self.anterior = None