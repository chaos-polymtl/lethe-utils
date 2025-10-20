# SPDX-FileCopyrightText: Copyright (c) 2025 The Lethe Authors
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception OR LGPL-2.1-or-later

#############################################################################
'''Importing Libraries'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pyvista as pv
import argparse


def circle_circle_intersection_area(R1, R2, d):
    """Area of intersection of two disks of radii R1, R2 separated by distance d."""
    R1, R2, d = float(R1), float(R2), float(d)
    if R1 <= 0 or R2 <= 0:
        return 0.0
    if d >= R1 + R2:
        return 0.0  # no overlap
    if d <= abs(R1 - R2):
        return np.pi * min(R1, R2)**2  # one fully inside the other

    term1 = R1**2 * np.arccos((d**2 + R1**2 - R2**2) / (2 * d * R1))
    term2 = R2**2 * np.arccos((d**2 + R2**2 - R1**2) / (2 * d * R2))
    term3 = 0.5 * np.sqrt(
        (-d + R1 + R2)*(d + R1 - R2)*(d - R1 + R2)*(d + R1 + R2)
    )
    return term1 + term2 - term3


def sphere_cylindrical_shell_overlap(center, radius, R, dR_in, dR_out, zmin, zmax, n_z=100):
    """
    Compute the overlap volume between a single sphere and a cylindrical shell.
    """
    x0, y0, z0 = center
    rc = np.hypot(x0, y0)
    Rin = R - dR_in
    Rout = R + dR_out
    r = radius

    # z-range where sphere intersects the shell volume
    z_lo = max(zmin, z0 - r)
    z_hi = min(zmax, z0 + r)
    if z_hi <= z_lo:
        return 0.0

    # z quadrature
    z = np.linspace(z_lo, z_hi, n_z)
    rho = np.sqrt(np.maximum(0.0, r**2 - (z - z0)**2))

    A = np.empty_like(z)
    for i in range(len(z)):
        if rho[i] <= 0:
            A[i] = 0.0
            continue
        A_outer = circle_circle_intersection_area(Rout, rho[i], rc)
        A_inner = circle_circle_intersection_area(Rin, rho[i], rc)
        A[i] = max(0.0, A_outer - A_inner)

    return np.trapz(A, z)


def total_cylindrical_shell_overlap(positions, diameters, R, dR_in, dR_out, zmin, zmax, n_z=100):
    """
    Compute the total overlap volume between many spheres and a cylindrical shell volume.

    Parameters
    ----------
    positions : (N,3) array-like
        Sphere centers.
    diameters : (N,) array-like
        Sphere diameters.
    R : float
        Mean radius of cylindrical shell.
    dR_in, dR_out : float
        Shell thickness inside/outside.
    zmin, zmax : float
        Axial limits of the shell.
    n_z : int
        Quadrature resolution along z.

    Returns
    -------
    total_volume : float
        Total overlap volume (sum of all particle intersections).

    """
    positions = np.asarray(positions, dtype=float)
    diameters = np.asarray(diameters, dtype=float)
    radii = 0.5 * diameters

    N = len(radii)
    volumes = np.zeros(N)

    for i in range(N):
        volumes[i] = sphere_cylindrical_shell_overlap(
            positions[i], radii[i], R, dR_in, dR_out, zmin, zmax, n_z=n_z
        )

    return volumes.sum()/(np.pi * ( (R + dR_out)**2 - (R - dR_in)**2 ) * (zmax - zmin))


#Take case path as argument and store it
parser = argparse.ArgumentParser(description='Arguments for the post-processing of the 3d-rectangular hopper DEM case')
parser.add_argument('--files', '-f', nargs='+', help='list of files')
args, leftovers=parser.parse_known_args()


#Number of radius sampling point
n_r = 100
R_I=0.0064
R_O=0.0234
radii = np.linspace(R_I, R_O, n_r)

H=0.25

prm_file_name = args.files

for file in prm_file_name:
    particles = pv.read(file)
    print(f'File: {file}, Number of particles: {particles.n_points}')

    #Extract position and diameter of the particles
    position = particles.points
    diameter = particles['diameter']
    radius = diameter/2.

    phi=np.zeros((n_r))
    #Loop over the radial circle and calculate the fraction of the surface of each cylinder shell covered by particles
    phi[0] = total_cylindrical_shell_overlap(position, diameter, radii[0], radii[0]-0, radii[1]-radii[0], 0., H)
    for i in range(1,n_r-1):
        phi[i] = total_cylindrical_shell_overlap(position, diameter, radii[i],radii[i]-radii[i-1],radii[i+1]-radii[i], 0., H)
    phi[-1] = total_cylindrical_shell_overlap(position, diameter, radii[-1], R_O-radii[-1], radii[-1]-radii[-2], 0., H)

    plt.plot(radii,phi,'s')

    # Calculate the integral of the volume fraction over the radius
    integral = np.trapz(phi * 2 * np.pi * radii, radii)
    print(f'Integral of volume fraction over the radius: {integral:.7f}')
plt.ylabel("Volume Fraction of solid")
plt.xlabel("Radius (m)")
plt.show()
    






