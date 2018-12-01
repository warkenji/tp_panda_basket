from panda3d.core import BitMask32, Vec4
from panda3d.ode import OdePlaneGeom

from classes.elements.base.element_plat import ElementPlat


class Terrain(ElementPlat):
    def __init__(self, app):
        ElementPlat.__init__(self, app, "terrain", "modeles/floor/floor.png")

        # Modification de la rotation du terrain
        self.set_rotation(180, 270, 0)

        # Modification de la taille du terrain
        self.set_taille(28 / 2.0, 14.5, 15)

        # Creation d'un element geometrique plat
        self.geom = OdePlaneGeom(self.app.monde.espace, Vec4(0, 0, 1, 0))

        # Defini les parametres de collision
        self.geom.setCollideBits(BitMask32(0x00000001))
        self.geom.setCategoryBits(BitMask32(0x00000002))

