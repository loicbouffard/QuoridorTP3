'''Module de la classe du jeu QuoridorX'''
import turtle
import quoridor


class QuoridorX(quoridor.Quoridor):
    '''Constructeur d'un jeu Quoridor graphique'''

    def __init__(self, joueur, murs=None):
        super().__init__(joueur, murs)
        self.turtle_j1 = turtle.Turtle()
        self.turtle_j2 = turtle.Turtle()

    def afficher(self):
        '''Affiche le jeu Quoridor graphique'''

        fen = turtle.Screen()
        fen.title("Quoridor")
        fen.setup(width=700, height=600)
        point_tab = ((-200, 250), (250, 250), (250, -200), (-200, -200), (-200, 250),
                     (-150, 250), (-150, -200), (-100, -
                                                 200), (-100, 250), (-50, 250),
                     (-50, -200), (0, -200), (0, 250), (50,
                                                        250), (50, -200), (100, -200),
                     (100, 250), (150, 250), (150, -200), (200, -200), (200, 250),
                     (250, 250), (250, 200), (-200,
                                              200), (-200, 150), (250, 150), (250, 100),
                     (-200, 100), (-200, 50), (250,
                                               50), (250, 0), (-200, 0), (-200, -50),
                     (250, -50), (250, -100), (-200, -100), (-200, -150), (250, -150))

        tab = turtle.Turtle()
        tab.hideturtle()
        tab.speed(0)
        tab.penup()
        tab.goto(point_tab[0])
        tab.pendown()
        for i in point_tab:
            tab.goto(i)

        mur = turtle.Turtle()
        mur.speed(0)
        mur.hideturtle()
        fen.addshape('murV', ((-45, 5), (45, 5), (45, -5), (-45, -5)))
        mur.shape('murV')
        mur.penup()
        for i in self.liste_murs['verticaux']:
            mur.goto(-200+50*(i[0]-1), -200+50*i[1])
            mur.stamp()

        fen.addshape('murH', ((5, -45), (5, 45), (-5, 45), (-5, -45)))
        mur.shape('murH')
        for i in self.liste_murs['horizontaux']:
            mur.goto(-200+50*i[0], -200+50*(i[1]-1))
            mur.stamp()

        self.turtle_j1.hideturtle()
        self.turtle_j1.clearstamps()
        self.turtle_j1.speed(0)
        self.turtle_j1.penup()
        self.turtle_j1.shape('circle')
        self.turtle_j1.goto(
            (-175+50*(self.liste_joueurs[0]['pos'][0]-1),
             -175+50*(self.liste_joueurs[0]['pos'][1]-1)))
        self.turtle_j1.stamp()

        self.turtle_j2.hideturtle()
        self.turtle_j2.clearstamps()
        self.turtle_j2.color('red')
        self.turtle_j2.speed(0)
        self.turtle_j2.penup()
        self.turtle_j2.shape('circle')
        self.turtle_j2.goto(
            (-175+50*(self.liste_joueurs[1]['pos'][0]-1),
             -175+50*(self.liste_joueurs[1]['pos'][1]-1)))
        self.turtle_j2.stamp()
