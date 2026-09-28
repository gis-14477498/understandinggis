from geopandas import read_file

world = read_file("../../data/natural-earth/ne_50m_admin_0_countries.shp")

print(world.head())
from matplotlib.pyplot import subplots, savefig
# create map axis object
my_fig, my_ax = subplots(1, 1, figsize=(16, 10))

# plot the countries onto ax
world.plot(ax = my_ax)

# save the result
savefig('./out/1.png')
print("done!")