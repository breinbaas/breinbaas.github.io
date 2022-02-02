---
layout: post
title:  "Geolib - Hacking geolib"
date:   2022-02-02 19:48:49 +0200
categories: python geolib
---

### Geolib hacking

Now this might be the most useless code you will ever read but I found it useful so maybe someone else does as well :-) Anyway, thanks to Almar Joling for coming up with the idea!

So what's that idea? Almar has a great Unity / web based 3D visualization tool for Deltares stix files (geotechnical slope stability software files) and I have a method to automatically generate these stix files based on CPT's / crosssections and some more data. So we thought.. let's try to find a way to upload a lot of stix files so Almar's tool can render a nice 3D model. 

The problem we found was that we needed some way to find the location of a fixed point on the model to geo reference the location. We came up with some ideas like adding a geojson file with a reference to the file and containing the fixed point which then should be added to the uploaded stix files. I thought about including the latitude and longitude in the filename leading to filenames like; P1004_0075_52.25179556_4.90886070.stix .. brrr.. 

Then Almar said.. 'why not add the information in the stix file'.. readers of my previous posts might know that a stix file is in fact a bunch of json files zipped together. So this evening I did a test and indeed the software does not complain if you add another json file in the stix file.. 

The next step was to adjust geolib to implement a way to add the reference point and it proved to be easy. **Note, don't hack in the geolib code unless you don't mind that it won't work afterwards!**

The first thing to note is that the ```DStabilityStructure``` is the base of all properties of the calculation. The fields in this class are automatically serialized to json files with some clever parsing and pydantic usage. Adding a new field is easy..

```python
class DStabilityStructure(BaseModelStructure):
    ...
    reference_point: ReferencePoint = ReferencePoint()
    ...   
```

And off course it is easy to create that new model;

```python
class ReferencePoint(DStabilitySubStructure):
    """referencepoint.json"""
    Latitude: float = 0.0
    Longitude: float = 0.0

    @classmethod
    def structure_name(cls) -> str:
        return "referencepoint"
```

Note that you use camelcase for the properties because that is how the json file is structured in a stix file. 

The only thing left to do is make this available to the user of geolib, in ```DStabilityModel``` I added the following simple function;

```python
def set_reference_point(self, latitude: float, longitude: float):
    self.datastructure.reference_point = ReferencePoint(Latitude = latitude, Longitude = longitude)
```

And this is enough.. using the ```serialize``` function from ```DStabilityModel``` now gives us an extra file in the stix file named ```referencepoint.json```

![stix files](https://github.com/breinbaas/breinbaas.github.io/blob/master/img/06.01.png?raw=true)

Now my own code (called MLAS which stands for Modular Levee Assessment System) uses this field because MLAS creates ```CalculationModel``` classes which contain a crosssection and a crosssection contains a referencepoint in RD (EPSG:28992) space. To make it more generic I convert those coordinates to WGS84 (EPSG:4326) and store it in the calculation model before I serialize it to a stix file.

```python
try:
    refpoint = self.crosssection.reference_point
    proj = pyproj.Transformer.from_crs(28992, 4326, always_xy=True)
    lon, lat = proj.transform(refpoint.x, refpoint.y)
    dstability_model.set_reference_point(lat, lon)
except:
    pass // it defaults to 0.0, 0.0 which is fine 

return dstability_model
```

So now all the files that I generate using MLAS have a referencepoint.json file in the stix file with info like;

```
{
    "Latitude": 52.25145038374522,
    "Longitude": 4.909093887325246
}
```

And now any software parsing the stix file will also have access to that file.. which means that Almar can simply expect a user to upload a stix file and find the location in the provided file.. not only that, I can use this in MLAS and GIS software to easily find the location of the calculation which is a nice feature (hey Deltares, maybe something to add to the official software? ;-)

So is this really helpful? Yes, for me it is because it is a much nicer way to store the location of the stix file then writing silly filenames.. No, because it means I have 'hacked' the stix file and if Deltares ever decides to check for json files that should not be there I am in trouble (not really because I can revert the code ;-). Another problem that I introduced is that now geolib does not parse stix files without the referencepoint because 'normal' stix files have no referencepoint.json which means that I have to hack a little more to make sure that this file is optional. But hey, there is a solution for everything in Python land...

So that's it.. hacking is fun and can be a great way to add functionality but you have to be aware of the risks.. but still.. it is more fun than risky for me ;-)

Have fun,
Rob


