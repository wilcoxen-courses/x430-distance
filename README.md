# Example: GIS Distance Operations

## Summary

The **demo.py** file in this repository builds several GIS layers that can be used with QGIS in distance-based calculations such as building Voronoi polygons or computing the shortest line between features.

## Input Data

There are two input files: **demo.gpkg**, which has a number of Census layers related to Syracuse and Onondaga County, and **Retail_Food_Stores.csv**, which is a list of all retail food stores licensed by the NYS Department of Agriculture and Markets. The original database can be found here:  <https://data.ny.gov/Economic-Development/Retail-Food-Stores/9a8c-vfzj>.

## Deliverables

None. This is an example only and there's nothing due.

## Instructions

1. Run demo.py

1. Load `demo-output.gpkg` into QGIS

1. Try building Voronoi polygons. The Voronoi tool is under `Vector` > `Geometry Tools`.

1. Try computing the shortest distance between each tract centroid and the nearest store. The shortest line tool is available in the `Processing` > `Toolbox` (gear icon) under the `Vector analysis` heading. Use the tract centroids as the source layer and the stores as the destination layer.
