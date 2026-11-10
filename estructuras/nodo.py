class Nodo:
    """Caja que guarda un dato y una flecha al siguiente nodo."""

    def __init__(self, dato):
        """Crea un nodo.
        Recibe: dato, lo que se quiere guardar.
        Devuelve: nada (construye el objeto).
        """
        self.dato = dato
        self.siguiente = None