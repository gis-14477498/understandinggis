# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 01:33:10 2026

@author: 86391
"""


# ==========================================
# WEEK 5 - UNDERSTANDING DISTORTION
# ==========================================

# IMPORTS
from math import radians, sin, cos, hypot
from numpy.random import uniform
from numpy import arange
from geopandas import read_file
from pyproj import Geod, CRS, Transformer
from shapely.geometry import Polygon
from matplotlib.patches import Patch
from matplotlib.pyplot import subplots, savefig
from matplotlib_scalebar.scalebar import ScaleBar
from pathlib import Path


# ==========================================
# PART 1 - COMPUTE OFFSET
# ==========================================

def compute_offset(origin, distance, direction):
    """
    Compute the location of a point at a given
    distance and direction using trigonometry.
    """
    offset_x = origin[0] + cos(radians(direction)) * distance
    offset_y = origin[1] + sin(radians(direction)) * distance
    return (offset_x, offset_y)


# ==========================================
# PART 2 - EVALUATE DISTORTION
# ==========================================

def evaluate_distortion(
    g, transformer, minx, miny, maxx, maxy,
    minr, maxr, sample_number=1000, vertices=16
):

    # Calculate random locations and radii
    xs = uniform(low=minx, high=maxx, size=sample_number)
    ys = uniform(low=miny, high=maxy, size=sample_number)
    rs = uniform(low=minr, high=maxr, size=sample_number)

    # Calculate 16 directions
    forward_azimuths = arange(0, 360, 360 / vertices)

    # Create empty lists
    area_indices = []
    shape_indices = []
    distance_indices = []

    # --------------------------------------
    # AREA AND SHAPE DISTORTION
    # --------------------------------------

    for x, y, r in zip(xs, ys, rs):

        # Construct a circle on the ellipsoid
        lons, lats = g.fwd(
            [x] * vertices,
            [y] * vertices,
            forward_azimuths,
            [r] * vertices
        )[:2]

        # Project the ellipsoidal circle
        e_coords = [
            transformer.transform(
                lon, lat, direction="FORWARD"
            )
            for lon, lat in zip(lons, lats)
        ]

        # Calculate ellipsoidal circle area
        ellipsoidal_area = Polygon(e_coords).area

        # Transform the centre point
        centre_x, centre_y = transformer.transform(
            x, y, direction="FORWARD"
        )

        # Construct a circle on the projected plane
        planar_area = Polygon([
            compute_offset((centre_x, centre_y), r, az)
            for az in forward_azimuths
        ]).area

        # Calculate area distortion
        area_indices.append(
            abs(ellipsoidal_area - planar_area)
            / abs(ellipsoidal_area + planar_area)
        )

        # Calculate radial distances
        ellipsoidal_radial_distances = [
            hypot(centre_x - ex, centre_y - ey)
            for ex, ey in e_coords
        ]

        # Calculate shape distortion
        shape_distortion = [
            abs(
                (1 / vertices)
                - (d / sum(ellipsoidal_radial_distances))
            )
            for d in ellipsoidal_radial_distances
        ]

        shape_indices.append(sum(shape_distortion))

    # Calculate overall area and shape distortion
    Ea = sum(area_indices) / len(area_indices)
    Es = sum(shape_indices) / len(shape_indices)

    # --------------------------------------
    # DISTANCE DISTORTION
    # --------------------------------------

    for _ in range(sample_number):

        # Create two random locations
        xs = uniform(low=minx, high=maxx, size=2)
        ys = uniform(low=miny, high=maxy, size=2)

        # Calculate ellipsoidal distance
        ellipsoidal_distance = g.line_length(xs, ys)

        # Project both locations
        origin = transformer.transform(xs[0], ys[0])
        destination = transformer.transform(xs[1], ys[1])

        # Calculate planar distance
        planar_distance = hypot(
            destination[0] - origin[0],
            destination[1] - origin[1]
        )

        # Calculate distance distortion
        distance_indices.append(
            abs(ellipsoidal_distance - planar_distance)
            / abs(ellipsoidal_distance + planar_distance)
        )

    # Calculate overall distance distortion
    Ep = sum(distance_indices) / len(distance_indices)

    # Return the three distortion measures
    return Ep, Es, Ea


# ==========================================
# MAKE MAP BOUNDS SQUARE
# ==========================================

def make_bounds_square(ax):
    """
    Adjust the bounds of the axis to make a square.
    """

    # Get the current bounds
    ax_bounds_x = ax.get_xlim()
    ax_bounds_y = ax.get_ylim()

    # Get width and height
    ax_width = ax_bounds_x[1] - ax_bounds_x[0]
    ax_height = ax_bounds_y[1] - ax_bounds_y[0]

    # Expand height if width is larger
    if ax_width > ax_height:
        buffer = (ax_width - ax_height) / 2
        ax.set_ylim(
            (ax_bounds_y[0] - buffer,
             ax_bounds_y[1] + buffer)
        )

    # Expand width if height is larger
    elif ax_width < ax_height:
        buffer = (ax_height - ax_width) / 2
        ax.set_xlim(
            (ax_bounds_x[0] - buffer,
             ax_bounds_x[1] + buffer)
        )


# ==========================================
# MAIN PROGRAM
# ==========================================

if __name__ == "__main__":

    # Load the country data
    world = read_file(
        "../../data/natural-earth/ne_10m_admin_0_countries.shp"
    )

    # Extract Iceland
    iceland = world[world.ISO_A3 == "ISL"]

    # Load natural features
    land_cover = read_file(
        "../../data/iceland/gis_osm_natural_a_free_1.shp"
    )

    # Extract glaciers
    ice = land_cover[land_cover.fclass == "glacier"]

    # Get the bounds of Iceland
    minx, miny, maxx, maxy = iceland.total_bounds

    # Define geographical CRS and ellipsoid
    geo_string = "+proj=longlat +datum=WGS84 +no_defs"
    g = Geod(ellps="WGS84")

    # --------------------------------------
    # DEFINE THREE PROJECTIONS
    # --------------------------------------

    projections = [
        {
            'name': "Web Mercator",
            'description': "Global Conformal",
            'proj': (
                "+proj=merc +a=6378137 +b=6378137 "
                "+lat_ts=0 +lon_0=0 +x_0=0 +y_0=0 "
                "+k=1 +units=m +nadgrids=@null "
                "+wktext +no_defs"
            )
        },
        {
            'name': "Eckert IV",
            'description': "Global Equal Area",
            'proj': (
                "+proj=eck4 +lon_0=0 +x_0=0 +y_0=0 "
                "+datum=WGS84 +units=m +no_defs +type=crs"
            )
        },
        {
            'name': "Iceland Lambert Azimuthal Equal Area",
            'description': "Local Equal Area",
            'proj': (
                "+proj=laea +lon_0=-18.984375 "
                "+lat_0=64.6305525 +datum=WGS84 "
                "+units=m +no_defs"
            )
        }
    ]

    # --------------------------------------
    # CREATE THE MAP
    # --------------------------------------

    fig, my_axs = subplots(
        2, 2,
        figsize=(10, 10),
        constrained_layout=True
    )

    fig.suptitle("How much Ice is in Iceland?\n", fontsize=20)

    text = ""

    # --------------------------------------
    # LOOP THROUGH EACH PROJECTION
    # --------------------------------------

    for ax_num, projection in enumerate(projections):

        # Get the position of the current subplot
        axx = ax_num // my_axs.shape[0]
        axy = ax_num % my_axs.shape[0]

        # Initialise the coordinate transformer
        transformer = Transformer.from_crs(
            CRS.from_proj4(geo_string),
            CRS.from_proj4(projection['proj']),
            always_xy=True
        )

        # Calculate distortion
        Ep, Es, Ea = evaluate_distortion(
            g, transformer,
            minx, miny, maxx, maxy,
            10000, 1000000, 1000
        )

        # Calculate ice area in km2
        ice_area_km2 = (
            ice.to_crs(projection['proj'])
            .geometry.area.sum() / 1000000
        )

        # Report results in Console
        print(
            f"\n{projection['name']} "
            f"({projection['description']})"
        )

        print(f"   {'Distance distortion (Ep):':<26}{Ep:.6f}")
        print(f"   {'Shape distortion (Es):':<26}{Es:.6f}")
        print(f"   {'Area distortion (Ea):':<26}{Ea:.6f}")
        print(f"   {'Ice Area:':<26}{ice_area_km2:,.0f} km sq.")

        # ----------------------------------
        # PLOT THE CURRENT PROJECTION
        # ----------------------------------

        # Add results to the figure text
        text += (
            f"{projection['name']}:\n"
            f" Ep={Ep:.4f}  Es={Es:.4f}  Ea={Ea:.4f}\n\n"
        )

        # Disable the axis and set title
        my_axs[axx][axy].axis("off")
        my_axs[axx][axy].set_facecolor("#000000")

        my_axs[axx][axy].set_title(
            f"{projection['name']} "
            f"({projection['description']})\n"
            f"Ice area: {ice_area_km2:,.0f} km sq.",
            fontsize=10
        )

        # Plot Iceland
        iceland.to_crs(projection['proj']).plot(
            ax=my_axs[axx][axy],
            color="#b2df8a",
            edgecolor="#33a02c",
            linewidth=0.2
        )

        # Plot glaciers
        ice.to_crs(projection['proj']).plot(
            ax=my_axs[axx][axy],
            color="#e6f5f9",
            edgecolor="#e6f5f9",
            linewidth=0.1
        )

        # Add scalebar
        my_axs[axx][axy].add_artist(
            ScaleBar(
                dx=1,
                units="m",
                location="lower right"
            )
        )

        # Make map bounds square
        make_bounds_square(my_axs[axx][axy])

    # --------------------------------------
    # FINAL RESULTS PANEL
    # --------------------------------------

    # Disable the empty fourth axis
    my_axs[1][1].axis("off")

    # Create glacier legend
    my_axs[1][1].legend(
        [
            Patch(
                facecolor="#e6f5f9",
                edgecolor="#e6f5f9",
                label="Glacier"
            )
        ],
        ["Glacier"],
        loc="lower right"
    )

    # Add north arrow
    x, y, arrow_length = 0.9, 0.3, 0.15

    my_axs[1][1].annotate(
        "N",
        xy=(x, y),
        xytext=(x, y - arrow_length),
        arrowprops=dict(
            facecolor="black",
            width=3,
            headwidth=9
        ),
        ha="center",
        va="center",
        fontsize=16,
        xycoords=my_axs[1][1].transAxes
    )

    # Display numerical results
    my_axs[1][1].text(
        0.05,
        0.85,
        text,
        fontfamily="monospace",
        fontsize=8,
        va="top",
        transform=my_axs[1][1].transAxes
    )

    # Save the map
    Path("out").mkdir(exist_ok=True)

    savefig("out/5.png", bbox_inches="tight")

    print("done!")
