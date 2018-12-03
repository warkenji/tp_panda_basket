from random import random

from numpy import pi, mean
from panda3d.core import BitMask32, LVector3f
from panda3d.ode import OdeSphereGeom, OdeMass

from classes.elements.base.element_modele import ElementModele


class Balle(ElementModele):
    session = random()

    def __init__(self, app, distance=0, force=0):
        ElementModele.__init__(self, app, "balle", "modeles/ball/NBA BASKETBALL.obj", "modeles/ball/NBA BASKETBALL DIFFUSE.jpg")

        # Taille moyenne d'une balle
        taille = mean([23.8, 24.8]) * 10 ** -2
        self.session_courante = Balle.session

        self.distance = distance
        self.force = force

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
        self.geom = OdeSphereGeom(self.app.monde.espace, taille / 2.0)

        # Defini les parametres de collision
        self.geom.setCollideBits(BitMask32(0x00000002))
        self.geom.setCategoryBits(BitMask32(0x00000001))

        # Attache l'element geometrique a la balle
        self.geom.setBody(self.corps)

        # Ajout de la balle comme element dynamique
        self.app.monde.ajouter_element(self)

    def set_position(self, x, y, z):
        self.corps.setPosition(LVector3f(x, y, z))

    def get_position(self):
        return self.corps.getPosition()

    def set_rotation(self, x, y, z):
        ElementModele.set_rotation(self, x, y, z)

        self.corps.setQuaternion(self.modele.getQuat(self.app.render))

    def set_tir(self, force, position):
        self.corps.setLinearVel(0, 0, 0)
        self.corps.setAngularVel(0, 0, 0)
        self.set_position(position.x, position.y, position.z)
        self.corps.setForce(force)
