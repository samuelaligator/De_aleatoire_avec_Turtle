import turtle
import time
import random


# Classe Die : pour dessiner un dé en fonction de sa taille, son numéro et sa position (x et y)
class Die:
    DOT_COLOR = "red"
    DIE_COLOR = "white"

    def __init__(self, size, number, x, y):
        self.size = size
        self.number = number
        self.x = x
        self.y = y

        self.t = turtle.Turtle()  # Initialisation d'une tortue
        self.t.hideturtle()
        self.angle = 0
        self.spin = False
        self.previous_number = self.number
        self.border_radius = self.size // 10  # Pour avoir une bordure arrondie
        self.final_size = self.size - self.border_radius * 2
        self.x_or_y_dots_offset = self.final_size / 3  # Espacement des points
        self.dot_size = self.final_size // 4

    def move_the_mouse(self, distance1, distance2, rotation):
        # Déplace la tortue en fonction de son ancienne position
        self.t.up()
        self.t.forward(distance1)
        self.t.left(rotation)
        self.t.forward(distance2)
        self.t.down()

    def go_to(self, x, y):
        # Déplace la tortue à des coordonnées précises
        self.t.up()
        self.t.color("red")
        self.t.goto(x, y)
        self.t.down()

    def draw_die(self):
        # Dessine le dé
        self.t.setheading(self.angle)
        self.go_to(self.x, self.y)
        self.draw_outline()
        self.draw_die_face()

    def draw_outline(self):
        # Dessine le dé sans les points
        self.move_the_mouse(- self.final_size // 2 - self.border_radius, - self.final_size // 2, -90)
        self.t.color(Die.DIE_COLOR)
        self.t.begin_fill()
        for side in range(4):
            self.t.forward(self.final_size)
            self.t.circle(self.border_radius, 90)
        self.t.end_fill()
        self.move_the_mouse(self.final_size // 2, self.final_size // 2 + self.border_radius, 90)

    def draw_die_face(self):
        # Dessine les points d'une face du dé
        self.t.color(Die.DOT_COLOR)
        if self.number % 2 == 1:
            self.t.dot(self.dot_size)
        if self.number >= 2:
            self.layout1()
        if self.number >= 4:
            self.t.left(90)
            self.layout1()
            self.t.left(-90)
        if self.number == 6:
            self.layout2()

    def layout1(self):
        # Dessine le motif 1 des points (pour le numéro 2 et au-dessus)
        self.draw_dot_and_move(-self.x_or_y_dots_offset, -self.x_or_y_dots_offset, -90)
        self.draw_dot_and_move(self.x_or_y_dots_offset, self.x_or_y_dots_offset, -90)

    def layout2(self):
        # Dessine le motif 2 des points (juste pour le numéro 6)
        self.draw_dot_and_move(self.x_or_y_dots_offset, 0, 0)
        self.draw_dot_and_move(-self.x_or_y_dots_offset, 0, 0)

    def draw_dot_and_move(self, x, y, angle):
        # Dessine un point et se replace au milieu du dé
        self.move_the_mouse(x, y, angle)
        self.t.dot(self.dot_size)
        self.move_the_mouse(-x, -y, -angle)

    def spin_true(self):
        # Pour dire que le dé peut tourner
        self.spin = True

    def clear(self):
        # Pour effacer juste ce dé
        self.t.clear()


# Classe principal du programme
class Main:
    def __init__(self):
        self.s = turtle.Screen()  # Initialisation de l'écran
        self.s.tracer(0)
        self.s.bgcolor("black")
        self.s.setup(1.0, 1.0)  # La taille de la fenêtre est maximale
        self.s.title("Dé aléatoire")

        main_size = self.s.numinput("Enter the size of the die", "Entrez la taille du dé", 300, 50, 10000)
        self.main_die = Die(main_size, random.randint(1, 6), 0, main_size // 3)  # Initialise le dé principal
        self.turns_number = 2  # Nombre de tours que le dé va tourner
        self.turn = 0
        self.history_number = []  # Historique des faces déjà tombées
        self.main()

    def main(self):
        # Boucle principale qui dessine le dé principal et le fait tourner si on clique sur espace
        while True:
            self.main_die.clear()
            self.main_die.draw_die()
            if self.main_die.spin:
                self.turn_the_die()
            self.s.listen()
            self.s.onkeypress(self.main_die.spin_true, "space")  # Touche espace détectée ?
            self.s.onkeypress(self.s.bye, "Escape")  # Ferme la fenêtre si la touche d'échappement est pressée
            self.s.update()

    def turn_the_die(self):
        # Fait tourner le dé principal, change la face du dé et affiche l'historique des faces
        if self.turn < self.turns_number:
            if self.main_die.angle <= 180:
                self.main_die.angle += 1
                time.sleep((self.turn * 90 + self.main_die.angle) / 30000)  # Time.sleep pour ralentir le dé
            else:
                while self.main_die.previous_number == self.main_die.number:
                    self.main_die.number = random.randint(1, 6)
                self.main_die.previous_number = self.main_die.number
                self.main_die.angle = 0
                self.turn += 1
        else:
            self.turn = 0
            self.history_update(self.main_die.number)
            self.main_die.spin = False

    def history_update(self, number):
        # Affiche l'historique des faces déjà tombées
        self.history_number.append(number)
        size = self.main_die.final_size
        len_history = len(self.history_number) - 1

        # Change la position de du dernier dé de l'historique
        x = size // 3 * (len_history % 7)
        y = size // 3 * (len_history // 7)

        history_parameters = [size // 4, self.history_number[-1], -size + x, -size // 1.5 - y]
        die = Die(*history_parameters)  # Crée une instance de "Die" pour le dernier dé de l'historique
        die.draw_die()


# Crée une instance de la classe Main pour démarrer le programme
main = Main()
main.main()
