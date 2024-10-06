
from Profiles.profile import Profile
from Profiles.utils.profileEnergyDataAux import ProfileEnergyDataAux
from Profiles.utils.profileSharingsDataAux import ProfileSharingsDataAux
from Profiles.utils.profileCostDataAux import ProfileCostDataAux
from utils.enums import FactorType, MarketCountry
from Community.Sharing.sharingMethod import SharingMethod
from Community.Sharing.virtualNetBilling import VirtualNetBilling
from Community.Sharing.sequentialSharing import SequentialSharing
from Simulation.simulationConfiguration import SimulationConfig
from Community.Costs.costCalculationBaseMethod import CostCalculationBaseMethod
from Profiles.Factors.baseFactor import BaseFactor
from EnergyPrice.EnergyPlans.baseEnergyPlan import BaseEnergyPlan
from Simulation.simulatedCommunity import SimulatedCommunity
from EnergyPrice.wholesaleMarket import WholesaleMarket
from EnergyPrice.EnergyPlans.SomEnergia.somEnergiaIndexadaDomestic import SomEnergiaIndexadaDomestic
from typing import List, Tuple, Optional, Dict
import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta

import pyswarms as ps

from pyswarms.single.global_best import GlobalBestPSO

class Community():
    """
    Represents a community that consists of multiple profiles, energy production assets, and sharing methods.

    Attributes:
        _profiles (dict): A dictionary mapping profile IDs to Profile instances.
        _profilesShare (dict): A dictionary mapping profile IDs to their respective sharing percentages.
        _communityAssets (List[BaseFactor]): A list of community assets that can produce energy.
        _sharePersonalPvs (bool): Indicates if personal production should be shared with the community .
        _energyPlan (BaseEnergyPlan): The energy plan applied to the community.
        _costCalculationMethod (CostCalculationBaseMethod): The method used for cost calculation (specifys if the cost calculation should be using each profile plan, the community plan or the best option).
        _sharingMethod (SharingMethod): The method used for sharing energy within the community.
        _wholesaleMarketCountry (MarketCountry): The country in which the wholesale market operates.
        _pv (np.ndarray): The total photovoltaic energy produced in the community during the current day simulation.
        _detailedPv (Dict[BaseFactor, np.ndarray]): Detailed energy production from community assets during the  current day simulation.
        _simulatedCommunity (SimulatedCommunity): The simulated community containing simulation results of all the simulated days.
        _configLastSimulation (SimulationConfig): Configuration of the last simulation run.

    Methods:
        simulate(simulationConfig: SimulationConfig) -> None:
            Runs a day simulation based on the provided configuration.

        shareSimulatedEnergies(start: datetime=None, end: datetime=None) -> None:
            Shares simulated energy among profiles based on the defined sharing method.

        recalculate_cost(start: datetime=None, end: datetime=None) -> None:
            Recalculates costs for energy sharing within a specific time frame.

        optimize_shares_best_community_cost(start: datetime=None, end: datetime=None, saveSharesOptimized=False) -> Dict[int, float]:
            Optimizes each profile shares of community to minimize community costs.

        set_sharing_method(sharingMethod: SharingMethod) -> None:
            Sets the method used for sharing energy among profiles.

        set_share_personal_pvs(b: bool) -> None:
            Sets the flag indicating whether to share personal PV production.

        get_simulated_community() -> SimulatedCommunity:
            Returns the simulated community object.
    """
    def __init__(self,profiles:List[Tuple[Profile,float]],
                 communityAssets:List[BaseFactor],
                 energyPlan:BaseEnergyPlan,
                 costCalculationMethod:CostCalculationBaseMethod,
                 sharePersonalPvs:bool=False,
                 sharingMethod:SharingMethod=SequentialSharing(),
                 wholesaleMarketCountry:MarketCountry=MarketCountry.Spain) -> None:
        
        """
        Initializes the Community instance.

        Args:
            profiles (List[Tuple[Profile, float]]): A list of tuples containing Profile instances and their corresponding sharing percentages.
            communityAssets (List[BaseFactor]): A list of community assets that can produce energy.
            energyPlan (BaseEnergyPlan): The energy plan applied to the community.
            costCalculationMethod (CostCalculationBaseMethod): The method used for cost calculation.
            sharePersonalPvs (bool, optional): Flag to indicate whether personal production should be shared. Defaults to False.
            sharingMethod (SharingMethod, optional): The method used for sharing energy within the community. Defaults to SequentialSharing().
            wholesaleMarketCountry (MarketCountry, optional): The country for the wholesale market. Defaults to MarketCountry.Spain.
        """

        self._profiles= {tuple[0].get_id(): tuple[0] for tuple in profiles}
        self._profilesShare={tuple[0].get_id(): tuple[1] for tuple in profiles}
        self._communityAssets=communityAssets
        self._sharePersonalPvs=sharePersonalPvs
        self._energyPlan=energyPlan
        self._costCalculationMethod=costCalculationMethod
        self._pv=None
        self._detailedPv:Dict[BaseFactor,np.ndarray]={}
        self._sharingMethod=sharingMethod
        self._configLastSimulation=None
        self._simulatedCommunity=SimulatedCommunity()
        WholesaleMarket(country=wholesaleMarketCountry)


    def simulate(self,simulationConfig:SimulationConfig)->None:
        """
        Runs a day simulation for the community based on the given simulation configuration.

        Args:
            simulationConfig (SimulationConfig): Configuration settings for the simulation run.

        Raises:
            ValueError: If any error occurs during simulation.
        """

        self._simulate_community_assets(simulationConfig)

        for profile_id, profile in self._profiles.items():
            profile.simulate(simulationConfig=simulationConfig)
        
        self._update_simulateds(list(self._profiles.values()),simulationConfig)
        self._share_on_current_date(simulationConfig)
        

        self._configLastSimulation=simulationConfig
    

    def _simulate_community_assets(self,simulationConfig:SimulationConfig)->None:
        """
        Simulates the energy production of community assets based on the given simulation configuration.

        Args:
            simulationConfig (SimulationConfig): Configuration settings for the simulation run.
        """
        self._detailedPv:Dict[BaseFactor,np.ndarray]={}
        self._pv=np.zeros(simulationConfig.num_indices())
        for asset in self._communityAssets:
            assetLoad=asset.simulate(simulationConfig=simulationConfig)
            if asset.get_factor_type()==FactorType.Producer:
                self._pv+=assetLoad
                self._detailedPv[asset]=assetLoad

    def _update_simulateds(self,profiles:List[Profile],simulationConfig:SimulationConfig)->None:
        """
        Updates the simulatedCommunity data for profiles, community PV and external factors after the current day simulation.

        Args:
            profiles (List[Profile]): A list of Profile instances to update.
            simulationConfig (SimulationConfig): Configuration settings for the simulation run.
        """
        self._simulatedCommunity.add_profiles_simulation_day(profiles,simulationConfig.get_current_date(),override=True)
        self._simulatedCommunity.add_simulated_community_pv(self._pv,self._detailedPv,simulationConfig.get_current_date(),override=True)
        self._simulatedCommunity.add_simulated_external_factors(simulationConfig,simulationConfig.get_current_date(),override=True)

    def _share_on_current_date(self,simulationConfig:SimulationConfig)->None:
        """
        Shares simulated energy for the current date based on the simulation configuration.

        Args:
            simulationConfig (SimulationConfig): Configuration settings for the simulation run.
        """
        currentDate=simulationConfig.get_current_date()
        datetimeStart = datetime.combine(currentDate,time.min)
        datetimeEnd = datetime.combine(currentDate, time.max)
        self.shareSimulatedEnergies(datetimeStart,datetimeEnd)

    def shareSimulatedEnergies(self,start:datetime=None,end:datetime=None)->None: #shares the simulated energy using the self._sharingMethod on the range of time start-end (includes start includes end). si algun dels limits del rang es None, significa infinit
        """
        Shares the simulated energy among profiles for the specified time range.

        This method uses energy profiles and community pv data from the simulated community and processes it to 
        compute the detailed shared energy each individual obtains, then updates _simulatedCommunity.

        Args:
            start (datetime, optional): Start time for sharing. Defaults to None (infinity).
            end (datetime, optional): End time for sharing. Defaults to None (infinity).

        Raises:
            ValueError: If duplicate profile IDs are found during sharing.
        """
        profilesDf=self._simulatedCommunity.get_summarized_simulated_profiles(start,end)
        communityPvs=self._simulatedCommunity.get_community_pvs(start,end)
        groupedByDateTime = profilesDf.groupby(level='datetime')
        sharingInfoDatetimes:List[datetime]=[]
        profilesEnergySharings:Dict[datetime,List[ProfileSharingsDataAux]]={}
        for datetime_value, group in groupedByDateTime:
            duplicated_profile_ids = group.index.get_level_values('profile_id').duplicated(keep=False)
            if duplicated_profile_ids.any():
                raise ValueError(f"Duplicate profile_id found in energy simulated with datetime {datetime_value}")
            
            profile_ids = group.index.get_level_values('profile_id')
            profile_names = group['profile_name']
            pv = group['pv']
            load = group['load']
            profileDataList:List[ProfileEnergyDataAux]=[]
            for profile_id, profile_name, pv_value, load_value in zip(profile_ids, profile_names, pv, load):
                profileShare = self._profilesShare.get(profile_id, 0)
                profileData = ProfileEnergyDataAux(
                    id=profile_id,
                    name=profile_name,
                    production=pv_value,
                    load=load_value,
                    share=profileShare
                )
                profileDataList.append(profileData)
            communityPvRows = communityPvs[communityPvs.index.get_level_values('datetime') == datetime_value]
            if communityPvRows.empty:
                communityPv = 0
                print(f"There's no community pv instance for {datetime_value}")
            else:
                if len(communityPvRows) > 1:
                    print(f"There's more than one community pv instance for {datetime_value}")
                communityPv = communityPvRows.iloc[0]["pv"]
            sharingInfoDatetimes.append(datetime_value)
            profilesEnergySharings[datetime_value]=self._sharingMethod.share(profiles=profileDataList,sharePersonalPvs=self._sharePersonalPvs,communityPv=communityPv)

        self._simulatedCommunity.add_sharing_info(datetimes=sharingInfoDatetimes,sharingMethod=self._sharingMethod,sharedPersonalPvs=self._sharePersonalPvs)
        self._simulatedCommunity.add_energy_sharings(energySharings=profilesEnergySharings)
        self._calculate_and_save_costs(sharings=profilesEnergySharings)

    def recalculate_cost(self,start:datetime=None,end:datetime=None)->None:
        """
        Recalculates the cost of energy sharing within the community based on the specified date range.

        This method uses energy sharing data from the simulated community and processes it to 
        compute the costs associated with energy imports and exports for each profile in the community.

        Args:
            start (datetime, optional): The start date for the calculation period. Defaults to None(infinity).
            end (datetime, optional): The end date for the calculation period. Defaults to None(infinity).

        Raises:
            ValueError: If duplicate profile IDs are found in the energy sharing data for a given datetime.

        """
        energySharingsDf=self._simulatedCommunity.get_energy_sharings(start,end)
        groupedByDateTime = energySharingsDf.groupby(level='datetime')
        profilesEnergySharings:Dict[datetime,List[ProfileSharingsDataAux]]={}
        for datetime_value, group in groupedByDateTime:
            duplicated_profile_ids = group.index.get_level_values('profile_id').duplicated(keep=False)
            if duplicated_profile_ids.any():
                raise ValueError(f"Duplicate profile_id found in energy sharings with datetime {datetime_value}")
            profilesEnergySharings[datetime_value]=[]
            profile_ids = group.index.get_level_values('profile_id')
            gridImports = group['grid_import']
            microgridImports = group['microgrid_import']
            gridExports = group['grid_export']
            microgridExports = group['microgrid_export']
            personalPvExcedents = group['personal_pv_excedent']
            communityShares = group['community_shares']
            totalPvsAbleToShare = group['total_pv_able_to_share']
            for profile_id, gridImport, microgridImport, gridExport, microgridExport, personalPvExcedent, communityShare, totalPvAbleToShare  in zip(profile_ids, gridImports, microgridImports, gridExports, microgridExports, personalPvExcedents, communityShares, totalPvsAbleToShare):
                aux=ProfileSharingsDataAux(profile_id=profile_id)
                aux.gridImport=gridImport
                aux.gridExport=gridExport
                aux.microgridExport=microgridExport
                aux.microgridImport=microgridImport
                aux.personalPvExcedent=personalPvExcedent
                aux.communityShares=communityShare
                aux.totalPvAbleToShare=totalPvAbleToShare
                profilesEnergySharings[datetime_value].append(aux)
            self._calculate_and_save_costs(sharings=profilesEnergySharings)
    
    def _calculate_and_save_costs(self,sharings:Dict[datetime,List[ProfileSharingsDataAux]])->Dict[datetime,List[ProfileCostDataAux]]:
        """
        Calculates the costs associated with the energy sharing data and saves the results to the simulated community.

        Args:
            sharings (Dict[datetime, List[ProfileSharingsDataAux]]): A dictionary containing energy sharing data grouped by datetime.

        Returns:
            Dict[datetime, List[ProfileCostDataAux]]: A dictionary mapping each datetime to a list of associated profile costs.
        """
        costs:Dict[datetime,List[ProfileCostDataAux]]={}
        for datetime_value, profileSharingsList in sharings.items():
            costs[datetime_value]=[]
            profileSharingsAndPlans:List[Tuple[ProfileSharingsDataAux,BaseEnergyPlan]]=[
                (
                    profileSharingsAux,
                    self._profiles[profileSharingsAux.id].get_energy_plan() 
                    if profileSharingsAux.id in self._profiles 
                    else SomEnergiaIndexadaDomestic(contractedPower=5,iva=21) #en cas que el perfil no existeixi a self._profiles (mai hauria de pasar, pero per donar un plan default)
                )
                for profileSharingsAux in profileSharingsList
            ]
            costs[datetime_value]=self._costCalculationMethod.calculate(sharingsAndPlan=profileSharingsAndPlans,communityPlan=self._energyPlan,datetimeValue=datetime_value)
        self._simulatedCommunity.add_costs(costs=costs)
        datetimes = list(sharings.keys())
        self._simulatedCommunity.add_cost_calculation_info(method=self._costCalculationMethod, datetimes=datetimes)
        return costs

    def _shareAndGetCostOptimized(self,start:datetime=None,end:datetime=None)->float:
        """
        Shares energy among profiles using an optimized method and calculates the total cost.

        This method retrieves the summarized profiles and community PVs, then performs energy sharing
        calculations for the specified date range.

        Args:
            start (datetime, optional): The start date for the energy sharing period. Defaults to None(infinity).
            end (datetime, optional): The end date for the energy sharing period. Defaults to None(infinity).

        Returns:
            float: The total cost of energy sharing for the specified period.

        Raises:
            ValueError: If duplicate profile IDs are found in the energy data for a given datetime.
        """
        totalCost=0
        profilesDf=self._simulatedCommunity.get_summarized_simulated_profiles(start,end)
        communityPvs=self._simulatedCommunity.get_community_pvs(start,end)
        groupedByDateTime = profilesDf.groupby(level='datetime')
        for datetime_value, group in groupedByDateTime:
            duplicated_profile_ids = group.index.get_level_values('profile_id').duplicated(keep=False)
            if duplicated_profile_ids.any():
                raise ValueError(f"Duplicate profile_id found in energy simulated with datetime {datetime_value}")
            
            profile_ids = group.index.get_level_values('profile_id')
            profile_names = group['profile_name']
            pv = group['pv']
            load = group['load']
            profileDataList:List[ProfileEnergyDataAux]=[]
            for profile_id, profile_name, pv_value, load_value in zip(profile_ids, profile_names, pv, load):
                profileShare = self._profilesShare.get(profile_id, 0)
                profileData = ProfileEnergyDataAux(
                    id=profile_id,
                    name=profile_name,
                    production=pv_value,
                    load=load_value,
                    share=profileShare
                )
                profileDataList.append(profileData)
            communityPvRows = communityPvs[communityPvs.index.get_level_values('datetime') == datetime_value]
            if communityPvRows.empty:
                communityPv = 0
                print(f"There's no community pv instance for {datetime_value}")
            else:
                if len(communityPvRows) > 1:
                    print(f"There's more than one community pv instance for {datetime_value}")
                communityPv = communityPvRows.iloc[0]["pv"]
            sharingsList=self._sharingMethod.share(profiles=profileDataList,sharePersonalPvs=self._sharePersonalPvs,communityPv=communityPv)
            profileSharingsAndPlans:List[Tuple[ProfileSharingsDataAux,BaseEnergyPlan]]=[
                (
                    profileSharingsAux,
                    self._profiles[profileSharingsAux.id].get_energy_plan() 
                    if profileSharingsAux.id in self._profiles 
                    else SomEnergiaIndexadaDomestic(contractedPower=5,iva=21) #en cas que el perfil no existeixi a self._profiles (mai hauria de pasar, pero per donar un plan default)
                )
                for profileSharingsAux in sharingsList
            ]
            profilesCostList=self._costCalculationMethod.calculate(sharingsAndPlan=profileSharingsAndPlans,communityPlan=self._energyPlan,datetimeValue=datetime_value)
            for profileCost in profilesCostList:
                totalCost+=profileCost.gridImportCost+profileCost.microgridCost-profileCost.gridExportRevenue-profileCost.microgridRevenue-profileCost.personalExcedentsRevenue
        return totalCost



    def optimize_shares_best_community_cost(self,start:datetime=None,end:datetime=None,saveSharesOptimized=False)->Dict[int,float]:
        """
        Optimizes the energy sharing weights to minimize the total community cost over a specified period.

        This method uses a particle swarm optimization approach to find the best weights for energy sharing among profiles.

        Args:
            start (datetime, optional): The start date for the optimization period. Defaults to None(infinity).
            end (datetime, optional): The end date for the optimization period. Defaults to None(infinity).
            saveSharesOptimized (bool, optional): If True, saves the optimized sharing weights for the current community. Defaults to False.

        Returns:
            Dict[int, float]: A dictionary mapping profile IDs to their optimized sharing weights.

        Raises:
            ValueError: If the number of profiles does not match the number of weights.
        """
        def f(weights):
            weights = np.clip(weights, 0, 1)


            sum_weights = np.sum(weights, axis=1, keepdims=True)

            #petita constant per evitar dividir per 0
            epsilon = 1e-10
            sum_weights += epsilon
            normalized_weights = weights / sum_weights



            community_cost=np.zeros(normalized_weights.shape[0])
            for index, row in enumerate(normalized_weights):
                profileIds = list(self._profilesShare.keys())
                if len(profileIds) != len(row):
                    raise ValueError("Diferent numero de perfils que de pesos")
                self._profilesShare={profileId: share for profileId,share in zip(profileIds,row)}
                rowCost=self._shareAndGetCostOptimized(start=start,end=end)
                print(row)
                print(rowCost)
                community_cost[index]=rowCost
                
            #cost total
            total_cost = community_cost

            return total_cost

        profilesShareBeforeOptimitzation=self._profilesShare     
        numberOfProfiles=len(self._profilesShare)
        x_max = np.ones(numberOfProfiles)
        x_min = np.zeros(numberOfProfiles)
        bounds = (x_min, x_max)
        options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9}

        optimizer = GlobalBestPSO(n_particles=5, dimensions=numberOfProfiles, options=options, bounds=bounds)
        cost, weights = optimizer.optimize(f, iters=10)

        sum_weights = np.sum(weights, axis=0)
        epsilon = 1e-10
        sum_weights += epsilon
        normalized_weights = weights / sum_weights
        profileIds = list(self._profilesShare.keys())
        shares={profileId: share for profileId,share in zip(profileIds,normalized_weights)}

        if saveSharesOptimized:
            self._profilesShare=shares
            self.shareSimulatedEnergies(start=start,end=end)
        else:
            self._profilesShare=profilesShareBeforeOptimitzation
        
        return shares


    
    def set_sharing_method(self,sharingMethod:SharingMethod)->None:
        """
        Sets the sharing method used for distributing energy among profiles in the community.

        This method updates the internal sharing method used for calculating how energy is shared 
        among profiles.

        Args:
            sharingMethod (SharingMethod): An instance of the SharingMethod class that defines the 
            strategy for sharing energy among profiles.

        Returns:
            None
        """
        self._sharingMethod=sharingMethod

    def set_share_personal_pvs(self,b:bool)->None:
        """
        Sets whether to include personal production in the energy sharing calculations.

        This method updates a flag that indicates whether personal PV production should be taken 
        into account when calculating energy sharing among profiles in the community.

        Args:
            b (bool): If True, personal production will be included in the calculations; if False, it will not.

        Returns:
            None
        """
        self._sharePersonalPvs=b
            
    def get_simulated_community(self)->SimulatedCommunity:
        """
        Retrieves the simulated community object.

        This method returns the instance of the simulated community, which contains data about 
        profiles, energy sharing, and costs within the community historics.

        Returns:
            SimulatedCommunity: An instance of the SimulatedCommunity class representing the 
            historics of the simulated community.
        """
        return self._simulatedCommunity