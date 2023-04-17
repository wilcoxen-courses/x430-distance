# Example: GIS Distance Operations

## Summary

The **demo.py** file in this repository builds several GIS layers that can be used with QGIS in distance-based calculations such as building Voronoi polygons or computing the shortest line between features.

## Input Data

There are two input files: **demo.gpkg**, which has a number of Census layers related to Syracuse and Onondaga County, and **Retail_Food_Stores.csv**, which is a list of all retail food stores licensed by the NYS Department of Agriculture and Markets. The original database can be found here:  <https://data.ny.gov/Economic-Development/Retail-Food-Stores/9a8c-vfzj>.

## Deliverables

**None**. This is an example only and there's **nothing due**.

## Instructions

1. Run demo.py

1. Load `demo-output.gpkg` into QGIS

1. Build Voronoi polygons around the stores. The Voronoi tool is under `Vector` > `Geometry Tools`. Choose the stores as the input layer and set the buffer region to 100%. Then clip the Voronoi layer at the county boundary, remove the unclipped Voronoi layer, and move the store layer to the top to see the overall result.

1. Add lines showing the shortest distance between each tract centroid and the nearest store. The `Shortest line between features` tool is available from the top menu via the `Processing` > `Toolbox` (gear icon) under the `Vector analysis` heading. Use the tract centroids as the source layer and the stores as the destination layer. After the lines are built, move the centroid layer above the clipped Voronoi layer to see the overall result.

## Tips

* These layers could be exported for further analysis in a script. For example, the Voronoi layer could be used to find the population served by a given store, and the shortest line layer could be use to quickly compute an average distance people have to travel to their nearest store.
