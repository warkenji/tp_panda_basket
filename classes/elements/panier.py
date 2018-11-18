from classes.elements.base.element_modele import ElementModele


class Panier(ElementModele):
    def __init__(self, app):
        ElementModele.__init__(self, app, "panier", "modeles/basketball_hoop/basketball_hoop.obj", "modeles/basketball_hoop/basketball_hoop_diffuse_noAO.jpg")

        # Modification de la rotation du panier de basket
        self.set_rotation(90, 90, 0)

        taille_panier = self.get_taille()
        # Modification de la taille du panier de bakset
        self.set_taille(1.8, 1.8 * taille_panier.z / taille_panier.x, 2.9 + 1.05)
