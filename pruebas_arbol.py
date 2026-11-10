from estructuras.arbol_bst import ArbolBST

arbol = ArbolBST()
for numero in [50, 30, 70, 20, 40, 60, 80]:
    arbol.insertar(numero)

arbol.inorden()
arbol.preorden()
arbol.posorden()
print(arbol.buscar(60))
print(arbol.buscar(99))
print(arbol.eliminar(30))
arbol.inorden()
print(arbol.obtener_tamano())