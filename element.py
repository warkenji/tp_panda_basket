from panda3d.core import LPoint3f, CollisionNode
from panda3d.physics import ActorNode


class Element:

    def __init__(self, app, nom, modele, texture_chemin=None):
        self.app = app

        # Chargement du modele
        self.modele = modele

        # Creation d'un acteur
        self.acteur = ActorNode('acteur-' + nom)

        # Creation d'un parent a partir de Acteur
        self.obj = self.app.render.attachNewNode(self.acteur)

        self.collision = CollisionNode('collider-' + nom)
        self.obj_collision = self.obj.attachNewNode(self.collision)

        # Chargement de la texture si elle existe
        if texture_chemin is not None:
            tex = app.loader.loadTexture(texture_chemin)

            # Association de la texture a la balle
            self.modele.setTexture(tex)

        # Ajout de l'objet a la scene
        self.modele.reparentTo(self.obj)

    def set_position(self, x, y, z):
        if self.obj is not None:
            self.obj.setPos(x, y, z)

    def set_rotation(self, x, y, z):
        if self.obj is not None:
            self.obj.setHpr(x, y, z)

    def set_taille(self, x, y, z):
        taille = self.get_taille()
        echelle_modele = self.obj.getScale()
        echelle_collision = self.obj_collision.getScale()

        if taille is not None:
            if echelle_modele is not None:
                self.modele.setScale(x * echelle_modele.x / (taille.x if taille.x > 0 else 1),
                                     y * echelle_modele.y / (taille.z if taille.z > 0 else 1),
                                     z * echelle_modele.z / (taille.y if taille.y > 0 else 1))

            if echelle_collision is not None:
                self.obj_collision.setScale(x * echelle_collision.x / (taille.x if taille.x > 0 else 1),
                                            y * echelle_collision.y / (taille.z if taille.z > 0 else 1),
                                            z * echelle_collision.z / (taille.y if taille.y > 0 else 1))

    def get_taille(self):
        bounds = self.modele.getTightBounds()

        if bounds is not None:
            bound_min, bound_max = bounds
            return LPoint3f(abs(bound_max.x - bound_min.x),
                            abs(bound_max.y - bound_min.y), abs(bound_max.z - bound_min.z))

        return bounds
