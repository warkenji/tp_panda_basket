from numpy import pi, mean
from panda3d.core import BitMask32
from panda3d.ode import OdeSphereGeom, OdeMass

from classes.elements.base.element_modele import ElementModele


class Balle(ElementModele):
    def __init__(self, app):
        ElementModele.__init__(self, app, "balle", "modeles/ball/NBA BASKETBALL.obj", "modeles/ball/NBA BASKETBALL DIFFUSE.jpg")

        # Taille moyenne d'une balle
        taille = mean([23.8, 24.8]) * 10 ** -2

        # Rayon de la balle
        rayon = taille / 2.0

        # Poids moyen d'une balle
        poids = mean([567, 624]) * 10 ** -3

        # Modification de la taille de la balle
        self.set_taille(taille, taille, taille)

        volume = (4.0 * pi / 3.0) * rayon ** 3
        masse = OdeMass()
        masse.setSphere(poids / volume, rayon)
        self.corps.setMass(masse)

        # Creation d'un element geometrique spherique
        geom = OdeSphereGeom(self.app.monde.espace, taille / 2.0)

        # Defini les parametres de collision
        geom.setCollideBits(BitMask32(0x00000002))
        geom.setCategoryBits(BitMask32(0x00000001))

        # Attache l'element geometrique a la balle
        geom.setBody(self.corps)

        # Ajout de la balle comme element dynamique
        self.app.monde.ajouter_element(self)

    def set_position(self, x, y, z):
        ElementModele.set_position(self, x, y, z)

        self.corps.setPosition(self.modele.getPos(self.app.render))

    def set_rotation(self, x, y, z):
        ElementModele.set_rotation(self, x, y, z)

        self.corps.setQuaternion(self.modele.getQuat(self.app.render))
