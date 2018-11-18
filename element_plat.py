from panda3d.core import CardMaker, NodePath

from element import Element


class ElementPlat(Element):

    def __init__(self, app, nom, texture_chemin=None):
        Element.__init__(self, app, nom,  NodePath(CardMaker(nom).generate()), texture_chemin)

