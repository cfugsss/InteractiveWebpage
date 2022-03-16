import folium
import pandas

# initalizing volcanoes data using pandas

volcsData = pandas.read_csv("volcanoes.txt")
volcsLat = list(volcsData["LAT"])
volcsLon = list(volcsData["LON"])
volcsDesc = list(volcsData["NAME"])
volcsElev = list(volcsData["ELEV"])

# Creating map object holding the start position for web page

map = folium.Map(location=[40.47, -98.95], zoom_start=5, tiles="cartodbpositron")

# creating feature group for volcanoes and adding function to get the color depending on elevation of volcano

fgv = folium.FeatureGroup(name="Volcanoes")

def volcsColor(x):
    if x <= 1500:
        return("green")
    elif 1500 < x <= 3250:
        return("orange")
    else:
        return("red")

# iterating through each volcano to place a marker on the map

for lat, lon, desc, elev in zip(volcsLat, volcsLon, volcsDesc, volcsElev):
    fgv.add_child(folium.CircleMarker(
        location = [lat, lon],
        radius = 6,
        popup = desc,
        color = volcsColor(elev),
        fill = True
    ))

# creating a new feature group for the geojson polygon | Also fills each polygon with a different color depending on population

fgp = folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data=(open("world.json", "r", encoding="utf-8-sig").read()), 
style_function=lambda x: {"fillColor":"green" if x["properties"]["POP2005"] < 25000000 else "orange" if 25000000 <= x["properties"]["POP2005"] <  75000000 else "red"}))

# adding each group to the map object (web page) and adding layer control the page so we can turn each group on or off

map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())

map.save("map1.html")



