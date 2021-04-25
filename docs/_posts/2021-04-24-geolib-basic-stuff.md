---
layout: post
title:  "Geolib - Most basic example"
date:   2021-04-24 18:48:49 +0200
categories: python geolib
---

### Whoami

Rob van Putten, breinbaasnl@gmail.com, geotechnical engineer / developer / creative thinker 

### Geolib series

After waiting for about half a year after working on the geolib code with some great developers I finally got time to work **with** the library. So I decided to start a series of tutorials on how to use this amazing library. For those who don't know about geolib, it is actually an API over the Deltares geotechnical software called [the DSeries](https://www.deltares.nl/en/). To be complete, it is an interface over the following parts of the DSeries;

* [DFoundations](https://www.deltares.nl/en/software/d-foundation-2/) software for foundation design
* [DSheetPiling](https://www.deltares.nl/en/software/d-sheet-piling-2/) software for sheetpile calculations
* [DSettlement](https://www.deltares.nl/en/software/d-settlement-2/) software for settlement calculations
* [DStability](https://www.deltares.nl/nl/software/d-stability-nl/)

DStability is a bit of the odd one out since it is based on a new design approach. The input is based on a large collection of json files whereas the other software is based on an text file based input / output system. DStability is also the only one free to use. Finally, DStability is what I use most for work so the tutorial series might be focused on DStability for now.. also because I do not have commercial licenses for the other ones.

With geolib you will be able to use Python to generate input and read output of all the mentioned software so theoretically you will not need to push any button on a GUI anymore. This opens up a lot of possibilities for automation of calculations which is exactly my cup of tea. 

So let's start!

**note** I am writing these tutorials because I like to spend time on automation in engineering. If you want to support my work feel free to reach out. I teach Python to engineers and have done this succesfully for hundreds of engineers. There is no better way to learn coding then getting your feet wet with an experienced and passionate teacher :-)

breinbaasnl@gmail.com

**note** This series of tutorials is not connected to any of the other developers or Deltares in any way. It is my interpretation of geolib and how to work with it.

### The basics

Let's get started by just using (part of) the code provided by the documentation.

I will walk you through these steps with just a little more information;

```python
from geolib.models.dstability import DStabilityModel
from geolib.soils import Soil
from geolib.geometry.one import Point
from geolib.models.dstability.loads import UniformLoad
from geolib.models.dstability.analysis import DStabilityBishopAnalysisMethod, DStabilityCircle
from pathlib import Path
```

If you have installed geolib (and hopefully using a virtual environment) you will need to know which modules you have to import. Geolib uses a intuitive way to guide you to the modules. Modules that have objects that are shared over all models can be found in the geolib.soils and geolib.geometry modules. Model specific objects can be found in the geolib.models modules. For example, a uniform load is different for DSettlement and DStability because of the implementation in the calculation software. If you want to use the UniformLoad for DSettlement you will have to write;

```python
from geolib.models.dsettlement.loads import UniformLoad
```

But for using DStability you will need;

```python
from geolib.models.dstability.loads import UniformLoad
```

If you are using a modern IDE like [VSCode](https://code.visualstudio.com) you will probably have autocompletion which will make it easier to find the right module. And of course, there is always the documentation!

Ok, let's initialize the model;

```python
dm = DStabilityModel()
bishop_analysis_method = DStabilityBishopAnalysisMethod(
    circle=DStabilityCircle(center=Point(x=20, z=3), radius=15)
)
dm.set_model(bishop_analysis_method)
```

A thing to take away from this code is that geolib is using [pydantic](https://pydantic-docs.helpmanual.io). I learnt to use pydantic during development of geolib and it is a huge improvement over 'normal' Python code. I won't be dealing with pydantic in these tutorials but just look at this example;

```python
# old code
class Car:
    def __init__(self):
        self.wheels = 4 
        self.color = 'red'

# pydantic code
from pydantic import BaseModel
class Car(BaseModel):
    wheels: int = 4
    color: str = 'red'
```

If that doesn't make you feel good I don't know what will ;-) Be sure to learn more about pydantic even if you didn't feel anything at all!

Now let's continue with the documentation / tutorial;

```python
soil = Soil()
soil.name = "Soil test"
soil.code = "HV"
soil.soil_weight_parameters.saturated_weight.mean = 10.2
soil.soil_weight_parameters.unsaturated_weight.mean = 10.2
soil.mohr_coulomb_parameters.cohesion.mean = 0.5
soil.mohr_coulomb_parameters.friction_angle.mean = 15.0      
soil_peat_id = dm.add_soil(soil)
```

Easy isn't it? Simply define a soiltype by using the Soil class. You can also do it like this (I like that better);

```python
soil_peat_id = dm.add_soil(
    Soil(
        name = "Soil test",
        code = "HV",
        soil_weight_parameters.saturated_weight.mean = 10.2,
        soil_weight_parameters.unsaturated_weight.mean = 10.2,
        mohr_coulomb_parameters.cohesion.mean = 0.5,
        mohr_coulomb_parameters.friction_angle.mean = 15.0
    )
)
```

Nice.. and this should open your eyes and make you think about putting all your soiltypes in a database so you can easily import these soils from your database.. I did!

Next up, creating the layers;

```python
layer_1 = [
    Point(x=-50, z=-10),
    Point(x=50, z=-10),
    Point(x=50, z=-20),
    Point(x=-50, z=-20),
]
layer_2 = [
    Point(x=-50, z=-5),
    Point(x=50, z=-5),
    Point(x=50, z=-10),
    Point(x=-50, z=-10),
]
layer_3 = [
    Point(x=-50, z=0),
    Point(x=-10, z=0),
    Point(x=30, z=0),
    Point(x=50, z=0),
    Point(x=50, z=-5),
    Point(x=-50, z=-5),
]
embankment = [
    Point(x=-10, z=0),
    Point(x=0, z=2),
    Point(x=10, z=2),
    Point(x=30, z=0),
]
layers_and_soils = [
    (layer_1, "Sand"),
    (layer_2, "H_Ro_z&k"),
    (layer_3, "HV"),
    (embankment, "H_Aa_ht_old"),
]
```

Note that geolib uses x for the position and z for the depth. In the previous versions of the DSeries this was defined as x and y but I think x, z is much better. X and y can now be like a 2D point on a surface where z acts as the depth value. 

The logic of building layers makes sense. It is simply a collection of Point classes. 

Also note that DGeo Suite Stability comes with predefined soil types. You can find them if you open up the software and look add the apply material option;

![predefined soils](https://github.com/breinbaas/breinbaas.github.io/blob/master/img/01.01.jpg?raw=true)

That's the reason why you find those names in the layers_and_soils list.

So now we have the layers, let's add them to the model.

```python
layer_ids = []
for layer, soil in layers_and_soils:
    layer_id = dm.add_layer(layer, soil)
    layer_ids.append(layer_id)
```

This is straightforward isn't it? Now there is a catch which I will deal with in later tutorials.. you can create the most beautiful and complicated geometries but this does not mean that the geometry is valid! I think this is the most important update that geolib needs but it is not implemented right now. So be careful with how you build up your geometry or strange things can happen. I will come back to that in a later tutorial.

For now, we are happy with the geometry and we will add the water lines;

```python
phreatic_line_id = dm.add_head_line(
    points=[
        Point(x=-50, z=1.0),
        Point(x=0, z=1),
        Point(x=30, z=-1),
        Point(x=50, z=-1),
    ],
    label="Phreatic Line",
    is_phreatic_line=True,
)

sand_head_line_id = dm.add_head_line(
    points=[Point(x=-50, z=5.0), Point(x=50, z=5.0)],
    label="Hydraulic head in sandlayer",
)

dm.add_reference_line(
    points=[Point(x=-50, z=-3), Point(x=50, z=-3)],
    bottom_headline_id=phreatic_line_id,
    top_head_line_id=phreatic_line_id,
)
dm.add_reference_line(
    points=[Point(x=-50, z=-10), Point(x=50, z=-10)],
    bottom_headline_id=sand_head_line_id,
    top_head_line_id=sand_head_line_id,
)
```

For now, simply accept what is happening. Adding waterlines is a bit complex but the process of adding it using Python is really simple. Older DSeries users probably will remember the 1 99 2 etc way of working but that has changed and again this will be subject for another tutorial. 

Let's add the load;

```python
dm.add_load(
    UniformLoad(
        label="trafficload",
        start=6.5,
        end=9.0,
        magnitude=13,
        angle_of_distribution=45,
    )
)
```

Again, really easy. Just make sure to use the right type of UniformLoad (so not the DSettlement one).

The final step is to write the input file and (if you have the console versions installed) execute the file.

```python
dm.serialize(Path("tutorial.stix"))
dm.execute()
```

One thing to note is that geolib is using [pathlib](https://docs.python.org/3/library/pathlib.html) instead of the old 'os' and related modules. This might lead to errors if you are still used to file handling using the older modules. Be sure to learn about pathlib (Python 3.6+) because it is so much better. Here's a simple example but checkout articles like [this one](https://treyhunner.com/2018/12/why-you-should-be-using-pathlib/);

```python
PATH = "c:/bla/bla"
FILE = "somefile.txt"

#old
filename = os.path.join(PATH, FILE)

#using pathlib
filename = Path(PATH) / FILE
```

So there we are. We just stepped through the documentation example for DGeoStability and created a valid input file which we can open in the software or calculate using the console option. I hope this inspires you to think about all the stuff that you can do right now. 

![the output](https://github.com/breinbaas/breinbaas.github.io/blob/master/img/01.02.jpg?raw=true)

See you in the next tutorial!

the code for this part can be found [here](https://github.com/breinbaas/breinbaas.github.io/blob/master/code/01.basics.py?raw=true)

