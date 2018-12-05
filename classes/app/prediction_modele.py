from random import randint, random

import tensorflow as tf
from direct.showbase.ShowBase import ShowBase
from numpy import mean
from panda3d.core import LVector3f

from classes.elements.balle import Balle
from classes.elements.panier import Panier
from classes.elements.terrain import Terrain
from classes.monde.base.monde import Monde


class App(ShowBase):

    def __init__(self, chemin_fichier='tf_model.h5'):
        ShowBase.__init__(self)

        self.balles = {}
        self.chemin_fichier = chemin_fichier

        self.modele = None

        self.FPS = 60
        self.pos_balle = LVector3f()

        self.monde = Monde(self)
        self.force = 0
        self.impulsion_relative = 0

        self.configuration_camera()
        self.configuration_monde()
        self.configuration_elements()

        self.monde.lancer()

        # self.taskMgr.doMethodLater(0.5, self.balleAleatoire, "LancementBalle")
        self.taskMgr.doMethodLater(0.5, self.ballePredit, "LancementBalle")

    def configuration_camera(self):
        #self.disableMouse()
        self.camera.setPos(0, -5, 2)
        #self.camera.setPos(-2.5, 10, 1.25)
        self.oobe()

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
        self.panier = Panier(self)

        # Modification de la position du panier de basket
        self.panier.set_position(-3.35, 10, 2.06)

        # Chargement du terrain
        self.terrain = Terrain(self)

        # Modification de la position du terrain
        self.terrain.set_position(10, 17.5, 0)

        self.pos_balle = LVector3f(3, 10, 2)

        self.monde.espace.setCollisionEvent("ode-collision")
        self.accept("ode-collision", self.on_collision)

    def ballePredit(self, task):
        if self.modele is None:
            self.modele = tf.keras.models.load_model(self.chemin_fichier)

        # Chargement de la balle
        balle = Balle(self)

        x = randint(-2, 9)
        y = randint(3, 17)
        z = random() / 2 + 2

        pos_balle = LVector3f(x, y, z)
        self.balles[str(balle.corps)] = balle
        position_panier = self.panier.geom_cylinder.getPosition()
        position = position_panier - pos_balle
        distance = (position.x ** 2 + position.y ** 2 + position.z ** 2) ** 0.5

        pos_z = distance * 2

        direction = LVector3f(position.x, position.y, pos_z)
        direction.normalize()
        force = self.modele.predict([distance / 15.0]).flatten()[0] * 500

        balle.set_tir(direction * force, pos_balle)

        return task.again

    def on_collision(self, entry):
        geom1 = entry.getGeom1()
        geom2 = entry.getGeom2()
        cle = None
        tir_reussi = False

        if self.terrain.geom.compareTo(geom1) == 0 or self.terrain.geom.compareTo(geom2) == 0:

            if self.terrain.geom.compareTo(geom1) != 0:
                cle = str(geom1.getBody())

            elif self.terrain.geom.compareTo(geom2) != 0:
                cle = str(geom2.getBody())

        elif self.panier.geom_cylinder.compareTo(geom1) == 0 or self.panier.geom_cylinder.compareTo(geom2) == 0:
            tir_reussi = True

            if self.panier.geom_cylinder.compareTo(geom1) != 0:
                cle = str(geom1.getBody())

            elif self.panier.geom_cylinder.compareTo(geom2) != 0:
                cle = str(geom2.getBody())

        if cle is not None:
            balle = self.balles[cle]
            del (self.balles[cle])

            self.monde.retirer_element(balle)
            balle.modele.removeNode()
            balle.geom.destroy()
            balle.corps.destroy()
