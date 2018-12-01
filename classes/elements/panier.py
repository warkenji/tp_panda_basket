from panda3d.core import BitMask32, LVector3f
from panda3d.ode import OdeTriMeshData, OdeTriMeshGeom, OdeCylinderGeom

from classes.elements.base.element_modele import ElementModele


class Panier(ElementModele):
    def __init__(self, app):
        ElementModele.__init__(self, app, "panier", "modeles/basketball_hoop/basketball_hoop.obj",
                               "modeles/basketball_hoop/basketball_hoop_diffuse_noAO.jpg")

        taille_panier = self.get_taille()

        # Modification de la taille du panier de bakset
        self.set_taille(1.8, 1.8 * taille_panier.z / taille_panier.x, 2.9 + 1.05)

        # Application des modification au modele
        self.modele.flattenLight()

        # Recuparation des donnees du modele
        mesh = OdeTriMeshData(self.modele)

        # Creation d'un element geometrique baser sur les donnees du modele
        self.geom = OdeTriMeshGeom(self.app.monde.espace, mesh)

        # Defini les parametres de collision
        self.geom.setCollideBits(BitMask32(0x00000001))
        self.geom.setCategoryBits(BitMask32(0x00000002))

        self.geom_cylinder = OdeCylinderGeom(self.app.monde.espace, 0.15, 0.01)
        self.geom_cylinder.setCollideBits(BitMask32(0x00000001))
        self.geom_cylinder.setCategoryBits(BitMask32(0x00000002))

        # sphere = CollisionSphere(0, 0, 0, 0.2)
        # self.sphere_path = self.app.render.attachNewNode(CollisionNode('cnode'))
        # self.sphere_path.node().addSolid(sphere)
        # self.sphere_path.show()

        # Modification de la rotation du panier de basket
        self.set_rotation(90, 90, 0)

    def set_position(self, x, y, z):
        ElementModele.set_position(self, x, y, z)

        self.geom.setPosition(self.modele.getPos(self.app.render))
        self.geom_cylinder.setPosition(self.modele.getPos(self.app.render) + LVector3f(0.4, 0, 1.25))

        # self.sphere_path.setPos(self.modele.getPos(self.app.render) + LVector3f(0.4, 0, 1.3))

    def set_rotation(self, x, y, z):
        ElementModele.set_rotation(self, x, y, z)

        self.geom.setQuaternion(self.modele.getQuat(self.app.render))
