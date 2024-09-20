standardSolarPanel=SolarPanel(
    name="solarPanel",
    productionCapacity=0.3,
    efficiency=0.18
)

pv=SolarPV(name="SolarPanels",solarPanels=[standardSolarPanel for i in range(15)])