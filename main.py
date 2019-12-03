'''Module main'''
import argparse
import api


def analyser_commande():
    '''Analyseur de ligne de commande.'''
    parser = argparse.ArgumentParser(description='Jeu Quoridor - phase 1')

    # insérer ici avec les bons appels à la méthode add_argument
    parser.add_argument("idul", help="IDUL du joueur.")
    parser.add_argument("-l", '--lister', action='store_true',
                        help="Lister les identifiants de vos 20 dernières parties.")
    return parser.parse_args()


# Ajouter des conditions par rapport aux commandes reçues...(jeu automatique etc.)
if __name__ == "__main__":
    COMMANDE = analyser_commande()
    if COMMANDE.lister:
        print(api.lister_parties(COMMANDE.idul))
    else:
        DEBUTER = api.débuter_partie(COMMANDE.idul)

        ID_PARTIE = DEBUTER[0]

        # afficher_damier_ascii(DEBUTER[1])

        GAGNANT = True
        while GAGNANT:
            OK_CHOIX = True
            while OK_CHOIX:
                CHOIX_COUP = input('Choisir votre coup("D","MH", "MV"): ')
                POS_CHOISIE = input('Entrer les coordonnées (x,y): ')

                try:
                    JOUER = api.jouer_coup(ID_PARTIE, CHOIX_COUP, POS_CHOISIE)
                    OK_CHOIX = False
                   # afficher_damier_ascii(JOUER)
                except StopIteration as err:
                    OK_CHOIX = False
                    GAGNANT = False
                    print(f'Le gagnant est: {err}')
                except RuntimeError as err:
                    print(err)
