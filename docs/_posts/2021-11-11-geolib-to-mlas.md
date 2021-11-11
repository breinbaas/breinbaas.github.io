---
layout: post
title:  "Geolib - Converting the Geolib model to my own model"
date:   2021-11-11 12:48:49 +0200
categories: python geolib
---

### What and why?

This article is about converting the geolib (Deltares python codebase for automation using their DSeries software) dataclasses to my own class.. so why would you do that and not simply use and adjust the geolib models.. good question and my answer is.. because it makes my python code more flexible and not dependent on geolib / Deltares software only. 

So what's the idea..

If you work on levee assessments the main ingredients are;
- a crosssection
- soil layers
- soil parameters
- a phreatic and acquifer water level
- some calculation parameters
- a traffic load (or maybe loads)

This is valid for **any** model you use so that's why I have a software agnostic model called ```CalculationModel```, it looks a bit like this;

```python
class CalculationModel(DataModel):
    soils: List[Soil] = []
    soilpolygons: List[CMSoilPolygon] = []
    crosssection: Optional[Crosssection] = None
    phreaticline: List[Point2D] = []
    acquiferline: List[Point2D] = []
```

So you see that most ingredients are there. My entire library is based around this model and has all kinds of nifty things like, adding a ditch to the crosssection by simply using ```add_ditch(self, ditch_start_x: float, ditch_bottom_level: float, ditch_bottom_width: float, ditch_slope: float)``` or automatically finding the location of the transition between crest and polder (in case of 2D subsoil where the soil beneath the dike differs from that in the polder.. which it does!), etc. etc.

So all this functionality is built around this ```CalculationModel``` class. But that does not generate an input file for -for example- the DSeries yet so I also wrote an export function like ```to_dstability(self, filepath: str = "", filename: str = "")``` to generate a file or even ```to_dstability_base64(self) -> str``` to generate bytes to send over the internet (API anyone?). This export option relies heavily on the great Deltares DSeries API so thanks for that.

Now we are getting somewhere because I now have the option to generate calculation files from my code and even call the DSeries to run the file and give me the output. 

### There and back

Exporting calculation files is step one, the other one is a bit more tempting.. reading existing files and converting them to my ```CalculationModel```. For this I had to dive into the geolib code and here is some code that might help other people working on the same problem. The code is off course not complete because it only shows part of the process and uses much more internal logic but again, it might help on your geolib journey. I have added some extra comments which I hope makes things more clear.

```python
@classmethod
def from_stix(cls, filename: str, stage_id: int = 0):
    cm = CalculationModel()  # my model
    dsm = DStabilityModel()    # geolib model
    dsm.parse(Path(filename))  # geolib functionality

    # get the soils and remember the id
    dsmsoils = {}
    for soil in dsm.soils.Soils:
        cm.soils.append(MLSoil.from_dsm_persistable_soil(soil)) # the from_dsm_persistable_soil simply converts the geolib object to my object 
        dsmsoils[soil.Id] = soil.Code

    # get the soilpolygons
    # note that you need 2 things, the SoilLayersId and GeometryId or else you cannot 
    # define which soil id to use for the soillayer
    try:
        geometry_id = dsm.stages[stage_id].GeometryId
        soillayer_collection_id = dsm.stages[stage_id].SoilLayersId        
        waternet_id = dsm.stages[stage_id].WaternetId   
        calculation_settings_id = dsm.stages[stage_id].CalculationSettingsId
        loads_id = dsm.stages[stage_id].LoadsId
    except Exception as e:
        raise ValueError(f"Stage {stage_id} is not defined in {filename}")

    # get the points
    geometry = None
    for dsm_geometry in dsm.datastructure.geometries:
        if dsm_geometry.Id == geometry_id:
            geometry = dsm_geometry
            break

    if geometry is None:
        raise ValueError(f"Model error, geometry_id {geometry_id} is not defined in {filename}")

    # get the connection between the soillayers and the geometry
    soillayers = None        
    try:
        for dsm_soillayer in dsm.datastructure.soillayers:
            if dsm_soillayer.Id == soillayer_collection_id:
                soillayers = {s.LayerId:dsmsoils[s.SoilId] for s in dsm_soillayer.SoilLayers}
                break
    except Exception as e:
        raise ValueError(f"Model error, invalid soil-layer connections found in {filename}")

    if soillayers is None:
        raise ValueError(f"Model error, soillayers_id {soillayer_collection_id} is not defined in {filename}")

    for layer in geometry.Layers:
        cm.soilpolygons.append(CMSoilPolygon.from_dsm(layer, soillayers))

    # get the crosssection (surface layer)
    # first convert the polygons to a list of shapely polygons
    polygons = [points_to_shapely_polygon(spg.polygon) for spg in cm.soilpolygons]

    # next get the surface out of the polygons
    # so this is a nasty step.. how to get the surface from a bunch of polygons
    # this took me some time to figure out.. in the end it was easy.. as it always is ;-)
    surface = polygons_to_surface(polygons) 

    # add as a crosssection
    # note that I have to make assumptions.. the user should be aware of that
    # so document your API
    # ASSUMPTION! the point with x=0.0 (if available) is the REFERENCE POINT
    points = []
    for p in surface:
        if p[0] == 0.0:
            points.append(Point3D(x=p[0], y=0.0, z=p[1], l=p[0], type=PointType.REFERENCEPOINT))
        else:
            points.append(Point3D(x=p[0], y=0.0, z=p[1], l=p[0], type=PointType.NONE))

    cm.crosssection = Crosssection(
        source = 'from stix',
        points = points,
    )


    # get phreaticline
    waternet = None
    for dsm_waternet in dsm.waternets:
        if dsm_waternet.Id == waternet_id:
            waternet = dsm_waternet
            break

    if waternet is None:
        raise ValueError(f"Model error, waternet_id {waternet_id} is not defined in {filename}")


    if waternet.has_head_line_id(waternet.PhreaticLineId):
        cm.phreaticline = [Point2D(x=p.X, z=p.Z) for p in waternet.get_head_line(waternet.PhreaticLineId).Points]


    # get acquiferline
    # TODO > find a way to retrieve the acquiferline if possible
    # this will be hard.. unless I assume that the user uses a predifined number of headlines..
    # not so sure about this one right now

    # get dstability_bishopbruteforce_settings or dstability_spencer_genetic_analysis_settings
    # these are optional so don't freak out if it is not there
    calculation_settings = None
    for dsm_calculation_settings in dsm.datastructure.calculationsettings:
        if dsm_calculation_settings.Id == calculation_settings_id:
            calculation_settings = dsm_calculation_settings
            break

    if dsm_calculation_settings is not None:
        if dsm_calculation_settings.AnalysisType == AnalysisTypeEnum.BISHOP_BRUTE_FORCE:
            cm.dstability_bishopbruteforce_settings = DStabilityBishopBruteForceSettings.from_dsm(dsm_calculation_settings.BishopBruteForce)
        elif dsm_calculation_settings.AnalysisType == AnalysisTypeEnum.SPENCER_GENETIC:
            cm.dstability_spencer_genetic_analysis_settings = DStabilitySpencerGeneticSettings.from_dsm(dsm_calculation_settings.BishopBruteForce)

    # get dstability_traffic_load
    loads = None
    for dsm_loads in dsm.datastructure.loads:
        if dsm_loads.Id == loads_id:
            loads = dsm_loads
            break

    if loads is not None:
        # ASSUMPTION! assume the first uniform load is the traffic load
        # ASSUMPTION! assume the consolidation percentage = 0 (for cohesive soils), MLAS does not take a consolidation coeff per layer into account
        for load in loads.UniformLoads:
            cm.dstability_traffic_load = DStabilityUniformLoad.from_dsm(load)
            break

    # we are done.. now we can do nifty things using our own library..
    return cm
```

Just to show that it works; here is the input

![the output](https://github.com/breinbaas/breinbaas.github.io/blob/master/img/04.01.jpg?raw=true)

And here is the output as plotted by my library (yep, it uses random colors since it is not possible to find the Deltares colors)

![the output](https://github.com/breinbaas/breinbaas.github.io/blob/master/img/04.02.jpg?raw=true)

### Next

So what's next.. now it is easy to use already created calculations and apply all the functionality in my library like automatically adding ditches, optimizing the embankement etc etc and export it back to DSeries or auto calculate it. And the nice thing is that I can also create output options to other software like Plaxis. So using my own ```CalculationModel``` might not be the easiest way but it is a very rewarding and powerful way.

Cheers,
Rob
