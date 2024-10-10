class ProfileSharingsDataAux:
    """
    Class for representing the sharing data associated with an energy profile within a community.

    This class is designed to store various metrics related to energy sharing, including grid imports and exports,
    microgrid interactions, and personal production contributions. It serves as a data structure to facilitate
    the management of energy sharing information for individual profiles in a community setting.

    Attributes:
        id (int): The unique identifier for the energy profile.

        gridExport (float): The amount of energy exported to the external grid (in kWh). It means the energy exported to the energy retailer (Endesa or SomEnergia or whatever)

        gridImport (float): The amount of energy imported from the external grid (in kWh). It means the energy imported from the energy retailer (Endesa or SomEnergia or whatever)

        microgridExport (float): The amount of energy exported to the microgrid (in kWh). It means the energy exported to the community

        microgridImport (float): The amount of energy imported from the microgrid (in kWh). It means the energy imported from the community

        personalPvExcedent (float): The surplus energy generated from personal production systems (in kWh).

        totalPvAbleToShare (float): The total amount of production energy the user had available to share, considering both community
        assets and personal contributions (in kWh). 

        communityShares (float): The percentage of the energy community the user possesses (0-1).
    """
    def __init__(self,profile_id:int) -> None:
        """
        Initializes a ProfileSharingsDataAux instance with a unique profile ID.

        Args:
            profile_id (int): The unique identifier for the energy profile.
        """
        self.id=profile_id
        self.gridExport=0
        self.gridImport=0
        self.microgridExport=0
        self.microgridImport=0
        self.personalPvExcedent=0
        self.totalPvAbleToShare=0 #en cas que nomes es comparteixi assets de la comunitat, això es pv del asset de la comunitat * community shares (el percentatge que té), si tb comparteix els seus assets serà lo anterior + el pv seu
        self.communityShares=0