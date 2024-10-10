class ProfileEnergyDataAux:
    """
    A class to represent the energy data for a specific profile in the community.

    This class holds information about the energy production, consumption (load), 
    and community sharing owned, along with the profile's ID and name.

    Attributes:
        id (int): A unique identifier for the profile.

        name (str): The name of the profile.

        production (float): The amount of energy produced by the profile (in kWh).

        load (float): The amount of energy consumed by the profile (in kWh).

        share (float): The proportion of the community owned by the profile (0-1).
        
        personalPvExcedent (float): The excess energy produced by the profile that is not consumed or shared. 
    """
    def __init__(self, id: int, name:str, production: float, load: float, share: float) -> None:
        """
        Initializes a ProfileEnergyDataAux instance with the provided parameters.

        Args:
            id (int): A unique identifier for the profile.
            name (str): The name of the profile.
            production (float): The energy produced by the profile (in kWh).
            load (float): The energy consumed by the profile (in kWh).
            share (float): The proportion of the community owned by the profile (0-1). 

        Sets the `personalPvExcedent` attribute to 0 by default.
        """
        self.id=id
        self.name=name
        self.production=production
        self.load=load
        self.share=share
        self.personalPvExcedent=0