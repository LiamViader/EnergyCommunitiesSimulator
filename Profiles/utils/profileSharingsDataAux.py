class ProfileSharingsDataAux:
    def __init__(self,profile_id:int) -> None:
        self.id=profile_id
        self.gridExport=0
        self.gridImport=0
        self.microgridExport=0
        self.microgridImport=0
        self.personalPvExcedent=0
        self.totalPvAbleToShare=0 #en cas que nomes es comparteixi assets de la comunitat, això es pv del asset de la comunitat * community shares (el percentatge que té), si tb comparteix els seus assets serà lo anterior + el pv seu
        self.communityShares=0