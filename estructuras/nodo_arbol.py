class NodoArbol:
    """Nodo de un árbol: tiene un hijo izquierdo y uno derecho."""

    def __init__(self, dato):
        """Crea un nodo de árbol.
        Recibe: dato, lo que se quiere guardar.
        Devuelve: nada (construye el objeto).
        """
        self.dato = dato
        self.izquierda = None
        self.derecha = None