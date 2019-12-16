'''Module api'''
import requests

URL_BASE = 'https://python.gel.ulaval.ca/quoridor/api/'


def lister_parties(idul):
    '''Liste les parties du joueur'''
    rep = requests.get(URL_BASE+'lister/', params={'idul': idul})
    code = rep.status_code
    if code == 200:
        dic = rep.json()
        if dic.get('message', 0) != 0:
            raise RuntimeError(dic['message'])
    else:
        raise RuntimeError(
            f"Le GET sur {URL_BASE+'lister'} a produit le code d'erreur {code}.")
    return dic['parties']


def débuter_partie(idul):
    '''Permet de débuter une nouvelle partie'''
    rep = requests.post(URL_BASE+'débuter/', data={'idul': idul})
    code = rep.status_code
    if code == 200:
        dic = rep.json()
        if dic.get('message', 0) != 0:
            raise RuntimeError(dic['message'])
    else:
        raise RuntimeError(
            f"Le GET sur {URL_BASE+'débuter'} a produit le code d'erreur {code}.")
    return (dic['id'], dic['état'])


def jouer_coup(id_partie, type_coup, position):
    '''Envoie le coup joué au serveur'''
    rep = requests.post(
        URL_BASE+'jouer/', data={'id': id_partie, 'type': type_coup, 'pos': position})
    code = rep.status_code
    if code == 200:
        dic = rep.json()
        if dic.get('message', 0) != 0:
            raise RuntimeError(dic['message'])
        if dic.get('gagnant', 0) != 0:
            raise StopIteration(dic['gagnant'])
        else:
            return dic['état']
    else:
        raise RuntimeError(
            f"Le GET sur {URL_BASE+'jouer'} a produit le code d'erreur {code}.")
