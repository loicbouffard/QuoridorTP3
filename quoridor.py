'''Module de la classe du jeu Quoridor'''
import copy
import networkx as nx


def construire_graphe(joueurs, murs_horizontaux, murs_verticaux):
    """
    Crée le graphe des déplacements admissibles pour les joueurs.
    :param joueurs: une liste des positions (x,y) des joueurs.
    :param murs_horizontaux: une liste des positions (x,y) des murs horizontaux.
    :param murs_verticaux: une liste des positions (x,y) des murs verticaux.
    :returns: le graphe bidirectionnel (en networkX) des déplacements admissibles.
    """
    graphe = nx.DiGraph()

    # pour chaque colonne du damier
    for x in range(1, 10):
        # pour chaque ligne du damier
        for y in range(1, 10):
            # ajouter les arcs de tous les déplacements possibles pour cette tuile
            if x > 1:
                graphe.add_edge((x, y), (x-1, y))
            if x < 9:
                graphe.add_edge((x, y), (x+1, y))
            if y > 1:
                graphe.add_edge((x, y), (x, y-1))
            if y < 9:
                graphe.add_edge((x, y), (x, y+1))

    # retirer tous les arcs qui croisent les murs horizontaux
    for x, y in murs_horizontaux:
        graphe.remove_edge((x, y-1), (x, y))
        graphe.remove_edge((x, y), (x, y-1))
        graphe.remove_edge((x+1, y-1), (x+1, y))
        graphe.remove_edge((x+1, y), (x+1, y-1))

    # retirer tous les arcs qui croisent les murs verticaux
    for x, y in murs_verticaux:
        graphe.remove_edge((x-1, y), (x, y))
        graphe.remove_edge((x, y), (x-1, y))
        graphe.remove_edge((x-1, y+1), (x, y+1))
        graphe.remove_edge((x, y+1), (x-1, y+1))

    # retirer tous les arcs qui pointent vers les positions des joueurs
    # et ajouter les sauts en ligne droite ou en diagonale, selon le cas
    for joueur in map(tuple, joueurs):

        for prédécesseur in list(graphe.predecessors(joueur)):
            graphe.remove_edge(prédécesseur, joueur)

            # si admissible, ajouter un lien sauteur
            successeur = (2*joueur[0]-prédécesseur[0],
                          2*joueur[1]-prédécesseur[1])

            if successeur in graphe.successors(joueur) and successeur not in joueurs:
                # ajouter un saut en ligne droite
                graphe.add_edge(prédécesseur, successeur)

            else:
                # ajouter les liens en diagonal
                for successeur in list(graphe.successors(joueur)):
                    if prédécesseur != successeur and successeur not in joueurs:
                        graphe.add_edge(prédécesseur, successeur)

    # ajouter les noeuds objectifs des deux joueurs
    for x in range(1, 10):
        graphe.add_edge((x, 9), 'B1')
        graphe.add_edge((x, 1), 'B2')

    return graphe


class Quoridor:
    '''Classe du jeu Quoridor'''

    def __init__(self, joueurs, murs=None):
        if murs is not None and murs is not dict:
            raise QuoridorError(
                "murs n'est pas un dictionnaire lorsque présent.")
        elif murs is not None:
            for i in murs['horizonraux']:
                if i[0] < 1 or i[0] > 9 or i[1] < 1 or i[1] > 9:
                    raise QuoridorError("la position d'un mur est invalide.")
            for i in murs['verticaux']:
                if i[0] < 1 or i[0] > 9 or i[1] < 1 or i[1] > 9:
                    raise QuoridorError("la position d'un mur est invalide.")
            self.liste_murs = copy.deepcopy(murs)
        elif murs is None:
            self.liste_murs = {'horizontaux': [], 'verticaux': []}
        if isiterable(joueurs):
            if len(joueurs) > 2:
                raise QuoridorError(
                    "l'itérable de joueurs en contient plus de deux.")
            if isinstance(joueurs[0], str):
                self.liste_joueurs = [{'nom': joueurs[0], 'murs': 10, 'pos': (
                    5, 1)}, {'nom': joueurs[1], 'murs': 10, 'pos': (5, 9)}]

            elif isinstance(joueurs[0], dict):
                self.liste_joueurs = [copy.deepcopy(
                    joueurs[0]), copy.deepcopy(joueurs[1])]
                # valide position joueur1
                if (joueurs[0]['pos'][0] < 1 or joueurs[0]['pos'][0] > 9 or
                        joueurs[0]['pos'][1] < 1 or joueurs[0]['pos'][1] > 9):
                    raise QuoridorError(
                        "la position d'un joueur est invalide.")
                # valide position joueur2
                if (joueurs[1]['pos'][0] < 1 or joueurs[1]['pos'][0] > 9 or
                        joueurs[1]['pos'][1] < 1 or joueurs[1]['pos'][1] > 9):
                    raise QuoridorError(
                        "la position d'un joueur est invalide.")
                # Valide nombre mur
                if (joueurs[0]['murs'] > 10 or joueurs[0]['murs'] < 0 or
                        joueurs[1]['murs'] > 10 or joueurs[1]['murs'] < 0):
                    raise QuoridorError(
                        "le nombre de murs qu'un joueur peut placer est > 10, ou négatif.")
        else:
            raise QuoridorError("joueurs n'est pas un itérable.")

        if len(self.liste_murs['horizontaux']) + len(self.liste_murs[
                'verticaux']) + self.liste_joueurs[0]['murs'] + self.liste_joueurs[1]['murs'] != 20:
            raise QuoridorError(
                "le total des murs placés et plaçables n'est pas égal à 20.")

    def __str__(self):
        tab = []
        for i in range(9):
            tab += [[' . ', ' '] * 8 + [' . ']]
            if i != 8:
                tab += [['   ', ' '] * 8 + ['   ']]

        # place les joueurs sur le damier
        tab[(9 - self.liste_joueurs[0]["pos"][1]) *
            2][(self.liste_joueurs[0]["pos"][0]-1) * 2] = ' 1 '
        tab[(9-self.liste_joueurs[1]["pos"][1]) *
            2][(self.liste_joueurs[1]["pos"][0]-1) * 2] = ' 2 '

        # place les murs sur le damier
        for i in self.liste_murs["verticaux"]:
            tab[(9 - i[1]) * 2][(i[0] - 1) * 2 - 1] = '|'
            tab[(9 - i[1]) * 2 - 1][(i[0] - 1) * 2 - 1] = '|'
            tab[(9 - i[1] - 1) * 2][(i[0] - 1) * 2 - 1] = '|'

        for i in self.liste_murs["horizontaux"]:
            tab[(9 - i[1]) * 2 + 1][(i[0] - 1) * 2] = '---'
            tab[(9 - i[1]) * 2 + 1][(i[0] - 1) * 2 + 1] = '-'
            tab[(9 - i[1]) * 2 + 1][(i[0]) * 2] = '---'

        # transforme le damier en chaine de caractère
        damier = f'Légende: 1={self.liste_joueurs[0]["nom"]}, 2={self.liste_joueurs[1]["nom"]}\n'
        damier += '   ' + '-' * 35 + '\n'
        debut2 = '  |'
        ligne_f = '--|' + '-' * 35 + '\n  | 1   2   3   4   5   6   7   8   9'

        for i in range(9):
            debut1 = f'{9 - i} |'
            ligne1 = debut1 + ''.join(tab[2 * i]) + '|\n'
            if i != 8:
                ligne2 = debut2 + ''.join(tab[2 * i + 1]) + '|\n'
            else:
                ligne2 = ''
            damier += ligne1 + ligne2

        damier += ligne_f
        return damier

    def déplacer_jeton(self, joueur, position):
        '''Permet de déplacer un jeton'''
        if joueur not in (2, 1):
            raise QuoridorError("le numéro du joueur est autre que 1 ou 2.")

        if position[0] > 9 or position[0] < 1 or position[1] > 9 or position[1] < 1:
            raise QuoridorError(
                "la position est invalide (en dehors du damier).")

        graphe = construire_graphe([joueur['pos'] for joueur in self.liste_joueurs],
                                   self.liste_murs['horizontaux'], self.liste_murs['verticaux'])

        # vérifie position valide
        if position in graphe.successors(self.liste_joueurs[joueur-1]['pos']):
            self.liste_joueurs[joueur-1]['pos'] = position

        else:
            raise QuoridorError(
                "la position est invalide pour l'état actuel du jeu.")

    def jouer_coup(self, joueur):
        '''Permet de jouer un coup automatiquement'''
        if joueur not in (2, 1):
            raise QuoridorError("le numéro du joueur est autre que 1 ou 2.")

        if self.partie_terminée() is not False:
            raise QuoridorError("la partie est déjà terminée.")

        graphe = construire_graphe([joueur['pos'] for joueur in self.liste_joueurs],
                                   self.liste_murs['horizontaux'], self.liste_murs['verticaux'])
        coups = nx.shortest_path(
            graphe, self.liste_joueurs[joueur - 1]['pos'], 'B' + str(joueur))
        coups_adver = nx.shortest_path(
            graphe, self.liste_joueurs[2 - joueur]['pos'], 'B' + str(3 - joueur))

        if len(coups) <= len(coups_adver) or self.liste_joueurs[joueur-1]['murs'] < 1:
            self.déplacer_jeton(joueur, coups[1])

        else:
            # si horizontal
            if coups_adver[0][0]-coups_adver[1][0] == 0:
                for i in graphe.successors(coups_adver[0]):
                    if (i not in self.liste_murs["horizontaux"] and
                            (i[0]-1, i[1]) not in self.liste_murs["horizontaux"] and
                            (i[0] + 1, i[1] - 1) not in self.liste_murs["verticaux"]):
                        self.placer_mur(joueur, tuple(i), 'horizontal')
                        break

            # si vertical ou autre
            else:
                for i in graphe.successors(coups_adver[0]):
                    if (i not in self.liste_murs["verticaux"] and
                            [i[0], i[1]-1] not in self.liste_murs["verticaux"] and
                            (i[0] - 1, i[1] + 1) not in self.liste_murs["horizontaux"]):
                        self.placer_mur(joueur, tuple(i), 'vertical')
                        break

    def état_partie(self):
        """Permet de retourner l'état de la partie sous la forme d'un dictionnaire"""
        # murs a tirer de la methode placer_mur
        état = {'joueurs': [
            {'nom': self.liste_joueurs[0]['nom'], 'murs': self.liste_joueurs[0]['murs'],
             'pos': self.liste_joueurs[0]['pos']},
            {'nom': self.liste_joueurs[1]['nom'], 'murs': self.liste_joueurs[1]['murs'],
             'pos': self.liste_joueurs[1]['pos']}, ], 'murs': {
                 'horizontaux': self.liste_murs['horizontaux'],
                 'verticaux': self.liste_murs['verticaux'], }}
        return état

    def partie_terminée(self):
        """Détermine si la partie est terminée"""
        terminée = False

        if self.état_partie()['joueurs'][0]['pos'][1] == 9:
            terminée = self.état_partie()["joueurs"][0]["nom"]
        elif self.état_partie()['joueurs'][1]['pos'][1] == 1:
            terminée = self.état_partie()["joueurs"][1]["nom"]
        return terminée

    def placer_mur(self, joueur: int, position: tuple, orientation: str):
        """Permet de placer un mur sur le jeu"""
        if joueur not in (2, 1):
            raise QuoridorError('le numéro du joueur est autre que 1 ou 2.')
        if self.liste_joueurs[joueur-1]['murs'] > 0:
            if orientation == 'horizontal':
                if position[0] > 8 or position[0] < 1 or position[1] < 2 or position[1] > 9:
                    raise QuoridorError(
                        'la position est invalide pour cette orientation.')
                for mur in self.liste_murs['horizontaux']:
                    if position == mur or (position[0] == (mur[0]+1) and position[1] == mur[1]):
                        raise QuoridorError(
                            'un mur occupe déjà cette position.')

                # si les deux murs se croisent:
                for mur in self.liste_murs['verticaux']:
                    if position[0] == mur[0]-1 and position[1] == mur[1]+1:
                        raise QuoridorError(
                            'un mur occupe déjà cette position.')
                # on ajoute le tuple position au murs horizontaux
                self.liste_murs['horizontaux'].append(position)
                self.liste_joueurs[joueur-1]['murs'] -= 1
            if orientation == 'vertical':
                if position[0] > 9 or position[0] < 2 or position[1] < 1 or position[1] > 8:
                    raise QuoridorError(
                        'la position est invalide pour cette orientation.')
                for mur in self.liste_murs['verticaux']:
                    if position == mur or (position[1] == (mur[1]+1) and position[0] == mur[0]):
                        raise QuoridorError(
                            'un mur occupe déjà cette position.')

                # si les deux murs se croisent:
                for mur in self.liste_murs['horizontaux']:
                    if position[0] == mur[0]+1 and position[1] == mur[1]-1:
                        raise QuoridorError(
                            'un mur occupe déjà cette position.')
                # on ajoute le tuple position au murs verticaux
                self.liste_murs['verticaux'].append(position)
                self.liste_joueurs[joueur-1]['murs'] -= 1
        else:
            raise QuoridorError('Le joueur a déjà placé tous ses murs.')


class QuoridorError(Exception):
    """Classe pour soulever les erreurs dans le jeu Quoridor"""

    def __init__(self, message):
        super().__init__(message)


def isiterable(p_object):
    '''Permet de vérifier si un objet est itérable'''
    try:
        it = iter(p_object)
        return True
    except TypeError:
        return False
