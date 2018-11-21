from direct.showbase.ShowBase import ShowBase
from numpy import mean
from panda3d.core import LVector3f

from classes.elements.balle import Balle
from classes.elements.panier import Panier
from classes.elements.terrain import Terrain
from classes.monde.base.monde import Monde


class App(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        self.FPS = 60

        self.monde = Monde(self)

        self.configuration_camera()
        self.configuration_monde()
        self.configuration_elements()

        self.monde.lancer()

    def configuration_camera(self):
        self.disableMouse()
        self.camera.setPos(0, -10, 2)

    def configuration_monde(self):
        # Creation de la gravite
        self.monde.setGravity(0, 0, -9.81)

        # Activation de la table de collision
        self.monde.initSurfaceTable(1)

        # Creation d'une nouvelle surface de collision base sur la balle
        coeff_restitution = mean([0.76, 0.80])
        velocite_rebond_min = 10 ** -3
        self.monde.setSurfaceEntry(0, 0, 150, coeff_restitution, velocite_rebond_min, 0.9, 0.00001, 0.0, 0.002)

    def configuration_elements(self):
        # Chargement du panier de basket
        panier = Panier(self)

        # Modification de la position du panier de basket
        panier.set_position(-3.35, 10, 2.06)

        # Chargement du terrain
        terrain = Terrain(self)

        # Modification de la position du terrain
        terrain.set_position(10, 17.5, 0)

        # Chargement de la balle
        balle = Balle(self)

        balle.set_tir(LVector3f(-2.5, 0, 0), LVector3f(1.1, 10, 2))
