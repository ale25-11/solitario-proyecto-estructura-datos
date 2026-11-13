from juego.juego import Juego
from juego.puntajes import Puntajes
from juego.demo import preparar_demo


def mostrar_reglas():
    """Imprime las reglas del solitario. Recibe: nada. Devuelve: nada."""
    print()
    print("REGLAS")
    print("- Hay 7 columnas. Solo se mueven cartas boca arriba.")
    print("- En una columna se pone una carta de valor uno menos y color contrario.")
    print("- Una columna vacía solo acepta K.")
    print("- Las fundaciones se arman por palo, del A al K.")
    print("- Ganas cuando las 4 fundaciones llegan a K.")
    print("- Pierdes si te rindes.")


def main():
    """Menú principal del juego. Recibe: nada. Devuelve: nada."""
    puntajes = Puntajes()
    while True:
        print()
        print("=== SOLITARIO ===")
        print("1. Jugar")
        print("2. Demostración (tablero casi ganado)")
        print("3. Reglas")
        print("4. Mejores puntajes")
        print("5. Salir")
        opcion = input("Opción: ")
        if opcion == "1":
            partida = Juego()
            if partida.jugar():
                puntajes.registrar(partida.movimientos)
                print("Tu puntaje quedó guardado")
        elif opcion == "2":
            partida = Juego()
            preparar_demo(partida.tablero)
            partida.jugar()
        elif opcion == "3":
            mostrar_reglas()
        elif opcion == "4":
            print()
            puntajes.mostrar()
        elif opcion == "5":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida, escribe 1, 2, 3, 4 o 5")
main()