from threading import Lock

from panda3d.ode import OdeWorld, OdeJointGroup, OdeSimpleSpace


class Monde(OdeWorld):
    def __init__(self, app):
        OdeWorld.__init__(self)

        self.app = app

        self.lock = Lock()

        # Creation d'un espace
        self.espace = OdeSimpleSpace()
        # Activation de la collision automatique
        self.espace.setAutoCollideWorld(self)
        # Creation d'une jointure entre les collisions
        self.contactgroup = OdeJointGroup()
        self.espace.setAutoCollideJointGroup(self.contactgroup)

        # Creation d'une liste rassemblant les elements dynamique
        self.elements = []

    def ajouter_element(self, element):
        self.lock.acquire()
        # Ajout d'un element
        if element not in self.elements:
            self.elements.append(element)
        self.lock.release()

    def retirer_element(self, element):
        self.lock.acquire()
        # Suppression d'un element
        if element in self.elements:
            self.elements.remove(element)
        self.lock.release()

    def lancer(self):
        self.app.taskMgr.doMethodLater(1.0 / self.app.FPS, self.simulation, "SimulationPhysique")

    def arreter(self):
        self.app.taskMgr.remove("SimulationPhysique")

    def simulation(self, task):
        self.espace.autoCollide()  # Setup the contact joints
        # Step the simulation and set the new positions
        self.quickStep(globalClock.getDt())

        self.lock.acquire()

        # Met a jour chaque element dynamique lier a la physique du jeu
        for element in self.elements:
            element.maj_physique()

        self.lock.release()

        self.contactgroup.empty()  # Clear the contact joints
        return task.cont