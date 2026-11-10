from estructuras.cola import Cola

c = Cola()
c.encolar("A")
c.encolar("B")
c.encolar("C")
print(c.ver_frente())
print(c.desencolar())
print(c.obtener_tamano())
print(c.esta_vacia())