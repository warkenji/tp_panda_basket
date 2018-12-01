from math import hypot
from random import randint, random

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

        self.balles = {}

        self.FPS = 60
        self.pos_balle = LVector3f()

        self.monde = Monde(self)
        self.impulsion = 0
        self.impulsion_relative = 0

        self.configuration_camera()
        self.configuration_monde()
        self.configuration_elements()

        self.monde.lancer()

        self.taskMgr.doMethodLater(0.25, self.balleAleatoire, "LancementBalle")


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
        self.accept("ode-collision", self.onCollision)

    def balleAleatoire(self, task):
        # Chargement de la balle
        balle = Balle(self)
        self.balles[str(balle.corps)] = balle
        position_panier = self.panier.geom_cylinder.getPosition()
        position = position_panier - self.pos_balle
        distance_horizontal = hypot(position.x, position.y)
        distance_vertical = hypot(0, position.z)

        pos_z = hypot(distance_horizontal, distance_vertical) * 2

        force = LVector3f(position.x, position.y, pos_z)
        force.normalize()
        self.impulsion += 5

        balle.set_tir(force * self.impulsion, self.pos_balle)

        return task.again

    def onCollision(self, entry):
        geom1 = entry.getGeom1()
        geom2 = entry.getGeom2()

        if self.terrain.geom.compareTo(geom1) == 0 or self.terrain.geom.compareTo(geom2) == 0:

            if self.terrain.geom.compareTo(geom1) != 0:
                cle = str(geom1.getBody())
                balle = self.balles[cle]
                del(self.balles[cle])

                self.monde.retirer_element(balle)
                balle.modele.removeNode()
                balle.geom.destroy()
                balle.corps.destroy()

            elif self.terrain.geom.compareTo(geom2) != 0:
                cle = str(geom2.getBody())
                balle = self.balles[cle]
                del(self.balles[cle])

                self.monde.retirer_element(balle)
                balle.modele.removeNode()
                balle.geom.destroy()
                balle.corps.destroy()

        elif self.panier.geom_cylinder.compareTo(geom1) == 0 or self.panier.geom_cylinder.compareTo(geom2) == 0:
            x = randint(-2, 9)
            y = randint(3, 17)
            # y = 10
            z = random() / 2 + 2

            if self.panier.geom_cylinder.compareTo(geom1) != 0:
                cle = str(geom1.getBody())
                balle = self.balles[cle]
                del(self.balles[cle])

                if balle.session_courante == Balle.session:
                    self.pos_balle = LVector3f(x, y, z)
                    self.impulsion = 0
                    Balle.session = random()

                self.monde.retirer_element(balle)
                balle.modele.removeNode()
                balle.geom.destroy()
                balle.corps.destroy()

            elif self.panier.geom_cylinder.compareTo(geom2) != 0:
                cle = str(geom2.getBody())
                balle = self.balles[cle]
                del(self.balles[cle])

                if balle.session_courante == Balle.session:
                    self.pos_balle = LVector3f(x, y, z)
                    self.impulsion = 0
                    Balle.session = random()

                self.monde.retirer_element(balle)
                balle.modele.removeNode()
                balle.geom.destroy()
                balle.corps.destroy()

