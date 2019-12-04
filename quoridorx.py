import turtle
import quoridor


class QuoridorX(quoridor.Quoridor):

    def __init__(self):
        super().__init__()

    def afficher(self):
        fen = turtle.Screen()
        fen.title("Quoridor")
        fen.setup(width=700, height=600)
        pointTab=((-200, 250),(250, 250), (250, -200), (-200, -200), (-200, 250), (-150,250),(-150,-200),
        (-100,-200),(-100,250),(-50,250),(-50,-200),(0,-200),(0,250),(50,250),(50,-200),(100,-200),
        (100,250),(150,250),(150,-200),(200,-200),(200,250),(250,250),(250,200),(-200,200),(-200,150),
        (250,150),(250,100),(-200,100),(-200,50),(250,50),(250,0),(-200,0),(-200,-50),(250,-50),
        (250,-100),(-200,-100),(-200,-150),(250,-150))

        tab=turtle.Turtle()
        tab.hideturtle()
        tab.speed(0)
        tab.penup()
        tab.goto(pointTab[0])
        tab.pendown()
        for i in pointTab:
            tab.goto(i)


        mur= turtle.Turtle()
        mur.speed(0)
        fen.addshape('murV',((-45,5),(45,5),(45,-5),(-45,-5)))
        murvertical=[[6, 2], [4, 4], [2, 6], [7, 5], [7, 7]]
        mur.shape('murV')
        mur.penup()
        for i in murvertical:
            mur.goto(-200+50*(i[0]-1),-200+50*i[1])
            mur.stamp()

        fen.addshape('murH',((5,-45),(5,45),(-5,45),(-5,-45)))
        murhorizontal=[[4, 4], [2, 6], [3, 8], [5, 8], [7, 8]]
        mur.shape('murH')
        for i in murhorizontal:
            mur.goto(-200+50*i[0],-200+50*(i[1]-1))
            mur.stamp()

        posjoueur1=(5,5)
        posjoueur2=(8,6)
        j=turtle.Turtle()
        j.speed(0)
        j.penup()
        j.shape('circle')
        j.goto((-175+50*(posjoueur1[0]-1),-175+50*(posjoueur1[1]-1)))
        j.stamp()
        j.color('red')
        j.goto((-175+50*(posjoueur2[0]-1),-175+50*(posjoueur2[1]-1)))
        j.stamp()
        fen.exitonclick()