from juego.puntajes import Puntajes

puntajes = Puntajes()
print(puntajes.registrar(120))
print(puntajes.registrar(85))
print(puntajes.registrar(200))
print(puntajes.registrar(85))
puntajes.mostrar()