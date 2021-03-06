---
layout: post
title:  "Geolib - Geometry"
date:   2021-04-25 13:53:00 +0200
categories: python geolib
---

### Geolib series

In my [previous tutorial](https://breinbaas.github.io/python/geolib/2021/04/24/geolib-basic-stuff.html) I told you about errors that you might introduce in the geometry. This tutorial will elaborate on this.

So let's start!

**note** I am writing these tutorials because I like to spend time on automation in engineering. If you want to support my work feel free to reach out. I teach Python to engineers and have done this succesfully for hundreds of engineers. There is no better way to learn coding then getting your feet wet with an experienced and passionate teacher :-)

breinbaasnl@gmail.com

### Geometry problem

**update 2021-04-26** It seems that the geometry problem will be handled in later versions of geolib so be sure to follow the geolib news!

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
You simply add the bottomleft, topleft, topright and bottomright points. But unfortunately this will not work and you will not be warned because this is what it will look like if you open the generated file in DGeoStability;

![no problem](https://github.com/breinbaas/breinbaas.github.io/blob/master/img/02.02.jpg?raw=true)

Looks fine to me!

But it is not. Eventhough the geometry is off course nothing you expect to see in real life it is possible to tell DStab (let's abbreviate it for the sake of my fingers) to calculate the stability factor and this is what might happen;

![a problem](https://github.com/breinbaas/breinbaas.github.io/blob/master/img/02.03.jpg?raw=true)

The critical slip circle simply stops at the boundary between layer_2 and layer_3. 

The solution is simple, **add all intersecting points to the layer** which in this case means that you will have to add point x=30, z=-5 to layer 3 because it is intersecting with the layer!

![geometry problem](https://github.com/breinbaas/breinbaas.github.io/blob/master/img/02.06.png?raw=true)

```python
layer_3 = [
    Point(x=30, z=-7),
    Point(x=30, z=-5), # you need to add this point!
    Point(x=30, z=-3),     
    Point(x=50, z=-3),    
    Point(x=50, z=-7),
]
```

The same applies to the intersection with layer_1

![geometry problem](https://github.com/breinbaas/breinbaas.github.io/blob/master/img/02.07.png?raw=true)

```python
layer_1 = [
    Point(x=0, z=-5),
    Point(x=0, z=0),    
    Point(x=30, z=0),
    Point(x=30, z=-3), # another intersection
    Point(x=30, z=-5),
]
```

There we go.. much better!

![nope, no problem](https://github.com/breinbaas/breinbaas.github.io/blob/master/img/02.04.jpg?raw=true)

Now I do think that fixing broken geometries should actually be part of the geolib logic but it is complicated to fix whatever users might come up with. For now be aware of this problem because it will cause you headaches due to the fact that the geometry is fine in the software until you start your analysis and you see funny slope circles! 

### A simple solution

For geometries where the layers are either between coordinates xleft, xmid or xmid and xright (like in the next image) there is a rather easy solution.

![this is easy to fix](https://github.com/breinbaas/breinbaas.github.io/blob/master/img/02.05.png?raw=true)

Let's say you have layers like this;


```python
layers_left = [
    (0, -5, 'layer_1'),
    (-5, -7, 'layer_2')
]

layers_right = [
    (-3, -7, 'layer_3')
]
```

So a layer is a tuple of (z_top, z_bottom, layer- or soilname). Now simply combine the z coordinates to one list.

```python
z_combined = sorted(list(set(chain(*[[l[0], l[1]] for l in layers_left + layers_right]))), reverse=True)
```

Let's break down that line for those unfamiliar with what is happening.

```python
z_combined = layers_left + layers_right
```

is a way to combine two lists so we add all elements from layers_left and layers_right

```python
[[l[0], l[1]] for l in layers_left + layers_right]
```

will create a list with both z coordinates of the layer like [[z1, z2], [z3, z4]...]

```python
chain(*[[l[0], l[1]] ...
```

will create a chain of elements like [z1, z2, z3, z4 ...]

```python
list(set(...))
```

will make sure that we have a list with unique elements only and

```python
sorted(..., reverse=True)
```

will make sure that our z values increase in depth 

So a lot is happening in that line (and don't forget to import chain from itertools!) but in essence it selects all the possible z values and combines them in one list ordered from top to bottom. 

Next you can use that list to select points within the top and bottom coordinate of that layer, like so;

```python
z_extras = [z for z in z_combined if z < layer[0] and z > layer[1]]
```

By the way, if you're not familair with [list comprehension](https://www.datacamp.com/community/tutorials/python-list-comprehension) in Python.. now is the time!

Now you are ready to add these coordinates to your layer and this way you can be sure that the intersecting points will be added (in this case you might even get some extra points but that doesn't hurt). 

The complete code as a function is here;

```python
from itertools import chain

def combine_layers(layers_left, layers_right, xleft, xmid, xright):
    result = []
    z_combined = sorted(list(set(chain(*[[l[0], l[1]] for l in layers_left + layers_right]))), reverse=True)

    for layer in layers_left:
        coords = []
        coords.append((xleft, layer[1])) # bottomleft
        coords.append((xleft, layer[0])) # topleft
        coords.append((xmid, layer[0])) # topright
        
        z_extras = [z for z in z_combined if z < layer[0] and z > layer[1]]
        for z in z_extras:
            coords.append((xmid, z))

        coords.append((xmid, layer[1])) # bottomright    
        result.append((layer[2], coords))    

    for layer in layers_right:
        coords = []
        coords.append((xmid, layer[1])) # bottomleft

        z_extras = [z for z in z_combined if z < layer[0] and z > layer[1]]
        for z in reversed(z_extras):
            coords.append((xmid, z))

        coords.append((xmid, layer[0])) # topleft
        coords.append((xright, layer[0])) # topright
        coords.append((xright, layer[1])) # bottomright
        result.append((layer[2], coords))    

    return result
```

This will however not work for more complicated geometries. If you happen to get to that point it would be a nice idea to dive into libraries that can handle polygon intersections. 

### Wrap up

Be careful with geometries because they might look ok in the software but they might break during analysis. I've shown you one way to come up with a valid geometry but feel free to develop and share your own! Have fun and see you in the next tutorial!

the code for this part can be found [here](https://raw.githubusercontent.com/breinbaas/breinbaas.github.io/master/code/02.geometry.py)

