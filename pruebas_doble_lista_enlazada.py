from estructuras.doble_lista_enlazada import DobleListaEnlazada

lista = DobleListaEnlazada()
lista.insertar_final("B")
lista.insertar_final("C")
lista.insertar_inicio("A")
lista.recorrer_adelante()
lista.recorrer_atras()
lista.insertar_posicion("X", 2)
lista.recorrer_adelante()
print(lista.buscar("C"))
print(lista.eliminar("A"))
lista.recorrer_adelante()
print(lista.obtener_tamano())