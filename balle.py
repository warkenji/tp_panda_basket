from numpy import mean
from panda3d.core import CollisionSphere

from element_modele import ElementModele


class Balle(ElementModele):
    def __init__(self, app):
        ElementModele.__init__(self, app, "balle", "models/ball/NBA BASKETBALL.obj", "models/ball/NBA BASKETBALL DIFFUSE.jpg")

        # Attache de l'acteur au moteur physique
        self.app.physicsMgr.attachPhysicalNode(self.acteur)

        taille_balle = self.get_taille()

        # Modification de la taille de la balle
        taille = 0.243

        self.set_taille(taille, taille, taille)


        # Attribution d'une masse d'un ballon de basket
        self.acteur.getPhysicsObject().setMass(0.624)

        # Creation d'un solide spherique
        solide = CollisionSphere(0, 0, 0, mean([taille_balle.x, taille_balle.y, taille_balle.z]) * 0.5)

        # Ajouter le solide comme une nouvelle collision au ballon
        self.collision.addSolid(solide)

        # Affichage de la colision
        self.obj_collision.show()

        # Ajout d'une tache recurrente pour faire tourner la balle
        self.app.taskMgr.add(self.simulation_task, "rotation-balle")

    def simulation_task(self, task):
        euler_angle = self.acteur.getPhysicsObject().getRotation().getHpr()
        self.modele.setHpr(self.modele.getHpr() + euler_angle)
        return task.cont
