from geolib.models.dstability import DStabilityModel
from geolib.geometry.one import Point

from pathlib import Path

dm = DStabilityModel()

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
    Point(x=30, z=-5), # we need to add this point!
    Point(x=30, z=-3),
    Point(x=50, z=-3),
    Point(x=50, z=-7),
]
layers_and_soils = [
    (layer_1, "Sand"),
    (layer_2, "H_Ro_z&k"),
    (layer_3, "H_Aa_ht_old")
]

layer_ids = []
for layer, soil in layers_and_soils:
    layer_id = dm.add_layer(layer, soil)
    layer_ids.append(layer_id)

dm.serialize(Path("geometry.stix"))
