import io
import tkinter as tk
from contextlib import redirect_stdout
from tkinter import messagebox

from juego.demo import preparar_demo
from juego.puntajes import Puntajes
from juego.tablero import Tablero

VERDE = "#2e7d32"
SIMBOLOS = {"corazones": "♥", "diamantes": "♦", "treboles": "♣", "picas": "♠"}


class VentanaJuego:
    """Ventana de una partida. Solo dibuja el tablero y llama a los métodos de Tablero."""

    def __init__(self, menu, es_demo):
        """Crea la ventana de la partida.
        Recibe: menu (el menú principal) y es_demo (True para el tablero casi ganado).
        Devuelve: nada (construye el objeto).
        """
        self.menu = menu
        self.es_demo = es_demo
        self.tablero = Tablero()
        if es_demo:
            preparar_demo(self.tablero)
        self.movimientos = 0

        self.ventana = tk.Toplevel(menu.raiz)
        self.ventana.title("Solitario")
        self.ventana.configure(bg=VERDE)

        self.etiqueta_info = tk.Label(self.ventana, bg=VERDE, fg="white",
                                      font=("Arial", 11, "bold"))
        self.etiqueta_info.pack(pady=5)
        self.marco_columnas = tk.Frame(self.ventana, bg=VERDE)
        self.marco_columnas.pack(padx=10, pady=5)
        self.etiqueta_fundaciones = tk.Label(self.ventana, bg=VERDE, fg="white",
                                             font=("Arial", 11, "bold"))
        self.etiqueta_fundaciones.pack(pady=5)
        self.etiqueta_mensaje = tk.Label(self.ventana, bg=VERDE, fg="yellow",
                                         font=("Arial", 11))
        self.etiqueta_mensaje.pack(pady=5)

        controles = tk.Frame(self.ventana, bg=VERDE)
        controles.pack(pady=5)

        fila = self.crear_fila(controles)
        self.crear_boton(fila, "Robar carta", self.robar)
        self.crear_boton(fila, "Mandar carta robada a fundación",
                         self.robada_a_fundacion)

        fila = self.crear_fila(controles)
        self.crear_texto(fila, "Bajar carta robada a la columna")
        self.spin_bajar = self.crear_spin(fila, 1, 7)
        self.crear_boton(fila, "Bajar", self.bajar_robada)

        fila = self.crear_fila(controles)
        self.crear_texto(fila, "Mover cartas de la columna")
        self.spin_origen = self.crear_spin(fila, 1, 7)
        self.crear_texto(fila, "a la columna")
        self.spin_destino = self.crear_spin(fila, 1, 7)
        self.crear_texto(fila, "cantidad")
        self.spin_cantidad = self.crear_spin(fila, 1, 19)
        self.crear_boton(fila, "Mover", self.mover)

        fila = self.crear_fila(controles)
        self.crear_texto(fila, "Mandar última carta de la columna")
        self.spin_fundacion = self.crear_spin(fila, 1, 7)
        self.crear_texto(fila, "a su fundación")
        self.crear_boton(fila, "Enviar", self.columna_a_fundacion)

        fila = self.crear_fila(controles)
        self.crear_boton(fila, "Rendirse", self.rendirse)

        self.dibujar()

    def crear_fila(self, padre):
        """Crea una fila de controles. Recibe: el contenedor. Devuelve: la fila."""
        fila = tk.Frame(padre, bg=VERDE)
        fila.pack(pady=3)
        return fila

    def crear_texto(self, fila, texto):
        """Pone un texto en una fila. Recibe: la fila y el texto. Devuelve: nada."""
        tk.Label(fila, text=texto, bg=VERDE, fg="white").pack(side="left")

    def crear_spin(self, fila, minimo, maximo):
        """Crea una casilla de solo flechas, así no se puede escribir un dato inválido.
        Recibe: la fila, el mínimo y el máximo. Devuelve: la casilla.
        """
        spin = tk.Spinbox(fila, from_=minimo, to=maximo, width=3, state="readonly")
        spin.pack(side="left", padx=4)
        return spin

    def crear_boton(self, fila, texto, comando):
        """Crea un botón en una fila.
        Recibe: la fila, el texto y la función que se ejecuta al presionarlo.
        Devuelve: nada.
        """
        tk.Button(fila, text=texto, command=comando).pack(side="left", padx=4)

    def leer(self, spin):
        """Recibe: una casilla de flechas. Devuelve: el número que muestra."""
        return int(spin.get())

    def dibujar_carta(self, columna, carta):
        """Dibuja una carta dentro de una columna.
        Boca arriba se ve el valor y el palo; boca abajo se ve un signo de pregunta.
        Recibe: la columna (contenedor) y la carta. Devuelve: nada.
        """
        if carta.boca_arriba:
            if carta.color() == "rojo":
                color = "red"
            else:
                color = "black"
            texto = carta.nombre_valor() + " " + SIMBOLOS[carta.palo]
            tk.Label(columna, text=texto, fg=color, bg="white", width=8,
                     relief="raised", font=("Arial", 10, "bold")).pack(pady=1)
        else:
            tk.Label(columna, text="?", fg="white", bg="#1565c0", width=8,
                     relief="raised", font=("Arial", 10, "bold")).pack(pady=1)

    def dibujar(self):
        """Redibuja todo el tablero con el estado actual.
        Recibe: nada. Devuelve: nada.
        """
        for elemento in self.marco_columnas.winfo_children():
            elemento.destroy()
        for numero in range(7):
            columna = tk.Frame(self.marco_columnas, bg=VERDE)
            columna.grid(row=0, column=numero, padx=4, sticky="n")
            tk.Label(columna, text="Columna " + str(numero + 1), bg=VERDE,
                     fg="white").pack()
            actual = self.tablero.columnas[numero].cabeza
            while actual is not None:
                self.dibujar_carta(columna, actual.dato)
                actual = actual.siguiente

        if self.tablero.nodo_robo is None:
            vista = "ninguna"
        else:
            vista = self.tablero.nodo_robo.dato.como_texto()
        self.etiqueta_info.config(
            text="Movimientos: " + str(self.movimientos)
            + "     Mazo de robo: "
            + str(self.tablero.mazo_robo.obtener_tamano()) + " cartas"
            + "     Carta a la vista: " + vista)

        texto = "Fundaciones:   "
        for indice in range(4):
            palo = self.tablero.palos[indice]
            fundacion = self.tablero.fundaciones[indice]
            if fundacion.esta_vacia():
                tope = "vacía"
            else:
                tope = fundacion.ver_tope().nombre_valor()
            texto += SIMBOLOS[palo] + " " + tope + "     "
        self.etiqueta_fundaciones.config(text=texto)

    def ejecutar(self, respuesta):
        """Muestra el resultado de una jugada, la cuenta y revisa si ganó.
        Recibe: una pareja (se_movio, mensaje). Devuelve: nada.
        """
        se_movio, mensaje = respuesta
        self.etiqueta_mensaje.config(text=mensaje)
        if se_movio:
            self.movimientos += 1
        self.dibujar()
        if self.tablero.ha_ganado():
            self.ganar()

    def robar(self):
        """Roba una carta del mazo. Recibe: nada. Devuelve: nada."""
        carta = self.tablero.robar()
        if carta is None:
            self.ejecutar((False, "El mazo de robo está vacío"))
        else:
            self.ejecutar((True, "Robaste: " + carta.como_texto()))

    def robada_a_fundacion(self):
        """Manda la carta robada a su fundación. Recibe: nada. Devuelve: nada."""
        self.ejecutar(self.tablero.mover_robo_a_fundacion())

    def bajar_robada(self):
        """Baja la carta robada a la columna escogida. Recibe: nada. Devuelve: nada."""
        self.ejecutar(self.tablero.mover_robo_a_columna(self.leer(self.spin_bajar)))

    def mover(self):
        """Mueve cartas entre columnas según las casillas. Recibe: nada. Devuelve: nada."""
        self.ejecutar(self.tablero.mover_columna(
            self.leer(self.spin_origen), self.leer(self.spin_destino),
            self.leer(self.spin_cantidad)))

    def columna_a_fundacion(self):
        """Manda la última carta de una columna a su fundación.
        Recibe: nada. Devuelve: nada.
        """
        self.ejecutar(self.tablero.mover_a_fundacion(self.leer(self.spin_fundacion)))

    def ganar(self):
        """Avisa que ganó y guarda el puntaje en el árbol (menos en la demostración).
        Recibe: nada. Devuelve: nada.
        """
        if not self.es_demo:
            self.menu.puntajes.registrar(self.movimientos)
        messagebox.showinfo("¡Ganaste!",
                            "¡GANASTE en " + str(self.movimientos) + " movimientos!",
                            parent=self.ventana)
        self.ventana.destroy()

    def rendirse(self):
        """El jugador se rinde y pierde. Recibe: nada. Devuelve: nada."""
        messagebox.showinfo("Solitario", "Te rendiste. PERDISTE.",
                            parent=self.ventana)
        self.ventana.destroy()


class MenuPrincipal:
    """Menú principal del juego."""

    def __init__(self):
        """Crea la ventana del menú y la lista de puntajes."""
        self.raiz = tk.Tk()
        self.raiz.title("Solitario")
        self.raiz.geometry("320x340")
        self.puntajes = Puntajes()

        tk.Label(self.raiz, text="SOLITARIO",
                 font=("Arial", 22, "bold")).pack(pady=20)
        self.crear_boton("Jugar", self.jugar)
        self.crear_boton("Demostración (tablero casi ganado)", self.demostracion)
        self.crear_boton("Reglas", self.reglas)
        self.crear_boton("Mejores puntajes", self.ver_puntajes)
        self.crear_boton("Salir", self.raiz.destroy)

    def crear_boton(self, texto, comando):
        """Crea un botón del menú.
        Recibe: el texto y la función que se ejecuta al presionarlo.
        Devuelve: nada.
        """
        tk.Button(self.raiz, text=texto, command=comando).pack(
            fill="x", padx=40, pady=6)

    def jugar(self):
        """Abre una partida nueva. Recibe: nada. Devuelve: nada."""
        VentanaJuego(self, False)

    def demostracion(self):
        """Abre la partida con el tablero casi ganado. Recibe: nada. Devuelve: nada."""
        VentanaJuego(self, True)

    def reglas(self):
        """Muestra las reglas del juego. Recibe: nada. Devuelve: nada."""
        messagebox.showinfo(
            "Reglas",
            "- Hay 7 columnas. Solo se mueven cartas boca arriba.\n"
            "- En una columna va una carta de valor uno menos y color contrario.\n"
            "- Una columna vacía solo acepta K.\n"
            "- Las fundaciones se arman por palo, del A al K.\n"
            "- Ganas cuando las 4 fundaciones llegan a K.\n"
            "- Pierdes si te rindes.")

    def ver_puntajes(self):
        """Muestra los puntajes guardados en el árbol, de menor a mayor.
        Recibe: nada. Devuelve: nada.
        """
        captura = io.StringIO()
        with redirect_stdout(captura):
            self.puntajes.mostrar()
        messagebox.showinfo("Mejores puntajes", captura.getvalue())

    def iniciar(self):
        """Abre el menú y espera a que el usuario lo use. Recibe: nada. Devuelve: nada."""
        self.raiz.mainloop()