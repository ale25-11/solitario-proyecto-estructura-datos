from estructuras.nodo_arbol import NodoArbol


class ArbolBST:
    """Árbol binario de búsqueda: menores a la izquierda, mayores a la derecha."""

    def __init__(self):
        """Crea un árbol vacío."""
        self.raiz = None
        self.tamano = 0

    def esta_vacio(self):
        """Recibe: nada. Devuelve: True si no hay datos, False si hay."""
        return self.raiz is None

    def obtener_tamano(self):
        """Recibe: nada. Devuelve: cuántos datos hay en el árbol."""
        return self.tamano

    def insertar(self, dato):
        """Agrega un dato en su lugar correcto.
        Recibe: dato. Devuelve: True si lo agregó, False si ya existía.
        """
        if self.buscar(dato):
            return False
        self.raiz = self._insertar(self.raiz, dato)
        self.tamano += 1
        return True

    def _insertar(self, nodo, dato):
        """Auxiliar de insertar: baja por el árbol hasta encontrar el hueco.
        Recibe: nodo actual y dato. Devuelve: el nodo actual (ya actualizado).
        """
        if nodo is None:
            return NodoArbol(dato)
        if dato < nodo.dato:
            nodo.izquierda = self._insertar(nodo.izquierda, dato)
        else:
            nodo.derecha = self._insertar(nodo.derecha, dato)
        return nodo

    def buscar(self, dato):
        """Busca un dato en el árbol.
        Recibe: dato. Devuelve: True si está, False si no.
        """
        actual = self.raiz
        while actual is not None:
            if dato == actual.dato:
                return True
            if dato < actual.dato:
                actual = actual.izquierda
            else:
                actual = actual.derecha
        return False

    def eliminar(self, dato):
        """Elimina un dato del árbol.
        Recibe: dato. Devuelve: True si lo eliminó, False si no estaba.
        """
        if not self.buscar(dato):
            return False
        self.raiz = self._eliminar(self.raiz, dato)
        self.tamano -= 1
        return True

    def _eliminar(self, nodo, dato):
        """Auxiliar de eliminar: encuentra el nodo y lo saca del árbol.
        Recibe: nodo actual y dato. Devuelve: el nodo que queda en ese lugar.
        """
        if dato < nodo.dato:
            nodo.izquierda = self._eliminar(nodo.izquierda, dato)
        elif dato > nodo.dato:
            nodo.derecha = self._eliminar(nodo.derecha, dato)
        else:
            if nodo.izquierda is None:
                return nodo.derecha
            if nodo.derecha is None:
                return nodo.izquierda
            sucesor = nodo.derecha
            while sucesor.izquierda is not None:
                sucesor = sucesor.izquierda
            nodo.dato = sucesor.dato
            nodo.derecha = self._eliminar(nodo.derecha, sucesor.dato)
        return nodo

    def inorden(self):
        """Muestra los datos de menor a mayor (izquierda, raíz, derecha).
        Recibe: nada. Devuelve: nada (imprime en pantalla).
        """
        self._inorden(self.raiz)
        print()

    def _inorden(self, nodo):
        """Auxiliar de inorden. Recibe: nodo actual. Devuelve: nada."""
        if nodo is not None:
            self._inorden(nodo.izquierda)
            print(nodo.dato, end=" ")
            self._inorden(nodo.derecha)

    def preorden(self):
        """Muestra raíz, izquierda, derecha.
        Recibe: nada. Devuelve: nada (imprime en pantalla).
        """
        self._preorden(self.raiz)
        print()

    def _preorden(self, nodo):
        """Auxiliar de preorden. Recibe: nodo actual. Devuelve: nada."""
        if nodo is not None:
            print(nodo.dato, end=" ")
            self._preorden(nodo.izquierda)
            self._preorden(nodo.derecha)

    def posorden(self):
        """Muestra izquierda, derecha, raíz.
        Recibe: nada. Devuelve: nada (imprime en pantalla).
        """
        self._posorden(self.raiz)
        print()

    def _posorden(self, nodo):
        """Auxiliar de posorden. Recibe: nodo actual. Devuelve: nada."""
        if nodo is not None:
            self._posorden(nodo.izquierda)
            self._posorden(nodo.derecha)
            print(nodo.dato, end=" ")