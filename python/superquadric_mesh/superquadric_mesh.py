#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File   : mesh_superquadric.py
# License: MIT
# Author : Andrei Leonard Nicusan <a.l.nicusan@bham.ac.uk>
# Date   : 11.01.2023


import gmsh
import numpy as np


class Superquadric:
    '''Programmatically create superquadric geometry using the OpenCASCADE
    kernel of GMSH. It can then be meshed as is or subtracted from a bounding
    volume to create a conformal mesh. Or thrown away, you decide.

    The implicit superquadric equation used is:

        |x/a|^r + |y/b|^s + |z/c|^t = 1

    where [a, b, c] represent the aspect ratio and [r, s, t] set the
    blockiness.

    Parameters
    ----------
    aspect_ratio : np.array[(3,), float], default [1, 1, 1]
        Per-dimension multiplicative elongation factor.

    blockiness : np.array[(3,), float], default [2, 2, 2]
        Exponents used in superquadric equation: 2 yields a sphere, the greater
        above 2, the closer to a box it is; 1 is an octahedron and between
        (0, 2) it becomes pointier / rounder, respectively.

    num_vertical : int, default 10
        Number of vertical discretisation points.

    num_horizontal : int, default 10
        Number of horizontal discretisation_points.

    Attributes
    ----------
    points : list[np.ndarray[ndim=2, float]]
        The 3D discretisation points at each vertical level, going up; at
        level 0 and num_vertical - 1 are the apexes.

    point_tags : list[list[int]]
        The GMSH integer tags of the points at each vertical level.

    vertical_line_tags : list[list[int]]
        The GMSH integer tags of the vertical lines connecting points, at each
        vertical level.

    horizontal_line_tags : list[list[int]]
        The GMSH integer tags of the horizontal lines connecting points, at
        each vertical level.

    surface_tags : list[int]
        The GMSH integer tags of the surfaces, going anti-clockwise at each
        vertical level (this list is flattened).

    volume_tag : int
        The GMSH integer tag of the superquadric 3D volume.

    Examples
    --------
    Create a unit sphere:

    >>> sphere = Superquadric([1, 1, 1], [2, 2, 2])

    Create a box with slightly rounded corners of side length 4:

    >>> box = Superquadric([2, 2, 2], [10, 10, 10], 24, 24)

    Create an octahedron:

    >>> octahedron = Superquadric([1, 1, 1], [1, 1, 1])

    '''

    def __init__(
        self,
        aspect_ratio = [1, 1, 1],
        blockiness = [2, 2, 2],
        num_vertical = 10,
        num_horizontal = 10,
    ):
        # Type-checking input parameters
        aspect_ratio = np.asarray(aspect_ratio, dtype = float)
        assert aspect_ratio.ndim == 1
        assert len(aspect_ratio) == 3
        assert np.all(aspect_ratio > 0)

        blockiness = np.asarray(blockiness, dtype = float)
        assert blockiness.ndim == 1
        assert len(blockiness) == 3
        assert np.all(blockiness > 0)

        num_vertical = int(num_vertical)
        assert num_vertical >= 3

        num_horizontal = int(num_horizontal)
        assert num_horizontal >= 3

        # Saving superquadric settings
        self.aspect_ratio = aspect_ratio
        self.blockiness = blockiness
        self.num_vertical = num_vertical
        self.num_horizontal = num_horizontal

        # Add points in a list[list[tag]] of tags at each vertical level,
        # from bottom up
        points = []
        point_tags = []

        for i in range(num_vertical):
            horizontal_points = []
            horizontal_point_tags = []

            vangle = -np.pi / 2 + i * np.pi / (num_vertical - 1)

            for j in range(num_horizontal):

                # Bottom and top should have only a single point added
                if (i == 0 or i == num_vertical - 1) and j > 0:
                    break

                hangle = -np.pi + j * 2 * np.pi / num_horizontal

                x = (
                    aspect_ratio[0] *
                    np.sign(np.cos(vangle)) *
                    np.abs(np.cos(vangle))**(2 / blockiness[0]) *
                    np.sign(np.cos(hangle)) *
                    np.abs(np.cos(hangle))**(2 / blockiness[0])
                )

                y = (
                    aspect_ratio[1] *
                    np.sign(np.cos(vangle)) *
                    np.abs(np.cos(vangle))**(2 / blockiness[1]) *
                    np.sign(np.sin(hangle)) *
                    np.abs(np.sin(hangle))**(2 / blockiness[1])
                )

                z = (
                    aspect_ratio[2] *
                    np.sign(np.sin(vangle)) *
                    np.abs(np.sin(vangle))**(2 / blockiness[2])
                )

                horizontal_points.append([x, y, z])
                horizontal_point_tags.append(gmsh.model.occ.addPoint(x, y, z))

            points.append(np.array(horizontal_points))
            point_tags.append(horizontal_point_tags)

        self.points = points
        self.point_tags = point_tags

        gmsh.model.occ.synchronize()

        # Connect points into lines, wires, surfaces
        vertical_line_tags = []
        horizontal_line_tags = []
        surface_tags = []

        # Bottom cap: join apex with side points to form triangles
        level_vertical_lines = []
        level_horizontal_lines = []

        for j in range(len(point_tags[1])):
            level_vertical_lines.append(gmsh.model.occ.addLine(
                point_tags[0][0],
                point_tags[1][j],
            ))

            level_horizontal_lines.append(gmsh.model.occ.addLine(
                point_tags[1][j],
                point_tags[1][(j + 1) % len(point_tags[1])],
            ))

        vertical_line_tags.append(level_vertical_lines)
        horizontal_line_tags.append(level_horizontal_lines)

        for j in range(len(point_tags[1])):
            wire_tag = gmsh.model.occ.addWire([
                vertical_line_tags[0][j],
                horizontal_line_tags[0][j],
                vertical_line_tags[0][(j + 1) % len(point_tags[1])]
            ])

            surface_tags.append(gmsh.model.occ.addPlaneSurface([wire_tag]))

        gmsh.model.occ.synchronize()

        # Sides: join four points at a time to form quadrilaterals
        for i in range(1, len(point_tags) - 2):
            level_vertical_lines = []
            level_horizontal_lines = []

            for j in range(len(point_tags[i])):

                level_vertical_lines.append(gmsh.model.occ.addLine(
                    point_tags[i][j],
                    point_tags[i + 1][j],
                ))

                level_horizontal_lines.append(gmsh.model.occ.addLine(
                    point_tags[i + 1][j],
                    point_tags[i + 1][(j + 1) % len(point_tags[i])],
                ))

            vertical_line_tags.append(level_vertical_lines)
            horizontal_line_tags.append(level_horizontal_lines)

        for i in range(1, len(point_tags) - 2):
            for j in range(len(point_tags[i])):
                wire_tag = gmsh.model.occ.addWire([
                    vertical_line_tags[i][j],
                    horizontal_line_tags[i - 1][j],
                    vertical_line_tags[i][(j + 1) % len(point_tags[i])],
                    horizontal_line_tags[i][j],
                ])

                surface_tags.append(gmsh.model.occ.addPlaneSurface([wire_tag]))

        # Top cap: join apex with side points to form triangles
        level_vertical_lines = []

        for j in range(len(point_tags[-2])):
            imax = len(point_tags) - 1

            level_vertical_lines.append(gmsh.model.occ.addLine(
                point_tags[-2][j],
                point_tags[-1][0],
            ))

        vertical_line_tags.append(level_vertical_lines)

        for j in range(len(point_tags[-2])):
            wire_tag = gmsh.model.occ.addWire([
                vertical_line_tags[-1][j],
                horizontal_line_tags[-1][j],
                vertical_line_tags[-1][(j + 1) % len(point_tags[-2])]
            ])

            surface_tags.append(gmsh.model.occ.addPlaneSurface([wire_tag]))

        gmsh.model.occ.synchronize()

        self.vertical_line_tags = vertical_line_tags
        self.horizontal_line_tags = horizontal_line_tags
        self.surface_tags = surface_tags

        # Join surfaces and create enclosing volume
        surface_loop_tag = gmsh.model.occ.addSurfaceLoop(surface_tags)
        self.volume_tag = gmsh.model.occ.addVolume([surface_loop_tag])

        gmsh.model.occ.synchronize()


    def __repr__(self):
        # Dynamically construct display string showing all attributes not
        # starting with underscore
        name = self.__class__.__name__
        underline = "-" * len(name)

        docstr = [name, underline]
        for att_name in dir(self):
            att = getattr(self, att_name)
            if not callable(att) and not att_name.startswith("_"):
                att_str = str(att)
                if "\n" in att_str or len(att_name) + len(att_str) > 75:
                    rem = max(0, 75 - len(att_name))
                    att_str = att_str.replace("\n", "\\n")[:rem] + "..."
                docstr.append(att_name + " = " + att_str)

        return "\n".join(docstr)




# If a previous instance of GMSH is running, close it
if gmsh.isInitialized():
    gmsh.finalize()


# Initialise GMSH and set number of OpenMP threads
gmsh.initialize()
gmsh.option.setNumber("General.NumThreads", 16)
gmsh.option.setNumber("Mesh.MshFileVersion", 2.2)


# Create new model
gmsh.model.add("Superquadric")


# Create superquadric geometry
superquadric = Superquadric(
    aspect_ratio = [1, 1, 1],
    blockiness = [2, 2, 2],
    num_vertical = 10,
    num_horizontal = 10,
)


# Add volume to physical group so it is saved later - can add surfaces for
# boundary conditions here too...
gmsh.model.addPhysicalGroup(3, [superquadric.volume_tag])


# Mesh sizing options
# gmsh.option.setNumber("Mesh.MeshSizeExtendFromBoundary", 1)
# gmsh.option.setNumber("Mesh.MeshSizeFromPoints", 0)
# gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", 120)

gmsh.option.setNumber("Mesh.Smoothing", 20)
gmsh.option.setNumber("Mesh.MeshSizeFactor", 0.8)
gmsh.option.setNumber("Mesh.MeshSizeMin", 0.01)
gmsh.option.setNumber("Mesh.MeshSizeMax", 0.1)


# Generate mesh
gmsh.model.mesh.generate(3)
gmsh.model.mesh.optimize("Netgen")


# Print mesh quality statistics
gmsh.plugin.setNumber("AnalyseMeshQuality", "ICNMeasure", 1)
gmsh.plugin.setNumber("AnalyseMeshQuality", "Recompute", 1)
gmsh.plugin.setNumber("AnalyseMeshQuality", "CreateView", 1)
gmsh.plugin.setNumber("AnalyseMeshQuality", "DimensionOfElements", 2)
gmsh.plugin.run("AnalyseMeshQuality")


# Save mesh
gmsh.write("superquadric.msh")


# Open GUI
gmsh.fltk.run()
