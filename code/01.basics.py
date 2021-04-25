from geolib.models.dstability import DStabilityModel
from geolib.soils import Soil
from geolib.geometry.one import Point
from geolib.models.dstability.loads import UniformLoad
from geolib.models.dstability.analysis import DStabilityBishopAnalysisMethod, DStabilityCircle

from pathlib import Path

dm = DStabilityModel()
bishop_analysis_method = DStabilityBishopAnalysisMethod(
    circle=DStabilityCircle(center=Point(x=20, z=3), radius=15)
)
dm.set_model(bishop_analysis_method)

soil = Soil()
soil.name = "Soil test"
soil.code = "HV"
soil.soil_weight_parameters.saturated_weight.mean = 10.2
soil.soil_weight_parameters.unsaturated_weight.mean = 10.2
soil.mohr_coulomb_parameters.cohesion.mean = 0.5
soil.mohr_coulomb_parameters.friction_angle.mean = 15.0      
soil_peat_id = dm.add_soil(soil)

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

layer_ids = []
for layer, soil in layers_and_soils:
    layer_id = dm.add_layer(layer, soil)
    layer_ids.append(layer_id)

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

dm.add_load(
    UniformLoad(
        label="trafficload",
        start=6.5,
        end=9.0,
        magnitude=13,
        angle_of_distribution=45,
    )
)

dm.serialize(Path("tutorial.stix"))
dm.execute()