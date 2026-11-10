from estructuras.nodo import Nodo


class ListaCircular:
    """Lista circular: el último nodo apunta de vuelta al primero."""

    def __init__(self):
        """Crea una lista circular vacía."""
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
        nuevo = Nodo(dato)
        if self.esta_vacia():
            nuevo.siguiente = nuevo
            self.cabeza = nuevo
            self.ultimo = nuevo
        else:
            nuevo.siguiente = self.cabeza
            self.cabeza = nuevo
            self.ultimo.siguiente = nuevo
        self.tamano += 1

    def insertar_final(self, dato):
        """Agrega un dato al final de la lista.
        Recibe: dato. Devuelve: nada.
        """
        nuevo = Nodo(dato)
        if self.esta_vacia():
            nuevo.siguiente = nuevo
            self.cabeza = nuevo
            self.ultimo = nuevo
        else:
            nuevo.siguiente = self.cabeza
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
        anterior = self.cabeza
        for _ in range(posicion - 1):
            anterior = anterior.siguiente
        nuevo = Nodo(dato)
        nuevo.siguiente = anterior.siguiente
        anterior.siguiente = nuevo
        self.tamano += 1
        return True

    def eliminar(self, dato):
        """Elimina la primera vez que aparece un dato.
        Recibe: dato. Devuelve: True si lo eliminó, False si no lo encontró.
        """
        if self.esta_vacia():
            return False
        anterior = self.ultimo
        actual = self.cabeza
        for _ in range(self.tamano):
            if actual.dato == dato:
                if self.tamano == 1:
                    self.cabeza = None
                    self.ultimo = None
                else:
                    anterior.siguiente = actual.siguiente
                    if actual is self.cabeza:
                        self.cabeza = actual.siguiente
                    if actual is self.ultimo:
                        self.ultimo = anterior
                self.tamano -= 1
                return True
            anterior = actual
            actual = actual.siguiente
        return False

    def buscar(self, dato):
        """Busca un dato en la lista.
        Recibe: dato. Devuelve: su posición (0 es el inicio), o -1 si no está.
        """
        actual = self.cabeza
        for posicion in range(self.tamano):
            if actual.dato == dato:
                return posicion
            actual = actual.siguiente
        return -1

    def recorrer(self):
        """Muestra todos los datos una sola vuelta.
        Recibe: nada. Devuelve: nada (imprime en pantalla).
        """
        if self.esta_vacia():
            print("Lista vacía")
            return
        actual = self.cabeza
        texto = ""
        for _ in range(self.tamano):
            texto += str(actual.dato) + " -> "
            actual = actual.siguiente
        print(texto + "(vuelve a " + str(self.cabeza.dato) + ")")