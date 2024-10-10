class ProfileCostDataAux:
    """
    A class to represent the cost and revenue data for a specific profile.

    This class holds information about the costs and revenues associated with 
    energy imports and exports for a profile, including pricing details for grid 
    and microgrid transactions, as well as plans for each of these transactions.

    Attributes:
        id (int): A unique identifier for the profile.

        gridImportPrice (float): The price per kwh for importing energy from the grid.

        gridImportCost (float): The total cost incurred from importing energy from the grid.

        gridExportPrice (float): The price per kwh for exporting energy to the grid.

        gridExportRevenue (float): The total revenue earned from exporting energy to the grid.

        microgridPrice (float): The price per kwh for energy transactions within the microgrid.

        microgridRevenue (float): The total revenue earned from transactions within the microgrid.

        microgridCost (float): The total cost incurred from transactions within the microgrid.

        personalExcedentsPrice (float): The price per kwh for personal energy excess.

        personalExcedentsRevenue (float): The total revenue earned from personal energy excess.

        gridImportPlan (str): The name of the energy plan used to import from the grid.

        gridExportPlan (str): The name of the energy plan used to export to the grid.
        
        personalExcedentsPlan (str): The name of the energy plan used to export personal excedents.
    """
    def __init__(self, id: int) -> None:
        """
        Initializes a ProfileCostDataAux instance with the provided profile ID.

        Args:
            id (int): A unique identifier for the profile.

        All monetary attributes are initialized to zero by default, and all plan name attributes
        are initialized to "Missing".
        """
        self.id=id
        self.gridImportPrice=0
        self.gridImportCost=0
        self.gridExportPrice=0
        self.gridExportRevenue=0
        self.microgridPrice=0
        self.microgridRevenue=0
        self.microgridCost=0
        self.personalExcedentsPrice=0
        self.personalExcedentsRevenue=0
        self.gridImportPlan="Missing"
        self.gridExportPlan="Missing"
        self.personalExcedentsPlan="Missing"