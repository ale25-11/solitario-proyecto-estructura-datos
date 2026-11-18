import io
import random
import threading
import tkinter as tk
from contextlib import redirect_stdout
from tkinter import font as tkfont
from tkinter import messagebox

from estructuras.doble_lista_enlazada import DobleListaEnlazada
from estructuras.lista_circular import ListaCircular
from estructuras.pila import Pila
from juego.demo import preparar_demo
from juego.puntajes import Puntajes
from juego.tablero import Tablero

try:
    import winsound
except ImportError:
    winsound = None

# ---------- Paleta ----------
MESA = "#0b3470"
MESA_OSCURA = "#082a5a"
MESA_BORDE = "#3f74be"
BARRA = "#061d44"
MARFIL = "#fbf8f1"
MARFIL_BORDE = "#cfc8b8"
ROJO = "#c8332b"
NEGRO = "#1d2330"
AZUL_DORSO = "#7a1f2b"
DORADO = "#e9b949"
DORADO_CLARO = "#f3cd6e"
TEXTO = "#f4efe3"
TEXTO_SUAVE = "#a6c1e6"
ERROR = "#ff9d8f"
EXITO = "#a8e6a1"
BOTON = "#174488"
BOTON_HOVER = "#2158aa"

FUENTE_TITULO = "Georgia"
FUENTE_UI = "Segoe UI"
FUENTE_SIMBOLO = "Segoe UI Symbol"

SIMBOLOS = {"corazones": "♥", "diamantes": "♦", "treboles": "♣", "picas": "♠"}

# ---------- Medidas del tablero ----------
ANCHO = 960
ALTO = 590
CW = 100            # ancho de una carta
CH = 140            # alto de una carta
SEP = 22            # espacio entre columnas
MARGEN = (ANCHO - (7 * CW + 6 * SEP)) // 2
FILA_Y = 18         # altura de la fila de arriba (mazo, robo, fundaciones)
COL_Y = 190         # altura donde empiezan las columnas

# Frases con humor: reemplazan a los mensajes del tablero (la lógica no cambia)
HUMOR = {
    "Una columna vacía solo acepta K": [
        "Columna vacía = solo reyes. Esto es un palacio, no un hostal.",
        "Ahí solo entra un K. Los demás, a la fila."],
    "La carta debe valer uno menos que la de destino": [
        "Casi, pero va una carta menos que esa. Las matemáticas no perdonan.",
        "Esa carta no cuadra: tiene que valer uno menos."],
    "La carta debe ser de color contrario": [
        "Mismo color no. Hasta las cartas necesitan variedad.",
        "Rojo con rojo y negro con negro no se llevan."],
    "La fundación empieza con el A": [
        "Las fundaciones arrancan con el As, no hay atajos.",
        "Primero el As. Los reyes llegan al final."],
    "La carta debe valer uno más que la de la fundación": [
        "Falta una carta antes de esa. Paciencia, campeón.",
        "Todavía no le toca a esa carta. Hay fila."],
    "El mazo de robo está vacío": [
        "Mazo vacío. La casa no tiene más cartas."],
    "Primero roba una carta": [
        "No hay carta a la vista. ¡Roba una primero!"],
    "Esa carta está boca abajo": [
        "Esa carta está dormida, no se puede mover."],
    "Esa carta no tiene a dónde ir por ahora": [
        "Esa carta anda sin plan. Por ahora no tiene a dónde ir.",
        "Nadie la quiere por ahora. Prueba con otra."],
    "A las fundaciones se sube una carta a la vez": [
        "Una carta a la vez, que esto no es una mudanza."],
    "Movimiento hecho": ["Movimiento hecho", "Buena jugada", "Así se hace", "Limpio"],
    "Carta enviada a la fundación": [
        "¡Una más para la fundación!", "Directo a la fundación", "Eso sí es avanzar"],
    "Carta movida a la columna": ["Carta en su nueva casa", "Bien acomodada"],
}

FRASES_VICTORIA = [
    "La casa pierde. Tú ganas.",
    "Oficialmente, un crack de las cartas.",
    "Pago completo: las 4 fundaciones.",
]

CLICS_SECRETO = 5

# Sonidos suaves (frecuencia en Hz, duración en ms). Solo suenan en Windows.
SONIDOS = {
    "mover": [(700, 45)],
    "robar": [(520, 35)],
    "fundacion": [(784, 50), (1047, 70)],
    "error": [(240, 110)],
    "deshacer": [(500, 50), (380, 60)],
    "ganar": [(523, 130), (659, 130), (784, 130), (1047, 320)],
}

ESTRUCTURAS = [
    ("Pila", "Barajar, fundaciones, mover grupos de cartas y el historial de Deshacer"),
    ("Cola", "Repartir las cartas"),
    ("Lista circular", "Mazo de robo: al pasar la última carta vuelve a la primera"),
    ("Doble lista enlazada", "Las 7 columnas del tablero"),
    ("Árbol binario de búsqueda", "Mejores puntajes, ordenados de menor a mayor"),
]

REGLAS = [
    "Hay 7 columnas. Solo se mueven cartas boca arriba.",
    "En una columna va una carta de valor uno menos y color contrario.",
    "Una columna vacía solo acepta K.",
    "Las fundaciones se arman por palo, del A al K.",
    "Ganas cuando las 4 fundaciones llegan a K.",
    "Pierdes si te rindes.",
]

CONSEJOS = [
    "Arrastra una carta (o un grupo) a otra columna o a una fundación.",
    "Haz doble clic en una carta y se mueve sola donde pueda ir.",
    "Haz clic en el mazo (o presiona Espacio) para robar una carta.",
    "Pista (H) te muestra una jugada posible. Deshacer (U o Ctrl+Z) vuelve atrás.",
    "Estructuras (E) muestra por dentro cómo está el juego, en vivo.",
]


def centrar(ventana, ancho, alto):
    """Centra una ventana en la pantalla.
    Recibe: la ventana, su ancho y su alto. Devuelve: nada.
    """
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() - ancho) // 2
    y = max((ventana.winfo_screenheight() - alto) // 2 - 20, 0)
    ventana.geometry(str(ancho) + "x" + str(alto) + "+" + str(x) + "+" + str(y))


def crear_boton(padre, texto, comando, primario=False, grande=False, compacto=False):
    """Crea un botón plano que cambia de color al pasar el mouse.
    Recibe: el contenedor, el texto, la función a ejecutar y dos opciones de estilo.
    Devuelve: el botón (todavía sin colocar).
    """
    fondo = DORADO if primario else BOTON
    resaltado = DORADO_CLARO if primario else BOTON_HOVER
    color_texto = NEGRO if primario else TEXTO
    margen_x = 16
    if grande:
        letra = (FUENTE_UI, 12, "bold")
        margen_y = 11
    elif compacto:
        letra = (FUENTE_UI, 9, "bold")
        margen_y = 5
        margen_x = 10
    else:
        letra = (FUENTE_UI, 10, "bold")
        margen_y = 7
    boton = tk.Label(padre, text=texto, bg=fondo, fg=color_texto, font=letra,
                     padx=margen_x, pady=margen_y, cursor="hand2")
    boton.bind("<Enter>", lambda e: boton.config(bg=resaltado))
    boton.bind("<Leave>", lambda e: boton.config(bg=fondo))
    boton.bind("<Button-1>", lambda e: comando())
    return boton


def leer_pila(pila):
    """Lee el contenido de una Pila sin cambiarla.
    Recibe: la pila. Devuelve: una lista con sus cartas, de abajo hacia arriba.
    """
    sacadas = []
    while not pila.esta_vacia():
        sacadas.append(pila.desapilar())
    for carta in reversed(sacadas):
        pila.apilar(carta)
    sacadas.reverse()
    return sacadas


def capturar_estado(tablero, movimientos):
    """Guarda una foto del tablero para poder deshacer una jugada.
    Recibe: el tablero y el número de movimientos. Devuelve: un diccionario con
    las cartas de cada estructura y qué cartas están boca arriba.
    """
    columnas = []
    todas = []
    for lista in tablero.columnas:
        cartas = []
        actual = lista.cabeza
        while actual is not None:
            cartas.append(actual.dato)
            actual = actual.siguiente
        columnas.append(cartas)
        todas.extend(cartas)
    fundaciones = []
    for pila in tablero.fundaciones:
        cartas = leer_pila(pila)
        fundaciones.append(cartas)
        todas.extend(cartas)
    mazo = []
    indice_robo = None
    actual = tablero.mazo_robo.cabeza
    for posicion in range(tablero.mazo_robo.obtener_tamano()):
        mazo.append(actual.dato)
        if actual is tablero.nodo_robo:
            indice_robo = posicion
        actual = actual.siguiente
    todas.extend(mazo)
    caras = []
    for carta in todas:
        caras.append((carta, carta.boca_arriba))
    return {"columnas": columnas, "fundaciones": fundaciones, "mazo": mazo,
            "indice_robo": indice_robo, "caras": caras, "movimientos": movimientos}


def restaurar_estado(tablero, estado):
    """Vuelve el tablero a una foto guardada, reconstruyendo cada estructura.
    Recibe: el tablero y el estado. Devuelve: los movimientos que había entonces.
    """
    for indice in range(7):
        lista = DobleListaEnlazada()
        for carta in estado["columnas"][indice]:
            lista.insertar_final(carta)
        tablero.columnas[indice] = lista
    for indice in range(4):
        pila = Pila()
        for carta in estado["fundaciones"][indice]:
            pila.apilar(carta)
        tablero.fundaciones[indice] = pila
    mazo = ListaCircular()
    for carta in estado["mazo"]:
        mazo.insertar_final(carta)
    tablero.mazo_robo = mazo
    tablero.nodo_robo = None
    if estado["indice_robo"] is not None:
        nodo = mazo.cabeza
        for _ in range(estado["indice_robo"]):
            nodo = nodo.siguiente
        tablero.nodo_robo = nodo
    for carta, cara in estado["caras"]:
        carta.boca_arriba = cara
    return estado["movimientos"]


class VentanaJuego:
    """Ventana de una partida. Solo dibuja y llama a los métodos de Tablero."""

    def __init__(self, menu, es_demo):
        """Crea la ventana de la partida.
        Recibe: menu (el menú principal) y es_demo (True para el tablero casi ganado).
        Devuelve: nada (construye el objeto).
        """
        self.menu = menu
        self.es_demo = es_demo
        self.vivo = True
        self.id_tic = None
        self.id_pista = None
        self.panel_final = None
        self.id_auto = None
        self.id_tip = None
        self.capo = None
        self.sonido_activo = True
        self.ficha_giro = 0
        self.auto = False
        self.giro = None

        self.ventana = tk.Toplevel(menu.raiz)
        self.ventana.title("Solitario")
        self.ventana.configure(bg=BARRA)
        self.ventana.resizable(False, False)
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar)
        centrar(self.ventana, ANCHO, ALTO + 100)

        self.f_rango = tkfont.Font(root=self.ventana, family=FUENTE_TITULO,
                                   size=16, weight="bold")
        self.f_simbolo_peq = tkfont.Font(root=self.ventana, family=FUENTE_SIMBOLO,
                                         size=13)
        self.f_simbolo_med = tkfont.Font(root=self.ventana, family=FUENTE_SIMBOLO,
                                         size=20)
        self.f_simbolo_gde = tkfont.Font(root=self.ventana, family=FUENTE_SIMBOLO,
                                         size=40)
        self.f_figura = tkfont.Font(root=self.ventana, family=FUENTE_TITULO,
                                    size=34, weight="bold", slant="italic")
        self.f_pequena = tkfont.Font(root=self.ventana, family=FUENTE_UI, size=10)

        self.construir_encabezado()
        self.canvas = tk.Canvas(self.ventana, width=ANCHO, height=ALTO, bg=MESA,
                                highlightthickness=0)
        self.canvas.pack()
        self.dibujar_fondo()
        self.construir_pie()

        self.canvas.bind("<ButtonPress-1>", self.presionar)
        self.canvas.bind("<B1-Motion>", self.arrastrar)
        self.canvas.bind("<ButtonRelease-1>", self.soltar)
        self.canvas.bind("<Double-Button-1>", self.doble_clic)
        self.canvas.bind("<Motion>", self.pasar_mouse)
        self.ventana.bind("<KeyPress>", self.tecla)
        self.ventana.focus_force()

        self.nueva_partida()
        self.tic()

    # ------------------------------------------------------------------
    # Construcción de la ventana
    # ------------------------------------------------------------------
    def dibujar_fondo(self):
        """Dibuja el fondo de casino: paño azul con rombos suaves, luz en el centro
        y un borde dorado. Se dibuja una sola vez. Recibe: nada. Devuelve: nada.
        """
        c = self.canvas
        for k in range(7):
            mezcla = k / 7
            m = int(0x0b + (0x14 - 0x0b) * mezcla)
            n = int(0x34 + (0x5c - 0x34) * mezcla)
            o = int(0x70 + (0xb0 - 0x70) * mezcla)
            color = "#{:02x}{:02x}{:02x}".format(m, n, o)
            c.create_oval(-300 + k * 70, -170 + k * 40, ANCHO + 300 - k * 70,
                          ALTO + 170 - k * 40, fill=color, outline="", tags="fondo")
        for x in range(-ALTO, ANCHO + ALTO, 60):
            c.create_line(x, 0, x + ALTO, ALTO, fill="#0e3f84", tags="fondo")
            c.create_line(x, ALTO, x + ALTO, 0, fill="#0e3f84", tags="fondo")
        c.create_text(ANCHO / 2, COL_Y - 24, text="♠  ♥  ♣  ♦", fill="#14509f",
                      font=(FUENTE_SIMBOLO, 16), tags="fondo")
        c.create_rectangle(5, 5, ANCHO - 5, ALTO - 5, outline=DORADO, width=2,
                           tags="fondo")
        c.create_rectangle(11, 11, ANCHO - 11, ALTO - 11, outline="#8a6d25",
                           tags="fondo")
        c.tag_lower("fondo")

    def construir_encabezado(self):
        """Crea la barra de arriba con el título y los botones.
        Recibe: nada. Devuelve: nada.
        """
        barra = tk.Frame(self.ventana, bg=BARRA)
        barra.pack(fill="x", padx=18, pady=10)

        titulo = tk.Label(barra, text="Solitario", bg=BARRA, fg=TEXTO,
                          font=(FUENTE_TITULO, 20, "bold"))
        titulo.pack(side="left")
        titulo.bind("<Button-1>", self.clic_titulo)
        self.clics_titulo = 0
        if self.es_demo:
            tk.Label(barra, text="demostración", bg=BARRA, fg=DORADO,
                     font=(FUENTE_TITULO, 12, "italic")).pack(side="left", padx=10)

        crear_boton(barra, "Rendirse", self.rendirse, compacto=True).pack(
            side="right", padx=(5, 0))
        crear_boton(barra, "Reglas", self.menu.reglas, compacto=True).pack(
            side="right", padx=(5, 0))
        self.boton_sonido = crear_boton(barra, "Sonido: sí", self.alternar_sonido,
                                        compacto=True)
        self.boton_sonido.pack(side="right", padx=(5, 0))
        crear_boton(barra, "Estructuras", self.abrir_capo, compacto=True).pack(
            side="right", padx=(5, 0))
        if self.es_demo:
            self.boton_auto = crear_boton(barra, "Autojugar", self.alternar_auto,
                                          compacto=True)
            self.boton_auto.pack(side="right", padx=(5, 0))
        else:
            crear_boton(barra, "Nueva partida", self.confirmar_nueva,
                        compacto=True).pack(side="right", padx=(5, 0))
        crear_boton(barra, "Deshacer", self.deshacer, compacto=True).pack(
            side="right", padx=(5, 0))
        crear_boton(barra, "Pista", self.dar_pista, primario=True,
                    compacto=True).pack(side="right", padx=(5, 0))

    def construir_pie(self):
        """Crea la barra de abajo con el mensaje, los datos y el progreso.
        Recibe: nada. Devuelve: nada.
        """
        pie = tk.Frame(self.ventana, bg=BARRA)
        pie.pack(fill="x", padx=18, pady=(2, 10))
        datos = tk.Frame(pie, bg=BARRA)
        datos.pack(side="right")
        self.etiqueta_mov = tk.Label(datos, bg=BARRA, fg=TEXTO, font=(FUENTE_UI, 10))
        self.etiqueta_mov.pack(side="left", padx=8)
        self.etiqueta_tiempo = tk.Label(datos, bg=BARRA, fg=TEXTO, font=(FUENTE_UI, 10))
        self.etiqueta_tiempo.pack(side="left", padx=8)
        self.barra_fund = tk.Canvas(datos, width=110, height=10, bg=MESA_OSCURA,
                                    highlightthickness=0)
        self.barra_fund.pack(side="left", padx=(8, 4))
        self.etiqueta_prog = tk.Label(datos, bg=BARRA, fg=TEXTO, font=(FUENTE_UI, 10),
                                      width=5, anchor="w")
        self.etiqueta_prog.pack(side="left")
        self.etiqueta_mensaje = tk.Label(pie, bg=BARRA, fg=TEXTO_SUAVE,
                                         font=(FUENTE_UI, 11), anchor="w")
        self.etiqueta_mensaje.pack(side="left", fill="x", expand=True)

    # ------------------------------------------------------------------
    # Estado de la partida
    # ------------------------------------------------------------------
    def nueva_partida(self):
        """Reparte una partida nueva y reinicia los contadores.
        Recibe: nada. Devuelve: nada.
        """
        self.tablero = Tablero()
        if self.es_demo:
            preparar_demo(self.tablero)
        self.movimientos = 0
        self.segundos = 0
        self.terminada = False
        self.animando = False
        self.candidato = None
        self.arrastre = None
        self.destinos = []
        self.rects_pista = []
        self.historial = Pila()
        self.previo = None
        self.giro = None
        self.ficha_giro += 1
        self.detener_auto()
        self.zonas = []
        self.rect_cartas = {}
        self.rect_dest = {}
        self.rect_fund = {}
        self.canvas.delete("confeti")
        self.canvas.delete("final")
        if self.panel_final is not None:
            self.panel_final.destroy()
            self.panel_final = None
        self.mensaje("Arrastra las cartas o haz doble clic para moverlas.", None)
        self.actualizar_info()
        self.dibujar()

    def clic_titulo(self, evento):
        """Pequeña sorpresa: al hacer clic varias veces en el título cae confeti.
        Recibe: el evento. Devuelve: nada.
        """
        self.clics_titulo += 1
        if self.clics_titulo >= CLICS_SECRETO:
            self.clics_titulo = 0
            self.mensaje("¡Jackpot! Encontraste el secreto del casino.", "pista")
            self.lanzar_confeti(True)

    def confirmar_nueva(self):
        """Pregunta antes de abandonar la partida actual.
        Recibe: nada. Devuelve: nada.
        """
        if self.terminada or messagebox.askyesno(
                "Nueva partida", "¿Empezar una partida nueva? Perderás el avance actual.",
                parent=self.ventana):
            self.nueva_partida()

    def tic(self):
        """Avanza el reloj un segundo. Recibe: nada. Devuelve: nada."""
        if not self.vivo:
            return
        if not self.terminada:
            self.segundos += 1
            self.actualizar_info()
        self.id_tic = self.ventana.after(1000, self.tic)

    def actualizar_info(self):
        """Muestra los movimientos y el tiempo. Recibe: nada. Devuelve: nada."""
        self.etiqueta_mov.config(text="Movimientos " + str(self.movimientos))
        self.etiqueta_tiempo.config(text="Tiempo " + self.texto_tiempo())
        total = self.contar_fundaciones()
        self.barra_fund.delete("all")
        if total > 0:
            self.barra_fund.create_rectangle(0, 0, 110 * total / 52, 10, fill=DORADO,
                                             outline="")
        self.etiqueta_prog.config(text=str(total) + "/52")

    def contar_fundaciones(self):
        """Recibe: nada. Devuelve: cuántas cartas hay en las 4 fundaciones."""
        total = 0
        for fundacion in self.tablero.fundaciones:
            total += fundacion.obtener_tamano()
        return total

    def alternar_sonido(self):
        """Activa o apaga los sonidos. Recibe: nada. Devuelve: nada."""
        self.sonido_activo = not self.sonido_activo
        self.boton_sonido.config(text="Sonido: sí" if self.sonido_activo else "Sonido: no")

    def sonido(self, tipo):
        """Toca un sonido corto en otro hilo, para no frenar el juego.
        Recibe: el tipo de sonido. Devuelve: nada.
        """
        if winsound is None or not self.sonido_activo:
            return
        notas = SONIDOS[tipo]

        def tocar():
            for frecuencia, duracion in notas:
                try:
                    winsound.Beep(frecuencia, duracion)
                except Exception:
                    return
        threading.Thread(target=tocar, daemon=True).start()

    def tecla(self, evento):
        """Atajos de teclado. Recibe: el evento. Devuelve: nada."""
        if self.animando or self.arrastre is not None:
            return
        tecla = evento.keysym.lower()
        if tecla == "space":
            if not self.terminada:
                self.robar()
        elif tecla == "h":
            self.dar_pista()
        elif tecla == "n" and not self.es_demo:
            self.confirmar_nueva()
        elif tecla == "u" or (tecla == "z" and evento.state & 4):
            self.deshacer()
        elif tecla == "e":
            self.abrir_capo()

    def texto_tiempo(self):
        """Recibe: nada. Devuelve: el tiempo jugado como mm:ss."""
        return "{:02d}:{:02d}".format(self.segundos // 60, self.segundos % 60)

    def humor(self, texto):
        """Recibe: un mensaje del tablero. Devuelve: una versión con humor si existe,
        o el mismo texto.
        """
        if texto in HUMOR:
            return random.choice(HUMOR[texto])
        return texto

    def mensaje(self, texto, exito):
        """Escribe un mensaje abajo. Recibe: el texto y True (bien), False (error),
        "pista" o None (neutro). Devuelve: nada.
        """
        if exito is True:
            color = EXITO
        elif exito is False:
            color = ERROR
        elif exito == "pista":
            color = DORADO
        else:
            color = TEXTO_SUAVE
        self.etiqueta_mensaje.config(text=texto, fg=color)

    def cartas_columna(self, indice):
        """Recibe: el índice de una columna (0 a 6).
        Devuelve: una lista de Python con sus cartas, solo para dibujar.
        """
        lista = []
        actual = self.tablero.columnas[indice].cabeza
        while actual is not None:
            lista.append(actual.dato)
            actual = actual.siguiente
        return lista

    # ------------------------------------------------------------------
    # Dibujo
    # ------------------------------------------------------------------
    def x_columna(self, indice):
        """Recibe: un índice de 0 a 6. Devuelve: la posición x de esa columna."""
        return MARGEN + indice * (CW + SEP)

    def rrect(self, x1, y1, x2, y2, radio, **opciones):
        """Dibuja un rectángulo de esquinas redondeadas.
        Recibe: las esquinas, el radio y las opciones de Tkinter. Devuelve: el item.
        """
        puntos = [x1 + radio, y1, x2 - radio, y1, x2, y1, x2, y1 + radio,
                  x2, y2 - radio, x2, y2, x2 - radio, y2, x1 + radio, y2,
                  x1, y2, x1, y2 - radio, x1, y1 + radio, x1, y1]
        return self.canvas.create_polygon(puntos, smooth=True, **opciones)

    def hueco(self, x, y, simbolo=None):
        """Dibuja el espacio vacío donde puede ir una carta.
        Recibe: x, y y un símbolo opcional. Devuelve: nada.
        """
        self.rrect(x, y, x + CW, y + CH, 10, fill=MESA_OSCURA, outline=MESA_BORDE,
                   width=2, dash=(5, 4), tags="tablero")
        if simbolo is not None:
            self.canvas.create_text(x + CW / 2, y + CH / 2, text=simbolo,
                                    fill=MESA_BORDE, font=self.f_simbolo_gde,
                                    tags="tablero")

    def dibujar_carta(self, x, y, carta, etiqueta="tablero", cara=None):
        """Dibuja una carta con su sombra.
        Recibe: la posición, la carta, la etiqueta del dibujo y cara
        (True/False para forzar el lado; None usa el estado de la carta).
        Devuelve: nada.
        """
        c = self.canvas
        visible = carta.boca_arriba if cara is None else cara
        self.rrect(x + 2, y + 3, x + CW + 2, y + CH + 3, 10, fill="#030f26",
                   outline="", tags=etiqueta)
        if not visible:
            self.rrect(x, y, x + CW, y + CH, 10, fill=AZUL_DORSO,
                       outline="#3d0d14", tags=etiqueta)
            self.rrect(x + 8, y + 8, x + CW - 8, y + CH - 8, 6, fill="",
                       outline=DORADO, tags=etiqueta)
            cx = x + CW / 2
            cy = y + CH / 2
            c.create_polygon(cx, cy - 26, cx + 18, cy, cx, cy + 26, cx - 18, cy,
                             fill="#a02c3a", outline=DORADO, tags=etiqueta)
            return

        color = ROJO if carta.color() == "rojo" else NEGRO
        simbolo = SIMBOLOS[carta.palo]
        rango = carta.nombre_valor()
        self.rrect(x, y, x + CW, y + CH, 10, fill=MARFIL, outline=MARFIL_BORDE,
                   tags=etiqueta)
        c.create_text(x + 9, y + 5, text=rango, anchor="nw", fill=color,
                      font=self.f_rango, tags=etiqueta)
        ancho_rango = self.f_rango.measure(rango)
        c.create_text(x + 13 + ancho_rango, y + 8, text=simbolo, anchor="nw",
                      fill=color, font=self.f_simbolo_peq, tags=etiqueta)
        if carta.valor >= 11:
            self.rrect(x + 12, y + 36, x + CW - 12, y + CH - 16, 8, fill="",
                       outline="#d9c58a", tags=etiqueta)
            c.create_text(x + CW / 2, y + CH / 2 + 2, text=rango, fill=color,
                          font=self.f_figura, tags=etiqueta)
            c.create_text(x + CW / 2, y + CH / 2 + 32, text=simbolo, fill=color,
                          font=self.f_simbolo_med, tags=etiqueta)
        else:
            c.create_text(x + CW / 2, y + CH / 2 + 6, text=simbolo, fill=color,
                          font=self.f_simbolo_gde, tags=etiqueta)
            c.create_text(x + CW - 9, y + CH - 6, text=simbolo, anchor="se",
                          fill=color, font=self.f_simbolo_peq, tags=etiqueta)

    def dibujar_carta_giro(self, x, y, carta, escala, frente):
        """Dibuja una carta a medio girar (animación al voltearse).
        Recibe: la posición, la carta, qué tan ancha se ve (0 a 1) y si ya muestra el frente.
        Devuelve: nada.
        """
        ancho = CW * escala
        x1 = x + (CW - ancho) / 2
        x2 = x1 + ancho
        radio = max(min(10, ancho / 2 - 1), 1)
        self.rrect(x1 + 2, y + 3, x2 + 2, y + CH + 3, radio, fill="#030f26",
                   outline="", tags="tablero")
        if frente:
            color = ROJO if carta.color() == "rojo" else NEGRO
            self.rrect(x1, y, x2, y + CH, radio, fill=MARFIL, outline=MARFIL_BORDE,
                       tags="tablero")
            if escala > 0.3:
                self.canvas.create_text((x1 + x2) / 2, y + CH / 2,
                                        text=SIMBOLOS[carta.palo], fill=color,
                                        font=self.f_simbolo_med, tags="tablero")
        else:
            self.rrect(x1, y, x2, y + CH, radio, fill=AZUL_DORSO, outline="#3d0d14",
                       tags="tablero")

    def animar_giro(self, columna, posicion):
        """Hace girar una carta que acaba de quedar boca arriba.
        Recibe: la columna y la posición de la carta. Devuelve: nada.
        """
        fases = [(0.7, False), (0.4, False), (0.12, False),
                 (0.12, True), (0.4, True), (0.7, True)]
        self.animando = True
        self.paso_giro(columna, posicion, fases, self.ficha_giro)

    def paso_giro(self, columna, posicion, fases, ficha):
        """Un cuadro de la animación de giro.
        Recibe: la carta, los cuadros que faltan y la ficha que identifica la partida.
        Devuelve: nada.
        """
        if not self.vivo or ficha != self.ficha_giro:
            return
        if not fases:
            self.giro = None
            self.animando = False
            self.dibujar()
            return
        escala, frente = fases[0]
        self.giro = (columna, posicion, escala, frente)
        self.dibujar()
        self.ventana.after(30, lambda: self.paso_giro(columna, posicion, fases[1:], ficha))

    def dibujar(self):
        """Redibuja todo el tablero con el estado actual.
        Recibe: nada. Devuelve: nada.
        """
        self.canvas.delete("tablero")
        self.canvas.delete("tip")
        self.zonas = []
        self.rect_cartas = {}
        self.rect_dest = {}
        self.rect_fund = {}

        oculto = None
        ocultar_robo = False
        if self.arrastre is not None:
            if self.arrastre["tipo"] == "col":
                oculto = (self.arrastre["col"], self.arrastre["indice"])
            else:
                ocultar_robo = True

        self.dibujar_fila_superior(ocultar_robo)
        for indice in range(7):
            self.dibujar_columna(indice, oculto)
        self.dibujar_resaltes()
        self.actualizar_capo()

    def dibujar_fila_superior(self, ocultar_robo):
        """Dibuja el mazo, la carta robada y las 4 fundaciones.
        Recibe: ocultar_robo (True si la carta robada se está arrastrando).
        Devuelve: nada.
        """
        t = self.tablero
        c = self.canvas

        x = self.x_columna(0)
        cantidad = t.mazo_robo.obtener_tamano()
        self.hueco(x, FILA_Y)
        if cantidad > 0:
            if cantidad > 2:
                self.dibujar_carta(x + 4, FILA_Y + 4, t.mazo_robo.cabeza.dato,
                                   cara=False)
            self.dibujar_carta(x, FILA_Y, t.mazo_robo.cabeza.dato, cara=False)
            self.zonas.append(((x, FILA_Y, x + CW, FILA_Y + CH), "mazo", None, None))
            if cantidad == 1:
                texto = "1 carta"
            else:
                texto = str(cantidad) + " cartas"
        else:
            texto = "Mazo vacío"
        c.create_text(x + CW / 2, FILA_Y + CH + 16, text=texto, fill=TEXTO_SUAVE,
                      font=self.f_pequena, tags="tablero")

        x = self.x_columna(1)
        self.hueco(x, FILA_Y)
        if t.nodo_robo is not None and not ocultar_robo:
            self.dibujar_carta(x, FILA_Y, t.nodo_robo.dato, cara=True)
            self.zonas.append(((x, FILA_Y, x + CW, FILA_Y + CH), "robo", None, None))
        if t.nodo_robo is not None:
            c.create_text(x + CW / 2, FILA_Y + CH + 16, text="Carta a la vista",
                          fill=TEXTO_SUAVE, font=self.f_pequena, tags="tablero")

        for indice in range(4):
            x = self.x_columna(3 + indice)
            palo = t.palos[indice]
            self.hueco(x, FILA_Y, SIMBOLOS[palo])
            fundacion = t.fundaciones[indice]
            if not fundacion.esta_vacia():
                self.dibujar_carta(x, FILA_Y, fundacion.ver_tope(), cara=True)
            self.rect_fund[indice] = (x, FILA_Y, x + CW, FILA_Y + CH)
            self.zonas.append((self.rect_fund[indice], "fund", indice, None))

    def dibujar_columna(self, indice, oculto):
        """Dibuja una columna del tablero y registra dónde se puede hacer clic.
        Recibe: el índice (0 a 6) y oculto (columna y posición desde la que las cartas
        se están arrastrando, o None). Devuelve: nada.
        """
        x = self.x_columna(indice)
        cartas = self.cartas_columna(indice)
        if oculto is not None and oculto[0] == indice:
            cartas = cartas[:oculto[1]]
        self.hueco(x, COL_Y)
        total = len(cartas)
        if total == 0:
            self.rect_dest[indice] = (x, COL_Y, x + CW, COL_Y + CH)
            self.zonas.append(((x, COL_Y, x + CW, COL_Y + CH), "vacia", indice, None))
            return

        paso_abajo = 12
        paso_arriba = 30
        suma = 0
        for carta in cartas[:-1]:
            suma += paso_arriba if carta.boca_arriba else paso_abajo
        libre = ALTO - 12 - COL_Y - CH
        escala = 1.0
        if suma > libre:
            escala = max(libre / suma, 0.4)

        y = COL_Y
        for posicion in range(total):
            carta = cartas[posicion]
            es_ultima = posicion == total - 1
            if es_ultima:
                paso = 0
                alto_zona = CH
            else:
                paso = (paso_arriba if carta.boca_arriba else paso_abajo) * escala
                alto_zona = paso
            if self.giro is not None and self.giro[0] == indice and self.giro[1] == posicion:
                self.dibujar_carta_giro(x, y, carta, self.giro[2], self.giro[3])
            else:
                self.dibujar_carta(x, y, carta)
            self.zonas.append(((x, y, x + CW, y + alto_zona), "carta", indice, posicion))
            self.rect_cartas[(indice, posicion)] = y
            if es_ultima:
                self.rect_dest[indice] = (x, y, x + CW, y + CH)
            y += paso

    def dibujar_resaltes(self):
        """Dibuja los marcos dorados de los destinos válidos y de la pista.
        Recibe: nada. Devuelve: nada.
        """
        rects = list(self.rects_pista)
        for tipo, indice in self.destinos:
            if tipo == "col":
                rects.append(self.rect_dest[indice])
            else:
                rects.append(self.rect_fund[indice])
        for x1, y1, x2, y2 in rects:
            self.rrect(x1 - 4, y1 - 4, x2 + 4, y2 + 4, 12, fill="", outline=DORADO,
                       width=3, tags="tablero")

    # ------------------------------------------------------------------
    # Ratón: clic, arrastre y doble clic
    # ------------------------------------------------------------------
    def zona_en(self, x, y):
        """Recibe: un punto. Devuelve: la zona de arriba en ese punto, o None."""
        for zona in reversed(self.zonas):
            x1, y1, x2, y2 = zona[0]
            if x1 <= x <= x2 and y1 <= y <= y2:
                return zona
        return None

    def pasar_mouse(self, evento):
        """Cambia el cursor a una mano sobre lo que se puede usar y, si el mouse
        se queda quieto, muestra qué estructura de datos hay ahí.
        Recibe: el evento. Devuelve: nada.
        """
        self.ocultar_tip()
        if self.animando or self.arrastre is not None:
            return
        zona = self.zona_en(evento.x, evento.y)
        usable = False
        if zona is not None and not self.terminada:
            tipo = zona[1]
            if tipo in ("mazo", "robo"):
                usable = True
            elif tipo == "carta":
                usable = self.cartas_columna(zona[2])[zona[3]].boca_arriba
        self.canvas.config(cursor="hand2" if usable else "")
        if zona is not None:
            texto = self.texto_estructura(zona)
            if texto is not None:
                x, y = evento.x, evento.y
                self.id_tip = self.ventana.after(600, lambda: self.mostrar_tip(x, y, texto))

    def texto_estructura(self, zona):
        """Recibe: una zona del tablero. Devuelve: el nombre de la estructura de datos
        que la guarda, o None.
        """
        tipo = zona[1]
        if tipo in ("mazo", "robo"):
            return "Lista circular: mazo de robo"
        if tipo in ("carta", "vacia"):
            return "Lista doblemente enlazada: columna " + str(zona[2] + 1)
        if tipo == "fund":
            return "Pila: fundación de " + SIMBOLOS[self.tablero.palos[zona[2]]]
        return None

    def mostrar_tip(self, x, y, texto):
        """Dibuja el cartelito de una estructura junto al mouse.
        Recibe: la posición y el texto. Devuelve: nada.
        """
        self.id_tip = None
        if not self.vivo:
            return
        ancho = self.f_pequena.measure(texto) + 22
        px = min(x + 14, ANCHO - ancho - 10)
        py = min(y + 16, ALTO - 40)
        self.rrect(px, py, px + ancho, py + 26, 8, fill=BARRA, outline=DORADO,
                   tags="tip")
        self.canvas.create_text(px + ancho / 2, py + 13, text=texto, fill=TEXTO,
                                font=self.f_pequena, tags="tip")

    def ocultar_tip(self):
        """Borra el cartelito y cancela el que estaba por aparecer.
        Recibe: nada. Devuelve: nada.
        """
        if self.id_tip is not None:
            self.ventana.after_cancel(self.id_tip)
            self.id_tip = None
        self.canvas.delete("tip")

    def presionar(self, evento):
        """Empieza un posible arrastre o clic. Recibe: el evento. Devuelve: nada."""
        self.ocultar_tip()
        self.candidato = None
        if self.animando or self.terminada:
            return
        zona = self.zona_en(evento.x, evento.y)
        if zona is None:
            return
        rect, tipo, a, b = zona
        if tipo == "mazo":
            self.candidato = {"tipo": "mazo"}
            return
        if tipo == "carta":
            cartas = self.cartas_columna(a)
            if not cartas[b].boca_arriba:
                return
            grupo = cartas[b:]
            ox = rect[0]
            oy = self.rect_cartas[(a, b)]
            desfases = []
            for k in range(len(grupo)):
                desfases.append(self.rect_cartas[(a, b + k)] - oy)
            self.candidato = {"tipo": "col", "col": a, "indice": b, "cartas": grupo,
                              "ox": ox, "oy": oy, "desfases": desfases}
        elif tipo == "robo":
            self.candidato = {"tipo": "robo", "cartas": [self.tablero.nodo_robo.dato],
                              "ox": rect[0], "oy": rect[1], "desfases": [0]}
        else:
            return
        self.candidato["inicio"] = (evento.x, evento.y)

    def arrastrar(self, evento):
        """Mueve las cartas que se están arrastrando.
        Recibe: el evento. Devuelve: nada.
        """
        cand = self.candidato
        if self.animando or cand is None or cand["tipo"] == "mazo":
            return
        if self.arrastre is None:
            lejos = abs(evento.x - cand["inicio"][0]) + abs(evento.y - cand["inicio"][1])
            if lejos < 6:
                return
            self.iniciar_arrastre()
        self.canvas.move("arrastre", evento.x - self.ultimo[0], evento.y - self.ultimo[1])
        self.ultimo = (evento.x, evento.y)
        self.pos = (cand["ox"] + evento.x - cand["inicio"][0],
                    cand["oy"] + evento.y - cand["inicio"][1])

    def iniciar_arrastre(self):
        """Levanta las cartas del tablero y marca a dónde pueden ir.
        Recibe: nada. Devuelve: nada.
        """
        cand = self.candidato
        self.arrastre = cand
        self.destinos = self.calcular_destinos(cand)
        self.ultimo = cand["inicio"]
        self.pos = (cand["ox"], cand["oy"])
        self.dibujar()
        for k in range(len(cand["cartas"])):
            self.dibujar_carta(cand["ox"], cand["oy"] + cand["desfases"][k],
                               cand["cartas"][k], etiqueta="arrastre", cara=True)
        self.canvas.tag_raise("arrastre")
        self.canvas.config(cursor="fleur")

    def calcular_destinos(self, cand):
        """Revisa a qué columnas y fundación puede ir lo que se arrastra.
        Recibe: el candidato. Devuelve: una lista de pares (tipo, índice).
        """
        t = self.tablero
        base = cand["cartas"][0]
        destinos = []
        for indice in range(7):
            if cand["tipo"] == "col" and indice == cand["col"]:
                continue
            if t._cabe_en_columna(base, t.columnas[indice])[0]:
                destinos.append(("col", indice))
        if len(cand["cartas"]) == 1 and t._cabe_en_fundacion(base)[0]:
            destinos.append(("fund", t.palos.index(base.palo)))
        return destinos

    def soltar(self, evento):
        """Termina un clic o un arrastre. Recibe: el evento. Devuelve: nada."""
        cand = self.candidato
        self.candidato = None
        if self.animando or cand is None:
            return
        if cand["tipo"] == "mazo":
            zona = self.zona_en(evento.x, evento.y)
            if zona is not None and zona[1] == "mazo":
                self.robar()
            return
        if self.arrastre is None:
            return

        cx = self.pos[0] + CW / 2
        cy = self.pos[1] + CH / 2
        destino = self.objetivo(cx, cy)
        if destino is None or (cand["tipo"] == "col" and destino == ("col", cand["col"])):
            self.volver()
            return
        self.previo = capturar_estado(self.tablero, self.movimientos)
        respuesta = self.intentar(cand, destino)
        if respuesta[0]:
            self.arrastre = None
            self.destinos = []
            self.ejecutar(respuesta)
        else:
            self.mensaje(self.humor(respuesta[1]), False)
            self.sonido("error")
            self.volver()

    def objetivo(self, cx, cy):
        """Recibe: el centro de la carta soltada.
        Devuelve: ("col", i), ("fund", i) o None si cayó fuera de todo.
        """
        if cy < COL_Y - 14:
            for indice in range(4):
                x = self.x_columna(3 + indice)
                if x - SEP / 2 <= cx <= x + CW + SEP / 2:
                    return ("fund", indice)
            return None
        for indice in range(7):
            x = self.x_columna(indice)
            if x - SEP / 2 <= cx <= x + CW + SEP / 2:
                return ("col", indice)
        return None

    def intentar(self, cand, destino):
        """Pide al tablero hacer el movimiento.
        Recibe: lo que se arrastra y el destino. Devuelve: (se_movio, mensaje).
        """
        t = self.tablero
        tipo, indice = destino
        if tipo == "col":
            if cand["tipo"] == "col":
                return t.mover_columna(cand["col"] + 1, indice + 1, len(cand["cartas"]))
            return t.mover_robo_a_columna(indice + 1)
        if len(cand["cartas"]) > 1:
            return False, "A las fundaciones se sube una carta a la vez"
        carta = cand["cartas"][0]
        if carta.palo != t.palos[indice]:
            return False, "Esa carta va en la fundación de " + SIMBOLOS[carta.palo]
        if cand["tipo"] == "col":
            return t.mover_a_fundacion(cand["col"] + 1)
        return t.mover_robo_a_fundacion()

    def volver(self):
        """Devuelve deslizando las cartas a su lugar. Recibe: nada. Devuelve: nada."""
        self.animando = True
        pasos = 8
        dx = (self.arrastre["ox"] - self.pos[0]) / pasos
        dy = (self.arrastre["oy"] - self.pos[1]) / pasos
        self.paso_volver(pasos, dx, dy)

    def paso_volver(self, restantes, dx, dy):
        """Un cuadro de la animación de regreso.
        Recibe: cuadros que faltan y el avance en x e y. Devuelve: nada.
        """
        if not self.vivo:
            return
        if restantes > 0:
            self.canvas.move("arrastre", dx, dy)
            self.ventana.after(14, lambda: self.paso_volver(restantes - 1, dx, dy))
            return
        self.canvas.delete("arrastre")
        self.arrastre = None
        self.destinos = []
        self.animando = False
        self.canvas.config(cursor="")
        self.dibujar()

    def doble_clic(self, evento):
        """Manda una carta donde pueda ir, sin arrastrar.
        Recibe: el evento. Devuelve: nada.
        """
        if self.animando or self.terminada:
            return
        zona = self.zona_en(evento.x, evento.y)
        if zona is None:
            return
        t = self.tablero
        tipo = zona[1]
        self.previo = capturar_estado(t, self.movimientos)
        if tipo == "robo":
            respuesta = t.mover_robo_a_fundacion()
            if not respuesta[0]:
                destino = self.columna_para(t.nodo_robo.dato, -1)
                if destino is not None:
                    respuesta = t.mover_robo_a_columna(destino + 1)
            self.ejecutar(respuesta)
        elif tipo == "carta":
            indice, posicion = zona[2], zona[3]
            cartas = self.cartas_columna(indice)
            if not cartas[posicion].boca_arriba:
                return
            respuesta = (False, "Esa carta no tiene a dónde ir por ahora")
            if posicion == len(cartas) - 1:
                respuesta = t.mover_a_fundacion(indice + 1)
            if not respuesta[0]:
                carta = cartas[posicion]
                inutil = carta.valor == 13 and posicion == 0
                destino = None if inutil else self.columna_para(carta, indice)
                if destino is not None:
                    respuesta = t.mover_columna(indice + 1, destino + 1,
                                                len(cartas) - posicion)
                else:
                    respuesta = (False, "Esa carta no tiene a dónde ir por ahora")
            self.ejecutar(respuesta)

    def columna_para(self, carta, excluir):
        """Busca la primera columna que acepta una carta.
        Recibe: la carta y una columna a ignorar (-1 para ninguna).
        Devuelve: el índice de la columna, o None.
        """
        for indice in range(7):
            if indice != excluir:
                if self.tablero._cabe_en_columna(carta, self.tablero.columnas[indice])[0]:
                    return indice
        return None

    # ------------------------------------------------------------------
    # Jugadas
    # ------------------------------------------------------------------
    def tipo_sonido(self, mensaje):
        """Recibe: el mensaje de una jugada hecha. Devuelve: el nombre del sonido."""
        if mensaje.startswith("Robaste"):
            return "robar"
        if mensaje == "Carta enviada a la fundación":
            return "fundacion"
        return "mover"

    def cartas_volteadas(self, previo):
        """Busca las cartas de las columnas que acaban de quedar boca arriba.
        Recibe: la foto del tablero antes de la jugada.
        Devuelve: una lista de pares (columna, posición).
        """
        antes = {}
        for carta, cara in previo["caras"]:
            antes[id(carta)] = cara
        volteadas = []
        for indice in range(7):
            cartas = self.cartas_columna(indice)
            for posicion in range(len(cartas)):
                if cartas[posicion].boca_arriba and antes.get(id(cartas[posicion])) is False:
                    volteadas.append((indice, posicion))
        return volteadas

    def ejecutar(self, respuesta):
        """Muestra el resultado de una jugada, la cuenta, la guarda para deshacer
        y revisa si ganó.
        Recibe: una pareja (se_movio, mensaje). Devuelve: nada.
        """
        se_movio, mensaje = respuesta
        previo = self.previo
        self.previo = None
        self.mensaje(self.humor(mensaje), se_movio)
        volteadas = []
        if se_movio:
            self.movimientos += 1
            if previo is not None:
                self.historial.apilar(previo)
                volteadas = self.cartas_volteadas(previo)
            self.sonido(self.tipo_sonido(mensaje))
        else:
            self.sonido("error")
        self.actualizar_info()
        self.quitar_pista(redibujar=False)
        self.canvas.delete("arrastre")
        self.canvas.config(cursor="")
        self.dibujar()
        if self.tablero.ha_ganado():
            self.ganar()
        elif volteadas:
            self.animar_giro(volteadas[0][0], volteadas[0][1])

    def respuesta_robar(self):
        """Roba una carta del mazo. Recibe: nada.
        Devuelve: una pareja (se_movio, mensaje).
        """
        carta = self.tablero.robar()
        if carta is None:
            return False, "El mazo de robo está vacío"
        return True, "Robaste: " + carta.como_texto()

    def robar(self):
        """Roba una carta del mazo. Recibe: nada. Devuelve: nada."""
        self.previo = capturar_estado(self.tablero, self.movimientos)
        self.ejecutar(self.respuesta_robar())

    def deshacer(self):
        """Vuelve a la foto guardada antes de la última jugada.
        Recibe: nada. Devuelve: nada.
        """
        if self.terminada or self.animando or self.arrastre is not None:
            return
        if self.historial.esta_vacia():
            self.mensaje("No hay jugadas para deshacer", False)
            return
        self.quitar_pista(redibujar=False)
        estado = self.historial.desapilar()
        self.movimientos = restaurar_estado(self.tablero, estado)
        self.actualizar_info()
        self.mensaje("Jugada deshecha", "pista")
        self.sonido("deshacer")
        self.dibujar()

    def alternar_auto(self):
        """Empieza o detiene la demostración automática.
        Recibe: nada. Devuelve: nada.
        """
        if self.auto:
            self.detener_auto()
            self.mensaje("Autojugar detenido", None)
            return
        if self.terminada:
            return
        self.auto = True
        self.auto_pasos = 0
        self.auto_sin_avance = 0
        self.auto_fund = self.contar_fundaciones()
        self.boton_auto.config(text="Detener")
        self.paso_auto()

    def detener_auto(self):
        """Para la demostración automática. Recibe: nada. Devuelve: nada."""
        self.auto = False
        if self.id_auto is not None:
            self.ventana.after_cancel(self.id_auto)
            self.id_auto = None
        boton = getattr(self, "boton_auto", None)
        if boton is not None:
            boton.config(text="Autojugar")

    def paso_auto(self):
        """Elige la próxima jugada, la marca y programa su ejecución.
        Recibe: nada. Devuelve: nada.
        """
        self.id_auto = None
        if not self.vivo or not self.auto:
            return
        if self.terminada or self.auto_pasos >= 120 or self.auto_sin_avance >= 25:
            self.detener_auto()
            return
        if self.animando or self.arrastre is not None:
            self.id_auto = self.ventana.after(200, self.paso_auto)
            return
        texto, rects, accion = self.buscar_pista()
        self.rects_pista = rects
        self.mensaje("Autojugar: " + texto, "pista")
        self.dibujar()
        self.id_auto = self.ventana.after(550, lambda: self.ejecutar_auto(accion))

    def ejecutar_auto(self, accion):
        """Hace la jugada elegida por la demostración automática.
        Recibe: la función que hace la jugada. Devuelve: nada.
        """
        self.id_auto = None
        if not self.vivo or not self.auto:
            return
        self.previo = capturar_estado(self.tablero, self.movimientos)
        self.auto_pasos += 1
        self.ejecutar(accion())
        total = self.contar_fundaciones()
        if total > self.auto_fund:
            self.auto_fund = total
            self.auto_sin_avance = 0
        else:
            self.auto_sin_avance += 1
        if self.auto and not self.terminada:
            self.id_auto = self.ventana.after(450, self.paso_auto)

    # ------------------------------------------------------------------
    # Pista
    # ------------------------------------------------------------------
    def rect_grupo(self, indice, posicion):
        """Recibe: una columna y una posición. Devuelve: el rectángulo que cubre
        desde esa carta hasta el final de la columna.
        """
        x = self.x_columna(indice)
        y1 = self.rect_cartas[(indice, posicion)]
        total = len(self.cartas_columna(indice))
        y2 = self.rect_cartas[(indice, total - 1)] + CH
        return (x, y1, x + CW, y2)

    def rect_robo(self):
        """Recibe: nada. Devuelve: el rectángulo de la carta robada."""
        x = self.x_columna(1)
        return (x, FILA_Y, x + CW, FILA_Y + CH)

    def buscar_pista(self):
        """Busca una jugada útil.
        Recibe: nada. Devuelve: una tripleta (texto, rectángulos a marcar,
        función que hace la jugada).
        """
        t = self.tablero
        if t.nodo_robo is not None:
            carta = t.nodo_robo.dato
            if t._cabe_en_fundacion(carta)[0]:
                return ("sube la carta robada a su fundación",
                        [self.rect_robo(), self.rect_fund[t.palos.index(carta.palo)]],
                        t.mover_robo_a_fundacion)
        for indice in range(7):
            cartas = self.cartas_columna(indice)
            if cartas and cartas[-1].boca_arriba and t._cabe_en_fundacion(cartas[-1])[0]:
                palo = t.palos.index(cartas[-1].palo)
                return ("sube " + cartas[-1].como_texto() + " a la fundación",
                        [self.rect_grupo(indice, len(cartas) - 1), self.rect_fund[palo]],
                        lambda i=indice: t.mover_a_fundacion(i + 1))
        for exigir_voltear in (True, False):
            for indice in range(7):
                cartas = self.cartas_columna(indice)
                for posicion in range(len(cartas)):
                    carta = cartas[posicion]
                    if not carta.boca_arriba:
                        continue
                    if carta.valor == 13 and posicion == 0:
                        continue
                    anterior = cartas[posicion - 1] if posicion > 0 else None
                    voltea = anterior is not None and not anterior.boca_arriba
                    if exigir_voltear and not voltea:
                        continue
                    if (anterior is not None and anterior.boca_arriba
                            and anterior.valor == carta.valor + 1
                            and anterior.color() != carta.color()):
                        continue
                    destino = self.columna_para(carta, indice)
                    if destino is not None:
                        cantidad = len(cartas) - posicion
                        return ("mueve " + carta.como_texto() + " a la columna "
                                + str(destino + 1),
                                [self.rect_grupo(indice, posicion), self.rect_dest[destino]],
                                lambda i=indice, d=destino, n=cantidad:
                                t.mover_columna(i + 1, d + 1, n))
        if t.nodo_robo is not None:
            destino = self.columna_para(t.nodo_robo.dato, -1)
            if destino is not None:
                return ("baja la carta robada a la columna " + str(destino + 1),
                        [self.rect_robo(), self.rect_dest[destino]],
                        lambda d=destino: t.mover_robo_a_columna(d + 1))
        x = self.x_columna(0)
        return ("roba una carta del mazo", [(x, FILA_Y, x + CW, FILA_Y + CH)],
                self.respuesta_robar)

    def dar_pista(self):
        """Marca en dorado una jugada posible. Recibe: nada. Devuelve: nada."""
        if self.terminada or self.animando or self.arrastre is not None:
            return
        texto, rects, accion = self.buscar_pista()
        self.quitar_pista(redibujar=False)
        self.rects_pista = rects
        self.mensaje("Pista: " + texto, "pista")
        self.dibujar()
        self.id_pista = self.ventana.after(2500, self.quitar_pista)

    def quitar_pista(self, redibujar=True):
        """Borra los marcos de la pista.
        Recibe: redibujar (True para actualizar la pantalla). Devuelve: nada.
        """
        if self.id_pista is not None:
            self.ventana.after_cancel(self.id_pista)
            self.id_pista = None
        if self.rects_pista:
            self.rects_pista = []
            if redibujar and self.vivo:
                self.dibujar()

    # ------------------------------------------------------------------
    # Panel de estructuras en vivo
    # ------------------------------------------------------------------
    def abrir_capo(self):
        """Abre la ventana que muestra las estructuras de datos funcionando.
        Recibe: nada. Devuelve: nada.
        """
        if self.capo is not None:
            self.capo.lift()
            return
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Estructuras en vivo")
        ventana.configure(bg=BARRA)
        ventana.resizable(False, False)
        ventana.protocol("WM_DELETE_WINDOW", self.cerrar_capo)
        centrar(ventana, 560, 620)
        tk.Label(ventana, text="Estructuras en vivo", bg=BARRA, fg=TEXTO,
                 font=(FUENTE_TITULO, 20, "bold")).pack(pady=(16, 2))
        tk.Label(ventana, text="Así están las estructuras de datos ahora mismo",
                 bg=BARRA, fg=TEXTO_SUAVE, font=(FUENTE_UI, 10)).pack(pady=(0, 10))
        self.texto_capo = tk.Text(ventana, bg=MESA_OSCURA, fg=TEXTO, relief="flat",
                                  font=("Consolas", 10), width=64, height=30,
                                  padx=14, pady=10, wrap="none", state="disabled",
                                  cursor="arrow")
        self.texto_capo.tag_configure("titulo", foreground=DORADO,
                                      font=("Consolas", 10, "bold"))
        self.texto_capo.pack(padx=18, pady=(0, 16))
        self.capo = ventana
        self.actualizar_capo()

    def cerrar_capo(self):
        """Cierra el panel de estructuras. Recibe: nada. Devuelve: nada."""
        if self.capo is not None:
            self.capo.destroy()
            self.capo = None

    def actualizar_capo(self):
        """Refresca el panel de estructuras si está abierto.
        Recibe: nada. Devuelve: nada.
        """
        if self.capo is None:
            return
        t = self.tablero
        lineas = [("PILA  (4 fundaciones)", True)]
        for indice in range(4):
            fundacion = t.fundaciones[indice]
            if fundacion.esta_vacia():
                tope = "vacía"
            else:
                tope = fundacion.ver_tope().nombre_valor()
            lineas.append(("  " + SIMBOLOS[t.palos[indice]] + "  "
                           + str(fundacion.obtener_tamano()).rjust(2)
                           + " cartas   tope: " + tope, False))
        lineas.append(("", False))
        lineas.append(("LISTA CIRCULAR  (mazo de robo)", True))
        lineas.append(("  " + str(t.mazo_robo.obtener_tamano()) + " cartas", False))
        if t.nodo_robo is None:
            lineas.append(("  nodo actual: ninguno todavía", False))
        else:
            posicion = 1
            actual = t.mazo_robo.cabeza
            while actual is not t.nodo_robo and posicion < t.mazo_robo.obtener_tamano():
                actual = actual.siguiente
                posicion += 1
            lineas.append(("  nodo actual: " + str(posicion) + " de "
                           + str(t.mazo_robo.obtener_tamano()) + "  ("
                           + t.nodo_robo.dato.como_texto() + ")", False))
        lineas.append(("", False))
        lineas.append(("DOBLE LISTA ENLAZADA  (7 columnas)", True))
        for indice in range(7):
            cartas = self.cartas_columna(indice)
            abajo = 0
            for carta in cartas:
                if not carta.boca_arriba:
                    abajo += 1
            lineas.append(("  columna " + str(indice + 1) + ": "
                           + str(t.columnas[indice].obtener_tamano()).rjust(2)
                           + " cartas, " + str(abajo) + " boca abajo", False))
        lineas.append(("", False))
        lineas.append(("PILA  (historial de Deshacer)", True))
        lineas.append(("  " + str(self.historial.obtener_tamano())
                       + " jugadas guardadas", False))
        lineas.append(("", False))
        lineas.append(("También en uso: Cola al repartir, Pila al barajar y al mover", False))
        lineas.append(("grupos, y un Árbol binario de búsqueda para los puntajes.", False))

        self.texto_capo.config(state="normal")
        self.texto_capo.delete("1.0", "end")
        for texto, es_titulo in lineas:
            if es_titulo:
                self.texto_capo.insert("end", texto + "\n", "titulo")
            else:
                self.texto_capo.insert("end", texto + "\n")
        self.texto_capo.config(state="disabled")

    # ------------------------------------------------------------------
    # Final de la partida
    # ------------------------------------------------------------------
    def ganar(self):
        """Celebra la victoria y guarda el puntaje en el árbol (menos en la demostración).
        Recibe: nada. Devuelve: nada.
        """
        self.terminada = True
        if not self.es_demo:
            self.menu.puntajes.registrar(self.movimientos)
        self.mensaje("¡Completaste las 4 fundaciones!", True)
        self.sonido("ganar")
        self.lanzar_confeti()
        self.ventana.after(900, self.mostrar_panel_final)

    def lanzar_confeti(self, siempre=False):
        """Crea las piezas de confeti y empieza a moverlas.
        Recibe: nada. Devuelve: nada.
        """
        colores = [DORADO, ROJO, MARFIL, "#7cd6a8", "#8ab4f8"]
        piezas = []
        for _ in range(70):
            x = random.randint(0, ANCHO)
            y = random.randint(-ALTO, 0)
            simbolo = random.choice(list(SIMBOLOS.values()))
            tamano = random.randint(14, 28)
            item = self.canvas.create_text(
                x, y, text=simbolo, fill=random.choice(colores),
                font=(FUENTE_SIMBOLO, tamano), tags="confeti")
            piezas.append((item, random.uniform(-1.2, 1.2), random.uniform(2.5, 6)))
        self.paso_confeti(piezas, 90 if siempre else 260, siempre)

    def paso_confeti(self, piezas, restantes, siempre=False):
        """Un cuadro de la animación del confeti.
        Recibe: las piezas y los cuadros que faltan. Devuelve: nada.
        """
        if not self.vivo or not (self.terminada or siempre):
            return
        if restantes <= 0:
            self.canvas.delete("confeti")
            return
        for item, vx, vy in piezas:
            self.canvas.move(item, vx, vy)
            posicion = self.canvas.coords(item)
            if posicion and posicion[1] > ALTO + 30:
                self.canvas.move(item, 0, -ALTO - 60)
        self.ventana.after(30, lambda: self.paso_confeti(piezas, restantes - 1, siempre))

    def mostrar_panel_final(self):
        """Muestra el cuadro de victoria con los botones.
        Recibe: nada. Devuelve: nada.
        """
        if not self.vivo or not self.terminada:
            return
        marco = tk.Frame(self.canvas, bg=BARRA, highlightbackground=DORADO,
                         highlightthickness=2, padx=44, pady=26)
        cara = tk.Canvas(marco, width=76, height=76, bg=BARRA, highlightthickness=0)
        cara.create_oval(4, 4, 72, 72, fill=DORADO, outline="#8a6d25", width=3)
        cara.create_rectangle(14, 26, 36, 40, fill=NEGRO, outline="")
        cara.create_rectangle(40, 26, 62, 40, fill=NEGRO, outline="")
        cara.create_line(36, 31, 40, 31, fill=NEGRO, width=3)
        cara.create_arc(18, 30, 58, 62, start=200, extent=140, style="arc",
                        outline=NEGRO, width=4)
        cara.pack(pady=(0, 6))
        tk.Label(marco, text="¡Ganaste!", bg=BARRA, fg=DORADO,
                 font=(FUENTE_TITULO, 34, "bold")).pack()
        tk.Label(marco, text=random.choice(FRASES_VICTORIA), bg=BARRA, fg=TEXTO,
                 font=(FUENTE_TITULO, 13, "italic")).pack(pady=(2, 0))
        tk.Label(marco, bg=BARRA, fg=TEXTO, font=(FUENTE_UI, 12),
                 text="Lo lograste en " + str(self.movimientos) + " movimientos y "
                 + self.texto_tiempo()).pack(pady=(6, 2))
        if self.es_demo:
            nota = "Era la demostración, el puntaje no se guarda."
        else:
            nota = "Tu puntaje quedó guardado."
        tk.Label(marco, text=nota, bg=BARRA, fg=TEXTO_SUAVE,
                 font=(FUENTE_UI, 10)).pack(pady=(0, 16))
        botones = tk.Frame(marco, bg=BARRA)
        botones.pack()
        crear_boton(botones, "Jugar de nuevo", self.nueva_partida,
                    primario=True).pack(side="left", padx=6)
        crear_boton(botones, "Volver al menú", self.cerrar).pack(side="left", padx=6)
        self.panel_final = marco
        self.canvas.create_window(ANCHO / 2, ALTO / 2, window=marco, tags="final")

    def rendirse(self):
        """El jugador se rinde y pierde. Recibe: nada. Devuelve: nada."""
        if self.terminada:
            self.cerrar()
            return
        if messagebox.askyesno("Rendirse", "¿Seguro que quieres rendirte?",
                               parent=self.ventana):
            messagebox.showinfo("Solitario", "Te rendiste. PERDISTE.",
                                parent=self.ventana)
            self.cerrar()

    def cerrar(self):
        """Cierra la ventana y detiene los relojes. Recibe: nada. Devuelve: nada."""
        self.vivo = False
        for identificador in (self.id_tic, self.id_pista, self.id_auto, self.id_tip):
            if identificador is not None:
                try:
                    self.ventana.after_cancel(identificador)
                except tk.TclError:
                    pass
        self.ventana.destroy()


class MenuPrincipal:
    """Menú principal del juego."""

    def __init__(self):
        """Crea la ventana del menú y la lista de puntajes."""
        self.raiz = tk.Tk()
        self.raiz.title("Solitario")
        self.raiz.configure(bg=MESA)
        self.raiz.resizable(False, False)
        centrar(self.raiz, 420, 700)
        self.puntajes = Puntajes()

        palos = tk.Frame(self.raiz, bg=MESA)
        palos.pack(pady=(44, 0))
        for simbolo, color in (("♠", TEXTO), ("♥", "#ff7a6e"), ("♣", TEXTO),
                               ("♦", "#ff7a6e")):
            tk.Label(palos, text=simbolo, bg=MESA, fg=color,
                     font=(FUENTE_SIMBOLO, 30)).pack(side="left", padx=8)

        tk.Label(self.raiz, text="Solitario", bg=MESA, fg=TEXTO,
                 font=(FUENTE_TITULO, 46, "bold")).pack(pady=(6, 0))
        tk.Label(self.raiz, text="Klondike clásico", bg=MESA, fg=DORADO,
                 font=(FUENTE_TITULO, 15, "italic")).pack(pady=(0, 30))

        self.crear_boton("Jugar", self.jugar, primario=True)
        self.crear_boton("Demostración", self.demostracion)
        self.crear_boton("Reglas", self.reglas)
        self.crear_boton("Mejores puntajes", self.ver_puntajes)
        self.crear_boton("Acerca del proyecto", self.acerca)
        self.crear_boton("Salir", self.raiz.destroy)

        tk.Label(self.raiz, text="Proyecto de Estructuras de Datos", bg=MESA,
                 fg=TEXTO_SUAVE, font=(FUENTE_UI, 9)).pack(side="bottom", pady=14)

    def crear_boton(self, texto, comando, primario=False):
        """Crea un botón del menú.
        Recibe: el texto, la función que se ejecuta al presionarlo y si es el principal.
        Devuelve: nada.
        """
        crear_boton(self.raiz, texto, comando, primario=primario, grande=True).pack(
            fill="x", padx=70, pady=6)

    def abrir_dialogo(self, titulo, ancho, alto):
        """Crea una ventana secundaria con el mismo estilo.
        Recibe: el título y el tamaño. Devuelve: la ventana.
        """
        dialogo = tk.Toplevel(self.raiz)
        dialogo.title(titulo)
        dialogo.configure(bg=BARRA)
        dialogo.resizable(False, False)
        dialogo.transient(self.raiz)
        centrar(dialogo, ancho, alto)
        dialogo.focus_set()
        return dialogo

    def jugar(self):
        """Abre una partida nueva. Recibe: nada. Devuelve: nada."""
        VentanaJuego(self, False)

    def demostracion(self):
        """Abre la partida con el tablero casi ganado. Recibe: nada. Devuelve: nada."""
        VentanaJuego(self, True)

    def reglas(self):
        """Muestra las reglas y los consejos de manejo.
        Recibe: nada. Devuelve: nada.
        """
        dialogo = self.abrir_dialogo("Reglas", 520, 560)
        tk.Label(dialogo, text="Reglas", bg=BARRA, fg=TEXTO,
                 font=(FUENTE_TITULO, 24, "bold")).pack(pady=(22, 10))
        for linea in REGLAS:
            tk.Label(dialogo, text="•  " + linea, bg=BARRA, fg=TEXTO, justify="left",
                     anchor="w", wraplength=450, font=(FUENTE_UI, 11)).pack(
                fill="x", padx=36, pady=3)
        tk.Label(dialogo, text="Cómo se juega", bg=BARRA, fg=DORADO,
                 font=(FUENTE_TITULO, 18, "bold")).pack(pady=(22, 8))
        for linea in CONSEJOS:
            tk.Label(dialogo, text="•  " + linea, bg=BARRA, fg=TEXTO, justify="left",
                     anchor="w", wraplength=450, font=(FUENTE_UI, 11)).pack(
                fill="x", padx=36, pady=3)
        crear_boton(dialogo, "Entendido", dialogo.destroy, primario=True).pack(
            side="bottom", pady=20)

    def acerca(self):
        """Muestra quiénes hicieron el proyecto y dónde se usa cada estructura.
        Recibe: nada. Devuelve: nada.
        """
        dialogo = self.abrir_dialogo("Acerca del proyecto", 600, 600)
        tk.Label(dialogo, text="Acerca del proyecto", bg=BARRA, fg=TEXTO,
                 font=(FUENTE_TITULO, 24, "bold")).pack(pady=(22, 4))
        tk.Label(dialogo, text="Solitario Klondike, proyecto final de Estructuras de Datos",
                 bg=BARRA, fg=DORADO, font=(FUENTE_TITULO, 12, "italic")).pack()
        tk.Label(dialogo, text="Jose Alejandro Jurado Bolaños y Juan David Hernandez Hernandez",
                 bg=BARRA, fg=TEXTO, font=(FUENTE_UI, 11)).pack(pady=(10, 2))
        tk.Label(dialogo, text="Hecho en Python con Tkinter. Las 5 estructuras se programaron "
                 "desde cero con nodos y referencias.", bg=BARRA, fg=TEXTO_SUAVE,
                 font=(FUENTE_UI, 10), wraplength=500).pack(pady=(0, 16))
        for nombre, uso in ESTRUCTURAS:
            fila = tk.Frame(dialogo, bg=BARRA)
            fila.pack(fill="x", padx=40, pady=4)
            tk.Label(fila, text=nombre, bg=BARRA, fg=DORADO, width=22, anchor="w",
                     font=(FUENTE_UI, 11, "bold")).pack(side="left")
            tk.Label(fila, text=uso, bg=BARRA, fg=TEXTO, anchor="w", justify="left",
                     wraplength=290, font=(FUENTE_UI, 10)).pack(side="left")
        tk.Label(dialogo, text="Dentro de una partida, el botón Estructuras muestra todo\n"
                 "esto funcionando en vivo.", bg=BARRA, fg=TEXTO_SUAVE,
                 font=(FUENTE_UI, 10)).pack(pady=(18, 0))
        crear_boton(dialogo, "Cerrar", dialogo.destroy, primario=True).pack(
            side="bottom", pady=20)

    def raiz_del_arbol(self):
        """Busca la raíz del árbol de puntajes.
        Recibe: nada. Devuelve: el nodo raíz, o None si no se encontró o está vacío.
        """
        try:
            candidatos = [self.puntajes] + list(vars(self.puntajes).values())
            for objeto in candidatos:
                for nombre in ("raiz", "root"):
                    if hasattr(objeto, nombre):
                        return getattr(objeto, nombre)
        except TypeError:
            pass
        return None

    def hijos_de(self, nodo):
        """Recibe: un nodo del árbol. Devuelve: una pareja (izquierdo, derecho)."""
        izquierdo = None
        derecho = None
        for nombre, valor in vars(nodo).items():
            bajo = nombre.lower()
            if "izq" in bajo or "left" in bajo:
                izquierdo = valor
            elif "der" in bajo or "right" in bajo:
                derecho = valor
        return izquierdo, derecho

    def valor_de(self, nodo):
        """Recibe: un nodo del árbol. Devuelve: el número que guarda."""
        datos = vars(nodo)
        for nombre in ("dato", "valor", "clave", "puntaje"):
            if nombre in datos:
                return datos[nombre]
        for valor in datos.values():
            if isinstance(valor, (int, float)) and not isinstance(valor, bool):
                return valor
        return "?"

    def dibujar_arbol(self, lienzo, raiz, ancho, alto):
        """Dibuja el árbol binario de búsqueda con círculos y líneas.
        Recibe: el lienzo, la raíz y el tamaño disponible. Devuelve: nada.
        """
        orden = []

        def recorrer(nodo, profundidad):
            if nodo is None:
                return
            izquierdo, derecho = self.hijos_de(nodo)
            recorrer(izquierdo, profundidad + 1)
            orden.append((nodo, profundidad))
            recorrer(derecho, profundidad + 1)

        recorrer(raiz, 0)
        if not orden:
            raise ValueError("árbol vacío")
        mayor = 0
        for _, profundidad in orden:
            mayor = max(mayor, profundidad)
        separacion = min(70, (ancho - 60) / max(len(orden) - 1, 1))
        paso_y = min(70, (alto - 70) / max(mayor, 1))
        radio = 19 if len(orden) <= 12 else 14
        posiciones = {}
        for numero in range(len(orden)):
            nodo, profundidad = orden[numero]
            posiciones[id(nodo)] = (30 + numero * separacion + (ancho - 60 -
                                    separacion * (len(orden) - 1)) / 2,
                                    36 + profundidad * paso_y)
        for nodo, _ in orden:
            x, y = posiciones[id(nodo)]
            for hijo in self.hijos_de(nodo):
                if hijo is not None and id(hijo) in posiciones:
                    hx, hy = posiciones[id(hijo)]
                    lienzo.create_line(x, y, hx, hy, fill=MESA_BORDE, width=2)
        for nodo, profundidad in orden:
            x, y = posiciones[id(nodo)]
            relleno = DORADO if profundidad == 0 else BOTON_HOVER
            color = NEGRO if profundidad == 0 else TEXTO
            lienzo.create_oval(x - radio, y - radio, x + radio, y + radio,
                               fill=relleno, outline=DORADO, width=2)
            lienzo.create_text(x, y, text=str(self.valor_de(nodo)), fill=color,
                               font=(FUENTE_UI, 10 if radio > 14 else 9, "bold"))

    def ver_puntajes(self):
        """Muestra los puntajes guardados en el árbol: dibujado y en lista.
        Recibe: nada. Devuelve: nada.
        """
        captura = io.StringIO()
        with redirect_stdout(captura):
            self.puntajes.mostrar()
        texto = captura.getvalue().strip()
        if texto == "":
            texto = "Todavía no hay puntajes.\nGana una partida para aparecer aquí."
        raiz = self.raiz_del_arbol()

        dialogo = self.abrir_dialogo("Mejores puntajes", 780 if raiz is not None else 420,
                                     720 if raiz is not None else 460)
        tk.Label(dialogo, text="Mejores puntajes", bg=BARRA, fg=TEXTO,
                 font=(FUENTE_TITULO, 24, "bold")).pack(pady=(22, 4))
        tk.Label(dialogo, text="Ordenados de menor a mayor número de movimientos",
                 bg=BARRA, fg=TEXTO_SUAVE, font=(FUENTE_UI, 10)).pack(pady=(0, 12))
        if raiz is not None:
            lienzo = tk.Canvas(dialogo, width=720, height=300, bg=MESA_OSCURA,
                               highlightthickness=1, highlightbackground=MESA_BORDE)
            lienzo.pack()
            try:
                self.dibujar_arbol(lienzo, raiz, 720, 300)
                tk.Label(dialogo, text="Árbol binario de búsqueda: los menores van a la "
                         "izquierda y los mayores a la derecha", bg=BARRA, fg=TEXTO_SUAVE,
                         font=(FUENTE_UI, 9)).pack(pady=(6, 10))
            except Exception:
                lienzo.destroy()
        tk.Label(dialogo, text=texto, bg=BARRA, fg=TEXTO, justify="left",
                 anchor="n", wraplength=360 if raiz is None else 700,
                 font=(FUENTE_UI, 12)).pack(fill="both", expand=True, padx=30)
        crear_boton(dialogo, "Cerrar", dialogo.destroy, primario=True).pack(
            side="bottom", pady=20)

    def iniciar(self):
        """Abre el menú y espera a que el usuario lo use. Recibe: nada. Devuelve: nada."""
        self.raiz.mainloop()