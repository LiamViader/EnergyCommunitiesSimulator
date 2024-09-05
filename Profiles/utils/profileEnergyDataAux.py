class ProfileEnergyDataAux:
    def __init__(self, id: int, name:str, production: float, load: float, share: float) -> None:
        self.id=id
        self.name=name
        self.production=production
        self.load=load
        self.share=share
        self.personalPvExcedent=0