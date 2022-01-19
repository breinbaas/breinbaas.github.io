---
layout: post
title:  "QGis - Code snippets"
date:   2022-01-29 18:48:49 +0200
categories: python qgis
---

## This will be the place for me to write down some interesting QGis plugin dev code snippets.

* Get layers from project 
```python
layers = QgsProject.instance().mapLayersByName(routes_layer_name)
```

* Select a feature and zoom selected
```python
expr = f'"myField"=\'myFieldIdentifier\'' # note that " means field and ' means value
layer.selectByExpression(expr)
box = layer.boundingBoxOfSelected()
self.iface.mapCanvas().setExtent(box)
self.iface.mapCanvas().refresh()
```

* Get fields from layer 
```python
layer = QgsProject.instance().mapLayersByName(routes_layer_name)[0]
prov = layer.dataProvider()
field_names = [field.name() for field in prov.fields()]
```
* Set active layer
```python
qgis.utils.iface.setActiveLayer(QgsMapLayer)
```

### Recompile resources
```pyrcc5 -o resources.py resources.qrc```

### Create a layer with a renderer

```python 
# this next code will get some objects from a database and determine their importance
# which will give a list of weights ranging from 0.0 to 1.0
crosssections = self.database.get_crosssections(self.project.levee_code)
weighted_crosssection = self._get_weighted_crosssections(crosssections)
weights = [w[0] for w in weighted_crosssection]
wmin = min(weights)
wmax = max(weights)

# create a new layer
layer = QgsVectorLayer("Point?crs=epsg:28992", f"{self.cbLeveeCode.currentText()}_crosssection_weights", "memory")

# create a provider to add attributes
provider = layer.dataProvider()
# I want to add the location of the object (crosssection) and the calculated weight
provider.addAttributes([
    QgsField("chainage", QVariant.Int),
    QgsField("weight",  QVariant.Double)
])
layer.updateFields() 

# now let's create the features
features = []
for w, crs in weighted_crosssection:
    pt = crs.get_point_at_l(20)
    p = (w - wmin) / (wmax - wmin) # yeah, should check for div0.. 
    f = QgsFeature()
    pxy = QgsPointXY(pt.x,pt.y) 
    f.setGeometry(QgsGeometry.fromPointXY(pxy))
    f.setAttributes([crs.levee_chainage, round(p,2)])
    features.append(f)

# done, now add them to the actual layer
provider.addFeatures(features)

# update the layer or the changes are not saved
layer.updateExtents()     

# now create a renderer which will choose a color based on the given field
# in my case I want some ranges around the lowest possible values since these are 
# important for my visualisation
graduated_renderer = QgsGraduatedSymbolRenderer()
graduated_renderer.addClassRange(QgsRendererRange(QgsClassificationRange('0.00 - 0.05', 0.00, 0.05), QgsMarkerSymbol.createSimple({'name': 'circle', 'color': '#ff0000'})))
graduated_renderer.addClassRange(QgsRendererRange(QgsClassificationRange('0.05 - 0.10', 0.05, 0.10), QgsMarkerSymbol.createSimple({'name': 'circle', 'color': '#ff4d00'})))
graduated_renderer.addClassRange(QgsRendererRange(QgsClassificationRange('0.10 - 0.15', 0.10, 0.15), QgsMarkerSymbol.createSimple({'name': 'circle', 'color': '#ff8400'})))
graduated_renderer.addClassRange(QgsRendererRange(QgsClassificationRange('0.15 - 0.20', 0.15, 0.20), QgsMarkerSymbol.createSimple({'name': 'circle', 'color': '#ffc800'})))
graduated_renderer.addClassRange(QgsRendererRange(QgsClassificationRange('0.20 - 0.30', 0.20, 0.30), QgsMarkerSymbol.createSimple({'name': 'circle', 'color': '#e5ff00'})))
graduated_renderer.addClassRange(QgsRendererRange(QgsClassificationRange('0.30 - 0.40', 0.30, 0.40), QgsMarkerSymbol.createSimple({'name': 'circle', 'color': '#bbff00'})))
graduated_renderer.addClassRange(QgsRendererRange(QgsClassificationRange('0.40 - 0.60', 0.40, 0.60), QgsMarkerSymbol.createSimple({'name': 'circle', 'color': '#80ff00'})))
graduated_renderer.addClassRange(QgsRendererRange(QgsClassificationRange('0.60 - 0.80', 0.60, 0.80), QgsMarkerSymbol.createSimple({'name': 'circle', 'color': '#33ff00'})))
graduated_renderer.addClassRange(QgsRendererRange(QgsClassificationRange('0.80 - 1.00', 0.80, 1.00), QgsMarkerSymbol.createSimple({'name': 'circle', 'color': '#02b005'})))

# be sure to connect the ranges to the right field
graduated_renderer.setClassAttribute('weight')

# there you go.. add it to the layer
layer.setRenderer(graduated_renderer)
# and add it to the project and we're done
QgsProject.instance().addMapLayer(layer)
```
