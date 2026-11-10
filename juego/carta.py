class Carta:
    """Una carta de la baraja: tiene valor, palo y si está boca arriba."""

    def __init__(self, valor, palo):
        """Crea una carta.
        Recibe: valor (1 a 13) y palo (corazones, diamantes, treboles, picas).
        Devuelve: nada (construye el objeto).
        """
        self.valor = valor
        self.palo = palo
        self.boca_arriba = False

    def color(self):
        """Recibe: nada. Devuelve: "rojo" o "negro" según el palo."""
        if self.palo == "corazones" or self.palo == "diamantes":
            return "rojo"
        return "negro"

    def nombre_valor(self):
        """Recibe: nada. Devuelve: A, 2 a 10, J, Q o K según el valor."""
        if self.valor == 1:
            return "A"
        if self.valor == 11:
            return "J"
        if self.valor == 12:
            return "Q"
        if self.valor == 13:
            return "K"
        return str(self.valor)

    def como_texto(self):
        """Recibe: nada. Devuelve: el texto de la carta, por ejemplo "K de picas"."""
        return self.nombre_valor() + " de " + self.palo