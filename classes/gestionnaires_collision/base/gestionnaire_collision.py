from direct.showbase.DirectObject import DirectObject
from panda3d.core import CollisionTraverser, LMatrix4f, LQuaternionf, CollisionHandlerPusher
from panda3d.physics import PhysicsCollisionHandler


class GestionnaireCollision(DirectObject):
    def __init__(self, app):
        DirectObject.__init__(self)

        self.app = app

        # coefficient de restitution
        self.e = 0.5

        # Creation de la detection de collision
        self.app.cTrav = CollisionTraverser()
        # Permet de verifier si un element n'a pas toucher un element avant de le traverser
        self.app.cTrav.setRespectPrevTransform(True)

        # Creation du gestionnaire de collision de pousser
        # (pousse nativement les objets entre eux pour eviter qu'ils s'enfoncent)
        self.app.pusher = CollisionHandlerPusher()

        # Ajout d'un pattern permettant de prendre en compte n'importe quel element toucher depuis un objet specifique
        self.app.pusher.addInPattern('%fn-in-collision')
        self.app.pusher.addAgainPattern('%fn-again-collision')
        self.app.pusher.addOutPattern('%fn-out-collision')

        # Recuperation du gestionnaire de collision physique par defaut
        self.physicsPusher = PhysicsCollisionHandler()

    def ajout_element(self, element):
        # Ajout de la collision lie a l'acteur dans le gestionnaire de collision natif
        self.app.pusher.addCollider(element.obj_collision, element.obj)
        # Ajout de la collision lie au gestionnaire de collision natif dans le detecteur
        self.app.cTrav.addCollider(element.obj_collision, self.app.pusher)

        # Accepte les response a la collision provoquer par l'element
        self.accept(element.obj_collision.getName() + '-in-collision', self.reponse_collision)

    def reponse_collision(self, entry):
        # https://en.wikipedia.org/wiki/Collision_response

        node_path_a = entry.getFromNodePath()
        node_path_b = entry.getIntoNodePath()

        num_nodes = node_path_a.getNumNodes()
        physics_object_a = node_path_a.getAncestor(num_nodes - 2).node().getPhysicsObject()

        num_nodes = node_path_b.getNumNodes()
        physics_object_b = node_path_b.getAncestor(num_nodes - 2).node().getPhysicsObject()

        ma = physics_object_a.getMass()
        mb = physics_object_b.getMass()

        ia = physics_object_a.getInertialTensor()
        ib = physics_object_a.getInertialTensor()

        vai = physics_object_a.getVelocity()
        vbi = physics_object_b.getVelocity()

        ra = entry.getSurfacePoint(node_path_a)
        rb = entry.getSurfacePoint(node_path_b)

        normal = entry.getSurfaceNormal(self.app.render)
        normal.normalize()

        ia_inverse = LMatrix4f()
        ia_inverse.invertFrom(ia)

        ib_inverse = LMatrix4f()
        ib_inverse.invertFrom(ib)

        angular_vel_change_a = ra.cross(normal)
        angular_vel_change_a = ia_inverse.xformPoint(angular_vel_change_a)
        va_lin_due_to_r = angular_vel_change_a.cross(ra)

        angular_vel_change_b = rb.cross(normal)
        angular_vel_change_b = ib_inverse.xformPoint(angular_vel_change_b)
        vb_lin_due_to_r = angular_vel_change_b.cross(rb)

        scalar_1 = -(1 + self.e) * (vbi - vai).dot(normal)
        scalar_2 = (ma ** -1) + (mb ** -1) + (va_lin_due_to_r + vb_lin_due_to_r).dot(normal)

        j_mod = scalar_1 / scalar_2
        j = normal * j_mod

        qa = LQuaternionf()
        qa.setHpr(- ia_inverse.xformPoint(ra.cross(normal)) * j_mod)

        physics_object_a.addImpulse(- j / ma)
        physics_object_a.addLocalTorque(qa)
