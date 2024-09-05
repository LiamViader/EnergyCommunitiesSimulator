import pandas as pd
from datetime import datetime,date,timedelta
from Community.Sharing.sharingMethod import SharingMethod
from Profiles.profile import Profile
from Profiles.Factors.baseFactor import BaseFactor
from typing import List, Tuple, Dict
from utils.enums import FactorType
from Simulation.simulationConfiguration import SimulationConfig
from Profiles.utils.profileSharingsDataAux import ProfileSharingsDataAux
from Profiles.utils.profileCostDataAux import ProfileCostDataAux
from Community.Costs.costCalculationBaseMethod import CostCalculationBaseMethod
import numpy as np

class SimulatedCommunity:
    def __init__(self) -> None:
        self.detailedSimulatedProfiles = pd.DataFrame({
            'datetime': pd.to_datetime([]),
            'profile_id': pd.Series(dtype='int'),
            'profile_name': pd.Series(dtype='str'),
            'asset_id': pd.Series(dtype='int'),
            'asset_name': pd.Series(dtype='str'),
            'energy': pd.Series(dtype='float32'),
            'asset_type': pd.Series(dtype='str')
        })
        self.detailedSimulatedProfiles.set_index(['datetime', 'profile_id', 'asset_id'], inplace=True)

        self.summarizedSimulatedProfiles = pd.DataFrame({
            'datetime': pd.to_datetime([]),
            'profile_id': pd.Series(dtype='int'),
            'profile_name': pd.Series(dtype='str'),
            'load': pd.Series(dtype='float32'),
            'pv': pd.Series(dtype='float32')
        })
        self.summarizedSimulatedProfiles.set_index(['datetime', 'profile_id'], inplace=True)

        self.simulatedCommunityAssets = pd.DataFrame({
            'datetime': pd.to_datetime([]),
            'asset_id': pd.Series(dtype='int'),
            'asset_name': pd.Series(dtype='str'),
            'energy': pd.Series(dtype='float32'),
            'asset_type': pd.Series(dtype='str')
        })
        self.simulatedCommunityAssets.set_index(['datetime', 'asset_id'], inplace=True)

        self.communityPv = pd.DataFrame({
            'datetime': pd.to_datetime([]),
            'pv': pd.Series(dtype='float32')
        })
        self.communityPv.set_index(['datetime'], inplace=True)

        self.externalFactors = pd.DataFrame({
            'datetime': pd.to_datetime([]),
            'temperature': pd.Series(dtype='float32'),
            'irradiation': pd.Series(dtype='float32'),
            'wind': pd.Series(dtype='float32')
        })
        self.externalFactors.set_index(['datetime'], inplace=True)

        self.sharingInfo = pd.DataFrame({
            'datetime': pd.to_datetime([]),
            'method': pd.Series(dtype='str'),
            'shared_personal_pvs': pd.Series(dtype='bool')
        })
        self.sharingInfo.set_index(['datetime'], inplace=True)

        self.energySharings = pd.DataFrame({
            'datetime': pd.to_datetime([]),
            'profile_id': pd.Series(dtype='int'),
            'community_shares': pd.Series(dtype='float32'),
            'grid_import': pd.Series(dtype='float32'),
            'microgrid_import': pd.Series(dtype='float32'),
            'grid_export': pd.Series(dtype='float32'),
            'microgrid_export': pd.Series(dtype='float32'),
            'personal_pv_excedent': pd.Series(dtype='float32'),
            'total_pv_able_to_share': pd.Series(dtype='float32'), #en cas que nomes es comparteixi assets de la comunitat, això es pv del asset de la comunitat * community shares (el percentatge que té), si tb comparteix els seus assets serà lo anterior + el pv seu

        })
        self.energySharings.set_index(['datetime','profile_id'], inplace=True)

        self.costs = pd.DataFrame({
            'datetime': pd.to_datetime([]),
            'profile_id': pd.Series(dtype='int'),
            'grid_import_price': pd.Series(dtype='float32'),
            'grid_import_cost': pd.Series(dtype='float32'),
            'grid_import_plan': pd.Series(dtype='str'),
            'grid_export_price': pd.Series(dtype='float32'),
            'grid_export_revenue': pd.Series(dtype='float32'),
            'grid_export_plan': pd.Series(dtype='str'),
            'microgrid_price': pd.Series(dtype='float32'),
            'microgrid_cost': pd.Series(dtype='float32'),
            'microgrid_revenue': pd.Series(dtype='float32'),
            'personal_excedents_price': pd.Series(dtype='float32'),
            'personal_excedents_revenue': pd.Series(dtype='float32'),
            'personal_excedents_plan': pd.Series(dtype='str'),
        })
        self.costs.set_index(['datetime','profile_id'], inplace=True)

        self.costCalculationInfo=pd.DataFrame({
            'datetime': pd.to_datetime([]),
            'method': pd.Series(dtype='str'),
        })
        self.costCalculationInfo.set_index(['datetime'],inplace=True)
        

    def add_profiles_simulation_day(self,profiles:List[Profile],currentDate:date,override:bool=True)->None:
        #detailed
        rows_to_add = []
        for profile in profiles:
            detailedProfile=profile.get_detailed_load()
            profileId=profile.get_id()
            profileName=profile.get_name()
            for asset, energy in detailedProfile.items():
                indices=energy.size
                minutesPerIndex=1440/indices
                assetId=asset.get_id()
                assetName=asset.get_name()
                assetType=asset.get_factor_type().name
                if assetType==FactorType.Producer: coef=-1
                else: coef=1
                for i in range(indices):
                    timestamp = pd.to_datetime(currentDate) + timedelta(minutes=i * minutesPerIndex)
                    row = {
                        'datetime': timestamp,
                        'profile_id': profileId,
                        'profile_name': profileName,
                        'asset_id': assetId,
                        'asset_name': assetName,
                        'energy': energy[i]*coef,
                        'asset_type': assetType
                    }
                    rows_to_add.append(row)

        new_data = pd.DataFrame(rows_to_add)
        if not new_data.empty:
            new_data['datetime'] = pd.to_datetime(new_data['datetime'])
            new_data['energy'] = new_data['energy'].astype('float32')
            new_data.set_index(['datetime', 'profile_id', 'asset_id'], inplace=True)


        #combined
        rows_to_add = []
        for profile in profiles:
            load,pv=profile.get_load_pv()
            profileId=profile.get_id()
            profileName=profile.get_name()
            indices=load.size
            minutesPerIndex=1440/indices
            for i in range(indices):
                timestamp = pd.to_datetime(currentDate) + timedelta(minutes=i * minutesPerIndex)
                row = {
                    'datetime': timestamp,
                    'profile_id': profileId,
                    'profile_name': profileName,
                    'load': load[i],
                    'pv': pv[i]
                }
                rows_to_add.append(row)

            new_data2=pd.DataFrame(rows_to_add)
            if not new_data2.empty:
                new_data2['datetime'] = pd.to_datetime(new_data2['datetime'])
                new_data2['load'] = new_data2['load'].astype('float32')
                new_data2['pv'] = new_data2['pv'].astype('float32')
                new_data2.set_index(['datetime', 'profile_id'], inplace=True)
                

        if override:
            if not new_data.empty:
                combined_data = pd.concat([self.detailedSimulatedProfiles, new_data])
                #elimino duplicats basat en datetime, profileid i assetid
                combined_data = combined_data[~combined_data.index.duplicated(keep='last')]
                self.detailedSimulatedProfiles = combined_data.sort_index()
            if not new_data2.empty:
                combined_data2 = pd.concat([self.summarizedSimulatedProfiles,new_data2])
                combined_data2 = combined_data2[~combined_data2.index.duplicated(keep='last')]
                self.summarizedSimulatedProfiles = combined_data2.sort_index()

            
        else:
            if not new_data.empty:
                combined_data = pd.concat([self.detailedSimulatedProfiles, new_data])
                #elimino duplicats basat en datetime, profileid i assetid
                combined_data = combined_data[~combined_data.index.duplicated(keep='first')]
                self.detailedSimulatedProfiles = combined_data.sort_index()
            if not new_data2.empty:
                combined_data2 = pd.concat([self.summarizedSimulatedProfiles,new_data2])
                combined_data2 = combined_data2[~combined_data2.index.duplicated(keep='first')]
                self.summarizedSimulatedProfiles = combined_data2.sort_index()

    def add_simulated_community_pv(self,totalPv:np.ndarray,detailedPv:Dict[BaseFactor,np.ndarray],currentDate:date,override:bool=True)->None:
        detailed_rows_to_add = []
        for asset, energy in detailedPv.items():
            indices=energy.size
            minutesPerIndex=1440/indices
            assetId=asset.get_id()
            assetName=asset.get_name()
            assetType=asset.get_factor_type().name
            if assetType==FactorType.Producer: coef=-1
            else: coef=1
            for i in range(indices):
                timestamp = pd.to_datetime(currentDate) + timedelta(minutes=i * minutesPerIndex)
                row = {
                    'datetime': timestamp,
                    'asset_id': assetId,
                    'asset_name': assetName,
                    'energy': energy[i]*coef,
                    'asset_type': assetType
                }
                detailed_rows_to_add.append(row)

        new_detailed_data = pd.DataFrame(detailed_rows_to_add)

        if not new_detailed_data.empty:
            new_detailed_data['datetime'] = pd.to_datetime(new_detailed_data['datetime'])
            new_detailed_data['energy'] = new_detailed_data['energy'].astype('float32')
            new_detailed_data.set_index(['datetime', 'asset_id'], inplace=True)

        pv_rows_to_add = []
        indices=totalPv.size
        minutesPerIndex=1440/indices
        for i in range(indices):
            timestamp = pd.to_datetime(currentDate) + timedelta(minutes=i * minutesPerIndex)
            row = {
                'datetime': timestamp,
                'pv': totalPv[i],
            }
            pv_rows_to_add.append(row)
        
        new_pv_data = pd.DataFrame(pv_rows_to_add)

        if not new_pv_data.empty:
            new_pv_data['datetime'] = pd.to_datetime(new_pv_data['datetime'])
            new_pv_data['pv'] = new_pv_data['pv'].astype('float32')
            new_pv_data.set_index(['datetime'], inplace=True)

        if override:
            if not new_detailed_data.empty:
                combined_detailed_data = pd.concat([self.detailedSimulatedProfiles, new_detailed_data])
                #elimino duplicats antics basat en datetime, assetid
                combined_detailed_data = combined_detailed_data[~combined_detailed_data.index.duplicated(keep='last')]
                self.simulatedCommunityAssets = combined_detailed_data.sort_index()
            if not new_pv_data.empty:
                combined_pv_data = pd.concat([self.communityPv, new_pv_data])
                #elimino duplicats antics basat en datetime, assetid
                combined_pv_data = combined_pv_data[~combined_pv_data.index.duplicated(keep='last')]
                self.communityPv = combined_pv_data.sort_index()

            
        else:
            if not new_detailed_data.empty:
                combined_detailed_data = pd.concat([self.detailedSimulatedProfiles, new_detailed_data])
                #elimino duplicats nous basat en datetime, assetid
                combined_detailed_data = combined_detailed_data[~combined_detailed_data.index.duplicated(keep='first')]
                self.simulatedCommunityAssets = combined_detailed_data.sort_index()
            if not new_pv_data.empty:
                combined_pv_data = pd.concat([self.communityPv, new_pv_data])
                #elimino duplicats nous basat en datetime, assetid
                combined_pv_data = combined_pv_data[~combined_pv_data.index.duplicated(keep='first')]
                self.communityPv = combined_pv_data.sort_index()

    def add_simulated_external_factors(self,simulationConfig:SimulationConfig,currentDate:date,override:bool=True)->None:
        rows_to_add = []
        irradiation=simulationConfig.get_irradiation()
        wind=simulationConfig.get_wind()
        temperature=simulationConfig.get_temperature()
        indices=simulationConfig.num_indices()
        minutesPerIndex=1440/indices
        for i in range(indices):
            timestamp = pd.to_datetime(currentDate) + timedelta(minutes=i * minutesPerIndex)
            row = {
                'datetime': timestamp,
                'irradiation': irradiation[i],
                'temperature': temperature[i],
                'wind': wind[i],
            }
            rows_to_add.append(row)

        new_data = pd.DataFrame(rows_to_add)
        if not new_data.empty:
            new_data['datetime'] = pd.to_datetime(new_data['datetime'])
            new_data['temperature'] = new_data['temperature'].astype('float32')
            new_data['irradiation'] = new_data['irradiation'].astype('float32')
            new_data['wind'] = new_data['wind'].astype('float32')
            new_data.set_index(['datetime'], inplace=True)

        if override:
            if not new_data.empty:
                combined_data = pd.concat([self.externalFactors, new_data])
                #elimino duplicats basat en datetime, profileid i assetid
                combined_data = combined_data[~combined_data.index.duplicated(keep='last')]
                self.externalFactors = combined_data.sort_index()
        else:
            if not new_data.empty:
                combined_data = pd.concat([self.externalFactors, new_data])
                #elimino duplicats basat en datetime, profileid i assetid
                combined_data = combined_data[~combined_data.index.duplicated(keep='first')]
                self.externalFactors = combined_data.sort_index()

    def add_sharing_info(self,datetimes:List[datetime],sharingMethod:SharingMethod,sharedPersonalPvs:bool)->None: #adds the sharing info used for share from start to end
        rowsToAdd=[]
        sharingMethodStr=sharingMethod.get_name()
        for dateTime in datetimes:
            row={
                'datetime': dateTime,
                'method': sharingMethodStr,
                'shared_personal_pvs': sharedPersonalPvs
            }
            rowsToAdd.append(row)
        new_data = pd.DataFrame(rowsToAdd)
        if not new_data.empty:
            new_data['datetime'] = pd.to_datetime(new_data['datetime'])
            new_data['method'] = new_data['method'].astype('str')
            new_data['shared_personal_pvs'] = new_data['shared_personal_pvs'].astype('bool')
            new_data.set_index(['datetime'], inplace=True)

            combined_data = pd.concat([self.sharingInfo, new_data])
            combined_data = combined_data[~combined_data.index.duplicated(keep='last')]
            self.sharingInfo = combined_data.sort_index()
    
    def add_energy_sharings(self,energySharings:Dict[datetime,List[ProfileSharingsDataAux]])->None:
        rowsToAdd=[]
        for datetime_value, energySharingsProfiles in energySharings.items():
            for profileSharings in energySharingsProfiles:
                row={
                    'datetime': datetime_value,
                    'profile_id': profileSharings.id,
                    'community_shares': profileSharings.communityShares,
                    'grid_import': profileSharings.gridImport,
                    'microgrid_import': profileSharings.microgridImport,
                    'grid_export': profileSharings.gridExport,
                    'microgrid_export': profileSharings.microgridExport,
                    'personal_pv_excedent': profileSharings.personalPvExcedent,
                    'total_pv_able_to_share': profileSharings.totalPvAbleToShare
                }
                rowsToAdd.append(row)
        new_data = pd.DataFrame(rowsToAdd)
        if not new_data.empty:
            new_data['datetime'] = pd.to_datetime(new_data['datetime'])
            new_data['profile_id'] = new_data['profile_id'].astype('int')
            new_data['community_shares'] = new_data['community_shares'].astype('float32')
            new_data['grid_import'] = new_data['grid_import'].astype('float32')
            new_data['microgrid_import'] = new_data['microgrid_import'].astype('float32')
            new_data['grid_export'] = new_data['grid_export'].astype('float32')
            new_data['microgrid_export'] = new_data['microgrid_export'].astype('float32')
            new_data['personal_pv_excedent'] = new_data['personal_pv_excedent'].astype('float32')
            new_data['total_pv_able_to_share'] = new_data['total_pv_able_to_share'].astype('float32')
            new_data.set_index(['datetime', 'profile_id'], inplace=True)

            combined_data = pd.concat([self.energySharings, new_data])
            combined_data = combined_data[~combined_data.index.duplicated(keep='last')]
            self.energySharings = combined_data.sort_index()
    
    def add_costs(self,costs:Dict[datetime,List[ProfileCostDataAux]])->None:
        rowsToAdd=[]
        for datetime_value, costsList in costs.items():
            for profileCost in costsList:
                row={
                    'datetime': datetime_value,
                    'profile_id': profileCost.id,
                    'grid_import_price': profileCost.gridImportPrice,
                    'grid_import_cost': profileCost.gridImportCost,
                    'grid_import_plan': profileCost.gridImportPlan,
                    'grid_export_price': profileCost.gridExportPrice,
                    'grid_export_revenue': profileCost.gridExportRevenue,
                    'grid_export_plan': profileCost.gridExportPlan,
                    'microgrid_price': profileCost.microgridPrice,
                    'microgrid_cost': profileCost.microgridCost,
                    'microgrid_revenue': profileCost.microgridRevenue,
                    'personal_excedents_price': profileCost.personalExcedentsPrice,
                    'personal_excedents_revenue': profileCost.personalExcedentsRevenue,
                    'personal_excedents_plan': profileCost.personalExcedentsPlan,
                }
                rowsToAdd.append(row)
        new_data = pd.DataFrame(rowsToAdd)
        if not new_data.empty:
            new_data['datetime'] = pd.to_datetime(new_data['datetime'])
            new_data['profile_id'] = new_data['profile_id'].astype('int')
            new_data['grid_import_price'] = new_data['grid_import_price'].astype('float32')
            new_data['grid_import_cost'] = new_data['grid_import_cost'].astype('float32')
            new_data['grid_import_plan'] = new_data['grid_import_plan'].astype('str')
            new_data['grid_export_price'] = new_data['grid_export_price'].astype('float32')
            new_data['grid_export_revenue'] = new_data['grid_export_revenue'].astype('float32')
            new_data['grid_export_plan'] = new_data['grid_export_plan'].astype('str')
            new_data['microgrid_price'] = new_data['microgrid_price'].astype('float32')
            new_data['microgrid_cost'] = new_data['microgrid_cost'].astype('float32')
            new_data['microgrid_revenue'] = new_data['microgrid_revenue'].astype('float32')
            new_data['personal_excedents_price'] = new_data['personal_excedents_price'].astype('float32')
            new_data['personal_excedents_revenue'] = new_data['personal_excedents_revenue'].astype('float32')
            new_data['personal_excedents_plan'] = new_data['personal_excedents_plan'].astype('str')
            new_data.set_index(['datetime', 'profile_id'], inplace=True)

            combined_data = pd.concat([self.costs, new_data])
            combined_data = combined_data[~combined_data.index.duplicated(keep='last')]
            self.costs = combined_data.sort_index()

    def add_cost_calculation_info(self,datetimes:List[datetime],method:CostCalculationBaseMethod)->None:
        rowsToAdd=[]
        methodStr=method.get_name()
        for dateTime in datetimes:
            row={
                'datetime': dateTime,
                'method': methodStr,
            }
            rowsToAdd.append(row)
        new_data = pd.DataFrame(rowsToAdd)
        if not new_data.empty:
            new_data['datetime'] = pd.to_datetime(new_data['datetime'])
            new_data['method'] = new_data['method'].astype('str')
            new_data.set_index(['datetime'], inplace=True)

            combined_data = pd.concat([self.costCalculationInfo, new_data])
            combined_data = combined_data[~combined_data.index.duplicated(keep='last')]
            self.costCalculationInfo = combined_data.sort_index()

    def get_summarized_simulated_profiles(self,start:datetime=None,end:datetime=None)->pd.DataFrame:#includes end includes start. if None then infinity. Retorna el df Filtrat i ordenat si sort=true
        
        if start is not None and end is not None:
            filtered_df=self.summarizedSimulatedProfiles.loc[start:end]
        elif end is not None:
            filtered_df=self.summarizedSimulatedProfiles.loc[:end]
        elif start is not None:
            filtered_df=self.summarizedSimulatedProfiles.loc[start:]
        else:
            filtered_df=self.summarizedSimulatedProfiles.loc[:]
    
        
        return filtered_df
    
    def get_community_pvs(self,start:datetime=None,end:datetime=None)->pd.DataFrame:

        if start is not None and end is not None:
            filtered_df=self.communityPv.loc[start:end]
        elif end is not None:
            filtered_df=self.communityPv.loc[:end]
        elif start is not None:
            filtered_df=self.communityPv.loc[start:]
        else:
            filtered_df=self.communityPv.loc[:]
        

        return filtered_df
    
    def get_energy_sharings(self,start:datetime=None,end:datetime=None)->pd.DataFrame:

        if start is not None and end is not None:
            filtered_df=self.energySharings.loc[start:end]
        elif end is not None:
            filtered_df=self.energySharings.loc[:end]
        elif start is not None:
            filtered_df=self.energySharings.loc[start:]
        else:
            filtered_df=self.energySharings.loc[:]
        

        return filtered_df
    
    def get_total_community_cost(self,start:datetime=None,end:datetime=None)->float:
        if start is not None and end is not None:
            filtered_df=self.costs.loc[start:end]
        elif end is not None:
            filtered_df=self.costs.loc[:end]
        elif start is not None:
            filtered_df=self.costs.loc[start:]
        else:
            filtered_df=self.costs.loc[:]
        
        columnsToSum = ['grid_import_cost', 'microgrid_cost']
        columnsToSubstract = ['grid_export_revenue', 'microgrid_revenue','personal_excedents_revenue']
        rowResults = self.costs[columnsToSum].sum(axis=1) - self.costs[columnsToSubstract].sum(axis=1)
        totalResult = rowResults.sum()
        return totalResult
        
