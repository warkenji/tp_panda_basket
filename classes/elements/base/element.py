from panda3d.core import LPoint3f, Quat
from panda3d.ode import OdeBody


class Element:

    def __init__(self, app, nom, modele, texture_chemin=None):
        self.app = app
        self.nom = nom

        self.corps = OdeBody(self.app.monde)

        # Chargement du modele
        self.modele = modele

        if texture_chemin is not None:
            tex = app.loader.loadTexture(texture_chemin)

            # Association de la texture au modele
            self.modele.setTexture(tex)

        # Ajout de l'objet a la scene
        self.modele.reparentTo(self.app.render)

    def set_position(self, x, y, z):
        if self.modele is not None:
            self.modele.setPos(x, y, z)

    def get_position(self):
        return self.modele.getPos()

    def set_rotation(self, x, y, z):
        if self.modele is not None:
            self.modele.setHpr(x, y, z)

    def set_taille(self, x, y, z):
        taille = self.get_taille()
        echelle_modele = self.modele.getScale()

        if taille is not None and echelle_modele is not None:
            self.modele.setScale(x * echelle_modele.x / (taille.x if taille.x > 0 else 1),
                                 y * echelle_modele.y / (taille.z if taille.z > 0 else 1),
                                 z * echelle_modele.z / (taille.y if taille.y > 0 else 1))

    def get_taille(self):
        bounds = self.modele.getTightBounds()

        if bounds is not None:
            bound_min, bound_max = bounds
            return LPoint3f(abs(bound_max.x - bound_min.x),
                            abs(bound_max.y - bound_min.y), abs(bound_max.z - bound_min.z))

        return bounds

    def maj_physique(self):
        self.modele.setPosQuat(self.app.render, self.corps.getPosition(), Quat(self.corps.getQuaternion()))
