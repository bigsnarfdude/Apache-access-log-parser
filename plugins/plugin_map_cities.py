import pygmaps 

# DESC:         initialize a map  with latitude and longitude of center point  
mymap = pygmaps.maps(37.428, -122.145, 16)

# DESC:         set grids on map  
mymap.setgrids(37.42, 37.43, 0.001, -122.15, -122.14, 0.001)

# DESC:         add a point into a map and dispaly it, color is optional default is red
mymap.addpoint(37.427, -122.145, "#0000FF")

# DESC:         add a point with a radius (Meter) - Draw cycle
mymap.addradpoint(37.429, -122.145, 95, "#FF0000")

# DESC:         add a path into map, the data struceture of Path is a list of points
path = [(37.429, -122.145),(37.428, -122.145),(37.427, -122.145),(37.427, -122.146),(37.427, -122.146)]
mymap.addpath(path,"#00FF00")

# DESC:         create the html map file (.html)
mymap.draw('./mymap.html')

