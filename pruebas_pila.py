from estructuras.pila import Pila

p = Pila()
p.apilar("A")
p.apilar("B")
p.apilar("C")
print(p.ver_tope())
print(p.desapilar())
print(p.obtener_tamano())
print(p.esta_vacia())