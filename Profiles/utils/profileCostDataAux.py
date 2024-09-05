class ProfileCostDataAux:
    def __init__(self, id: int) -> None:
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