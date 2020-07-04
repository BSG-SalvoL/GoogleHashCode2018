from Google_Hash_Code_2018.imports.LoadFile import loadinput
from Google_Hash_Code_2018.imports.OutputFile import create_output, output_file
from Google_Hash_Code_2018.imports.Mappa import Map

mapline, ridelines = loadinput()
mymap = Map(mapline)
print("Loaded Rides: " + str(mymap.load_rides(ridelines)))
mymap.loop()
output_file(create_output(mymap.__getattribute__("cars")))




