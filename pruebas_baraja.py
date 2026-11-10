from juego.baraja import Baraja

baraja = Baraja()
print(baraja.cantidad())
baraja.barajar()
print(baraja.cantidad())
for _ in range(5):
    print(baraja.sacar_carta().como_texto())
print(baraja.cantidad())