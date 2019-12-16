'''Module main'''
import argparse
import api
import quoridor
import quoridorx


def analyser_commande():
    '''Analyseur de ligne de commande.'''
    parser = argparse.ArgumentParser(description='Jeu Quoridor - phase 3')

    parser.add_argument("idul", help="IDUL du joueur.")

    parser.add_argument("-l", '--lister', action='store_true',
                        help="Lister les identifiants de vos 20 dernières parties.")
    # -a
    parser.add_argument("-a", '--automatique', action='store_true',
                        help="Activer le mode automatique.")
    # -x
    parser.add_argument("-x", '--graphique', action='store_true',
                        help="Activer le mode graphique.")

    return parser.parse_args()


if __name__ == "__main__":
    COMMANDE = analyser_commande()

    if COMMANDE.lister:
        print(api.lister_parties(COMMANDE.idul))

    # Mode automatique avec graphique (commande : python main.py -ax idul)
    elif COMMANDE.automatique and COMMANDE.graphique:
        DEBUTER = api.débuter_partie(COMMANDE.idul)
        JEU = quoridorx.QuoridorX(DEBUTER[1]['joueurs'], DEBUTER[1]['murs'])
        ID_PARTIE = DEBUTER[0]

        JEU.afficher()

        GAGNANT = True
        while GAGNANT:
            try:
                COUP = JEU.jouer_coup(1)

                JOUER = api.jouer_coup(ID_PARTIE, COUP[0], COUP[1])
                JEU.liste_joueurs = JOUER['joueurs']
                JEU.liste_murs = JOUER['murs']

                JEU.afficher()
            except StopIteration as err:
                GAGNANT = False
                print(f'Le gagnant est: {err}')
            except RuntimeError as err:
                print(err)

    # Mode automatique (commande : python main.py -a idul)
    elif COMMANDE.automatique:
        DEBUTER = api.débuter_partie(COMMANDE.idul)
        JEU = quoridor.Quoridor(DEBUTER[1]['joueurs'], DEBUTER[1]['murs'])
        ID_PARTIE = DEBUTER[0]

        print(JEU)

        GAGNANT = True
        while GAGNANT:
            try:
                COUP = JEU.jouer_coup(1)

                JOUER = api.jouer_coup(ID_PARTIE, COUP[0], COUP[1])

                JEU.liste_joueurs = JOUER['joueurs']
                JEU.liste_murs = JOUER['murs']

                print(JEU)
            except StopIteration as err:
                GAGNANT = False
                print(f'Le gagnant est: {err}')
            except RuntimeError as err:
                print(err)
    # Mode manuel avec graphique (commande : python main.py -x idul)
    elif COMMANDE.graphique:
        DEBUTER = api.débuter_partie(COMMANDE.idul)
        JEU = quoridorx.QuoridorX(DEBUTER[1]['joueurs'], DEBUTER[1]['murs'])
        ID_PARTIE = DEBUTER[0]

        JEU.afficher()

        GAGNANT = True
        while GAGNANT:
            OK_CHOIX = True
            while OK_CHOIX:
                CHOIX_COUP = input('Choisir votre coup("D","MH", "MV"): ')
                POS = input('Entrer les coordonnées (x,y): ')

                try:
                    JOUER = api.jouer_coup(ID_PARTIE, CHOIX_COUP, POS)

                    OK_CHOIX = False

                    JEU.liste_joueurs = JOUER['joueurs']
                    JEU.liste_murs = JOUER['murs']
                    JEU.afficher()
                except StopIteration as err:
                    OK_CHOIX = False
                    GAGNANT = False
                    print(f'Le gagnant est: {err}')
                except RuntimeError as err:
                    print(err)

    # Mode manuel contre le serveur (commande : python main.py idul)
    else:
        DEBUTER = api.débuter_partie(COMMANDE.idul)
        JEU = quoridor.Quoridor(DEBUTER[1]['joueurs'], DEBUTER[1]['murs'])
        ID_PARTIE = DEBUTER[0]

        print(JEU)

        GAGNANT = True
        while GAGNANT:
            OK_CHOIX = True
            while OK_CHOIX:
                CHOIX_COUP = input('Choisir votre coup("D","MH", "MV"): ')
                POS = input('Entrer les coordonnées (x,y): ')

                try:
                    JOUER = api.jouer_coup(ID_PARTIE, CHOIX_COUP, POS)

                    OK_CHOIX = False
                    JEU.liste_joueurs = JOUER['joueurs']
                    JEU.liste_murs = JOUER['murs']

                    print(JEU)
                except StopIteration as err:
                    OK_CHOIX = False
                    GAGNANT = False
                    print(f'Le gagnant est: {err}')
                except RuntimeError as err:
                    print(err)
