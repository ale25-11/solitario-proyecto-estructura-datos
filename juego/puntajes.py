from estructuras.arbol_bst import ArbolBST


class Puntajes:
    """Guarda los mejores puntajes en un árbol binario de búsqueda.
    El puntaje es la cantidad de movimientos: menos es mejor.
    """

    def __init__(self):
        """Crea la lista de puntajes vacía."""
        self.arbol = ArbolBST()

    def registrar(self, movimientos):
        """Guarda un puntaje en el árbol.
        Recibe: movimientos de la partida ganada.
        Devuelve: True si lo guardó, False si ese puntaje ya existía.
        """
        return self.arbol.insertar(movimientos)

    def mostrar(self):
        """Imprime los puntajes de menor a mayor (recorrido inorden).
        Recibe: nada. Devuelve: nada.
        """
        print("Mejores puntajes (menos movimientos es mejor):")
        if self.arbol.esta_vacio():
            print("Aún no hay puntajes")
        else:
            self.arbol.inorden()