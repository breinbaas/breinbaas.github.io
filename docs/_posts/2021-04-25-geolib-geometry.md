---
layout: post
title:  "Geolib - Geometry"
date:   2021-04-24 18:48:49 +0200
categories: python geolib
---

### tutorial in development!

### Geolib series

In my previous tutorial I told you about errors that you might introduce in the geometry. This tutorial will elaborate on this.

So let's start!

**note** I am writing these tutorials because I like to spend time on automation in engineering. If you want to support my work feel free to reach out. I teach Python to engineers and have done this succesfully for hundreds of engineers. There is no better way to learn coding then getting your feet wet with an experienced and passionate teacher :-)

breinbaasnl@gmail.com

### Geometry problem

Building up geometries from code is easy. Here's a short snippet of building up some layers as seen in the documentation;

```python
# define some layers
layer_1 = [
    Point(x=-50, z=-10),
    Point(x=50, z=-10),
    Point(x=50, z=-20),
    Point(x=-50, z=-20),
]

...

layers_and_soils = [
    (layer_1, "Sand"),
    (layer_2, "H_Ro_z&k"),
    (layer_3, "HV"),
    (embankment, "H_Aa_ht_old"),
]

# add layers to the model
for layer, soil in layers_and_soils:
    dm.add_layer(layer, soil)
```

But problems will come up with a geometry like this;

![geometry problem](https://github.com/breinbaas/breinbaas.github.io/blob/master/img/02.01.png?raw=true)

You might be tempted to write code like;

```
layer_1 = [
    Point(x=0, z=-5),
    Point(x=0, z=0),
    Point(x=30, z=0),
    Point(x=30, z=-5),
]
layer_2 = [
    Point(x=0, z=-7),
    Point(x=0, z=-5),
    Point(x=30, z=-5),
    Point(x=30, z=-7),
]
layer_3 = [
    Point(x=30, z=-7),
    Point(x=30, z=-3),
    Point(x=50, z=-3),
    Point(x=50, z=-7),
]
```

But unfortunately this will not work and you will not be warned because this is what it will look like if you open the generated file in DGeoStability;

![no problem](https://github.com/breinbaas/breinbaas.github.io/blob/master/img/02.02.jpg?raw=true)

Looks fine to me!

But it is not. Eventhough the geometry is off course nothing you expect to see in real life it is possible to tell DStab (let's abbreviate it for the sake of my fingers) to calculate the stability factor and this is what might happen;

![a problem](https://github.com/breinbaas/breinbaas.github.io/blob/master/img/02.03.jpg?raw=true)

The critical slip circle simply stops at the boundary between layer_2 and layer_3. 

The solution is simple, **add all points that are part of the outer polyline of the layer** which in this case means that you will have to add point x=30, z=-5 to layer 3!

```python
layer_3 = [
    Point(x=30, z=-7),
    Point(x=30, z=-5),
    Point(x=30, z=-3),    
    Point(x=50, z=-3),    
    Point(x=50, z=-7),
]
```

There we go.. much better!

![nope, no problem](https://github.com/breinbaas/breinbaas.github.io/blob/master/img/02.03.jpg?raw=true)

Now I do think that fixing broken geometries should actually be part of the geolib logic but it is complicated to fix whatever users might come up with. For now be aware of this problem because it will cause you headaches due to the fact that the geometry is fine in the software until you start your analysis and you see funny slope circles! 

#### todo > write some code for a solution

See you in the next tutorial!

the code for this part can be found [here](https://github.com/breinbaas/breinbaas.github.io/blob/master/code/02.geometry.py?raw=true)

