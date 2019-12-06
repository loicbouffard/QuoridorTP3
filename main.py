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
    parser.add_argument("-a", action='store_true',
                        help="Jouer en mode automatique contre le serveur.")
    # -x
    parser.add_argument("-x", action='store_true',
                        help="Jouer en mode manuel contre le serveur avec affichage graphique.")
    # -ax
    parser.add_argument("-ax", action='store_true',
                        help="Jouer en mode automatique contre le serveur avec un affichage graphique.")
    return parser.parse_args()


if __name__ == "__main__":
    COMMANDE = analyser_commande()

    if COMMANDE.lister:
        print(api.lister_parties(COMMANDE.idul))
    # Mode automatique (commande : python main.py -a idul)
    elif COMMANDE.a:
        DEBUTER = api.débuter_partie(COMMANDE.idul)
        JEU = quoridor.Quoridor(DEBUTER[1]['joueurs'], DEBUTER[1]['murs'])
        ID_PARTIE = DEBUTER[0]

        print(JEU)
        CHOIX_COUP = ''
        POS = ''
        GAGNANT = True
        while GAGNANT:
            POS_PRECEDENTE = JEU.état_partie()['joueurs'][0]['pos']
            NBR_MURSH = len(JEU.état_partie()['murs']['horizontaux'])
            NBR_MURSV = len(JEU.état_partie()['murs']['verticaux'])

            try:
                JEU.jouer_coup(1)
                # Détection du coup joué automatique et de la position
                if POS_PRECEDENTE != JEU.état_partie()['joueurs'][0]['pos']:
                    CHOIX_COUP = 'D'
                    POS = str(JEU.état_partie()['joueurs'][0]['pos'])
                elif NBR_MURSH != len(JEU.état_partie()['murs']['horizontaux']):
                    CHOIX_COUP = 'MH'
                    POS = str(JEU.état_partie()['murs']['horizontaux'][-1])
                elif NBR_MURSV != len(JEU.état_partie()['murs']['verticaux']):
                    CHOIX_COUP = 'MV'
                    POS = str(JEU.état_partie()['murs']['verticaux'][-1])

                JOUER = api.jouer_coup(ID_PARTIE, CHOIX_COUP, POS)

                OK_CHOIX = False
                JEU = quoridor.Quoridor(JOUER['joueurs'], JOUER['murs'])
                print(JEU)
            except StopIteration as err:
                OK_CHOIX = False
                GAGNANT = False
                print(f'Le gagnant est: {err}')
            except RuntimeError as err:
                print(err)
    # Mode manuel avec graphique (commande : python main.py -x idul)
    elif COMMANDE.x:
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
                    JEU = quoridorx.QuoridorX(JOUER['joueurs'], JOUER['murs'])
                    JEU.afficher()
                except StopIteration as err:
                    OK_CHOIX = False
                    GAGNANT = False
                    print(f'Le gagnant est: {err}')
                except RuntimeError as err:
                    print(err)
    # Mode automatique avec graphqiue (commande : python main.py -ax idul)
    elif COMMANDE.ax:
        DEBUTER = api.débuter_partie(COMMANDE.idul)
        JEU = quoridorx.QuoridorX(DEBUTER[1]['joueurs'], DEBUTER[1]['murs'])
        ID_PARTIE = DEBUTER[0]

        JEU.afficher()

        print('À implenter')
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
                    JEU = quoridor.Quoridor(JOUER['joueurs'], JOUER['murs'])
                    print(JEU)
                except StopIteration as err:
                    OK_CHOIX = False
                    GAGNANT = False
                    print(f'Le gagnant est: {err}')
                except RuntimeError as err:
                    print(err)
