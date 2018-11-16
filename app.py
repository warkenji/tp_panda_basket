from direct.showbase.ShowBase import ShowBase


class App(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        # Chargement du panier de basket
        panier_basket = self.chargement_panier_basket()

        # Modification de la rotation du panier de basket
        panier_basket.setHpr(90, 90, 0)

        # Modification de la taille du panier de bakset
        taille = 0.001
        panier_basket.setScale(taille, taille, taille)

        # Modification de la position du panier de basket
        panier_basket.setPos(-20, 75, 0)

        # ShowBase.oobe(self)

    def chargement_panier_basket(self):
        # Chargement du panier de basket
        obj = self.loader.loadModel("models/basketball_hoop/basketball_hoop.obj")

        # Chargement de la texture
        tex = self.loader.loadTexture("models/basketball_hoop/basketball_hoop_diffuse_noAO.jpg")

        # Association de la texture au panier de basket
        obj.setTexture(tex)

        # Ajout du panier de basket a la scene
        obj.reparentTo(self.render)

        return obj
