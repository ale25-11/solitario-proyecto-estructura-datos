from estructuras.lista_circular import ListaCircular

lista = ListaCircular()
lista.insertar_final("B")
lista.insertar_final("C")
lista.insertar_inicio("A")
lista.recorrer()
lista.insertar_posicion("X", 2)
lista.recorrer()
print(lista.buscar("C"))
print(lista.eliminar("A"))
lista.recorrer()
print(lista.obtener_tamano())