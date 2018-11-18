from panda3d.core import CollisionPlane, Plane, Vec3, Point3

from classes.elements.base.element_plat import ElementPlat


class Terrain(ElementPlat):
    def __init__(self, app):
        ElementPlat.__init__(self, app, "terrain", "modeles/floor/floor.png")

        # Modification de la rotation du terrain
        self.set_rotation(180, 270, 0)

        # Modification de la taille du terrain
        self.set_taille(28 / 2.0, 14.5, 15)

        # Modification de la position du terrain
        self.set_position(10, 17.5, 0)

        self.acteur.getPhysicsObject().setMass(5.972 * 10 ** 24)

        solide = CollisionPlane(Plane(Vec3(0, -1, 0), Point3(0, 0, 0)))

        self.collision.addSolid(solide)

        # Affichage de la colision
        self.obj_collision.show()
