from juego.tablero import Tablero


class Juego:
    """Controla una partida de solitario en consola."""

    def __init__(self):
        """Crea una partida nueva con el tablero repartido."""
        self.tablero = Tablero()
        self.movimientos = 0

    def pedir_numero(self, mensaje, minimo, maximo):
        """Pide un número y repite la pregunta hasta que sea válido.
        Recibe: mensaje a mostrar, y el mínimo y máximo permitidos.
        Devuelve: el número escrito por el usuario.
        """
        while True:
            texto = input(mensaje)
            try:
                numero = int(texto)
            except ValueError:
                print("Escribe solo números")
                continue
            if numero < minimo or numero > maximo:
                print("El número debe estar entre", minimo, "y", maximo)
                continue
            return numero

    def mostrar_resultado(self, respuesta):
        """Muestra el mensaje de un movimiento y lo cuenta si se hizo.
        Recibe: una pareja (se_movio, mensaje). Devuelve: nada.
        """
        se_movio, mensaje = respuesta
        print(mensaje)
        if se_movio:
            self.movimientos += 1

    def jugar(self):
        """Ciclo principal de la partida.
        Recibe: nada.
        Devuelve: True si ganó, False si se rindió.
        """
        while True:
            print()
            self.tablero.mostrar()
            if self.tablero.ha_ganado():
                print()
                print("¡GANASTE en", self.movimientos, "movimientos!")
                return True

            print()
            print("1. Robar carta")
            print("2. Bajar la carta robada a una columna")
            print("3. Mandar la carta robada a una fundación")
            print("4. Mover cartas entre columnas")
            print("5. Mandar la última carta de una columna a su fundación")
            print("6. Rendirse")
            opcion = self.pedir_numero("Opción: ", 1, 6)

            if opcion == 1:
                carta = self.tablero.robar()
                if carta is None:
                    print("El mazo de robo está vacío")
                else:
                    self.movimientos += 1
            elif opcion == 2:
                destino = self.pedir_numero("¿A qué columna (1-7)? ", 1, 7)
                self.mostrar_resultado(self.tablero.mover_robo_a_columna(destino))
            elif opcion == 3:
                self.mostrar_resultado(self.tablero.mover_robo_a_fundacion())
            elif opcion == 4:
                origen = self.pedir_numero("¿De qué columna (1-7)? ", 1, 7)
                destino = self.pedir_numero("¿A qué columna (1-7)? ", 1, 7)
                cantidad = self.pedir_numero("¿Cuántas cartas (1-19)? ", 1, 19)
                self.mostrar_resultado(
                    self.tablero.mover_columna(origen, destino, cantidad))
            elif opcion == 5:
                columna = self.pedir_numero("¿De qué columna (1-7)? ", 1, 7)
                self.mostrar_resultado(self.tablero.mover_a_fundacion(columna))
            elif opcion == 6:
                print()
                print("Te rendiste. PERDISTE.")
                return False