from direct.showbase.ShowBase import ShowBase
from panda3d.physics import ForceNode, LinearVectorForce

from balle import Balle
from gestionnaire_collision import GestionnaireCollision
from panier import Panier
from terrain import Terrain


class App(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.FPS = 60

        # Activation du moteur physique
        self.enableParticles()

        # Creation du gestionnaire de collision
        self.gestionnaire_collision = GestionnaireCollision(self)
        self.gestionnaire_collision.e = 0.78  # coefficient de restitution d'une balle de basket

        # Chargement du panier de basket
        panier = Panier(self)

        # Modification de la position du panier de basket
        panier.set_position(-3.35, 10, 2)

        # Chargement de la balle
        self.balle = Balle(self)

        # Modification de la position de la balle
        self.balle.set_position(1, 10, 2)

        # ajout de la balle dans le gestionnaire de collision
        self.gestionnaire_collision.ajout_element(self.balle)

        # Chargement du terrain
        Terrain(self)

        # Creation d'un noeud pour la gravite lier au rendu
        gravity_fn = ForceNode('force-gravite')
        # Ajout de la force de gravite au rendu
        self.render.attachNewNode(gravity_fn)
        # Creation de force de gravite
        gravity_force = LinearVectorForce(0, 0, -9.81)
        # Ajout de la force de gravite au noeud
        gravity_fn.addForce(gravity_force)
        # Acceleration uniforme
        gravity_force.setMassDependent(False)
        # Ajout de la gravite au moteur physique
        self.physicsMgr.addLinearForce(gravity_force)
