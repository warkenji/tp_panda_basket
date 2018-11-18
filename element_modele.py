from element import Element


class ElementModele(Element):

    def __init__(self, app, nom, modele_chemin, texture_chemin=None):
        Element.__init__(self, app, nom, app.loader.loadModel(modele_chemin), texture_chemin)
