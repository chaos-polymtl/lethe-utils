#!/usr/bin/env python3
"""
Generate a GMSH mesh for a packed bed of spheres.

Three meshing modes
-------------------
  outside  – mesh only the interstitial (fluid) region between the spheres (default)
  inside   – mesh only the sphere interiors
  both     – mesh both regions with a conforming interface (BooleanFragments)

Usage examples
--------------
  python generate_pb_geo.py datafile.txt
  python generate_pb_geo.py datafile.txt --mode both -o packed_bed_both.msh
  python generate_pb_geo.py datafile.txt --mode inside --h-min 1e-4 --h-max 5e-4
  python generate_pb_geo.py datafile.txt --x0 -0.005 --dx 0.01 --gui
"""

import argparse
import sys

import numpy as np

try:
    import gmsh
except ImportError:
    sys.exit(
        "Error: the 'gmsh' Python package is required.\n"
        "Install it with:  pip install gmsh"
    )


# ──────────────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────────────

def build_parser():
    p = argparse.ArgumentParser(
        description="Generate a GMSH mesh for a packed bed of spheres.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("datafile", help="Text file with columns: x y z radius")
    p.add_argument("-o", "--output", default="packed_bed.msh",
                   help="Output mesh file")

    geo = p.add_argument_group("Box geometry")
    geo.add_argument("--x0", type=float, default=-0.004, help="Box corner x")
    geo.add_argument("--y0", type=float, default=-0.004, help="Box corner y")
    geo.add_argument("--z0", type=float, default=0.0,    help="Box corner z")
    geo.add_argument("--dx", type=float, default=0.008,  help="Box extent in x")
    geo.add_argument("--dy", type=float, default=0.008,  help="Box extent in y")
    geo.add_argument("--dz", type=float, default=0.014,  help="Box extent in z")

    mesh = p.add_argument_group("Mesh parameters")
    mesh.add_argument("--h-min", type=float, default=5e-5, metavar="H",
                      help="Minimum element size")
    mesh.add_argument("--h-max", type=float, default=5e-4, metavar="H",
                      help="Maximum element size")
    mesh.add_argument("--buffer", type=float, default=0.99,
                      help="Radius scaling factor (<1 prevents surfaces from touching)")
    mesh.add_argument("--mode", choices=["outside", "inside", "both"],
                      default="outside",
                      help="Which region(s) to mesh")
    mesh.add_argument("--order", type=int, default=1, choices=[1, 2],
                      help="Finite element order")
    mesh.add_argument("--subdivision", type=int, default=2,
                      help="Mesh.SubdivisionAlgorithm (2 → hexahedra)")

    p.add_argument("--gui", action="store_true",
                   help="Open the GMSH GUI after meshing")
    return p


# ──────────────────────────────────────────────────────────────────────────────
# Data loading
# ──────────────────────────────────────────────────────────────────────────────

def load_spheres(path, buffer):
    """Load sphere centres and radii; apply the buffer factor."""
    try:
        data = np.loadtxt(path, skiprows=1)
    except Exception as exc:
        sys.exit(f"Cannot read '{path}': {exc}")

    if data.ndim == 1:          # single-sphere file
        data = data[np.newaxis, :]
    if data.shape[1] < 4:
        sys.exit(f"'{path}' must have at least 4 columns (x y z radius).")

    x, y, z, r = data[:, 0], data[:, 1], data[:, 2], data[:, 3]
    r = buffer * r

    if np.any(r <= 0):
        sys.exit("All radii must be positive after applying the buffer factor.")

    print(f"Loaded {len(x)} sphere(s) from '{path}'  (buffer={buffer})")
    return x, y, z, r


# ──────────────────────────────────────────────────────────────────────────────
# Geometry construction
# ──────────────────────────────────────────────────────────────────────────────

def build_geometry(occ, x, y, z, r, x0, y0, z0, dx, dy, dz, mode):
    """
    Build the CAD geometry and return (fluid_vols, sphere_vols).

    fluid_vols  – GMSH volume tags for the interstitial region (empty for 'inside')
    sphere_vols – GMSH volume tags for sphere interiors       (empty for 'outside')

    Boolean operations used per mode
    ---------------------------------
    outside  : occ.cut        – removes spheres from the box
    inside   : occ.intersect  – clips spheres to the box interior
    both     : occ.fragment   – splits all volumes at shared boundaries
                                (conformal mesh between fluid and sphere regions)
    """
    # Warn about any sphere that extends outside the box — those spheres will
    # be absent from (or truncated in) the mesh, which is usually unintended.
    xmax, ymax, zmax = x0 + dx, y0 + dy, z0 + dz
    outside = np.where(
        (x - r < min(x0, xmax)) | (x + r > max(x0, xmax)) |
        (y - r < min(y0, ymax)) | (y + r > max(y0, ymax)) |
        (z - r < min(z0, zmax)) | (z + r > max(z0, zmax))
    )[0]
    if outside.size:
        print(
            f"Warning: {outside.size} sphere(s) extend outside the box "
            f"(indices {outside.tolist()}).\n"
            f"  Box  z-range : [{min(z0,zmax):.6g}, {max(z0,zmax):.6g}]\n"
            f"  Sphere z-range: [{np.min(z-r):.6g}, {np.max(z+r):.6g}]\n"
            f"  Tip: if you shifted z0 downward, increase dz by the same amount\n"
            f"  to keep the top of the box at the same position."
        )

    box_tag = occ.addBox(x0, y0, z0, dx, dy, dz)
    sphere_tags = [
        occ.addSphere(float(xi), float(yi), float(zi), float(ri))
        for xi, yi, zi, ri in zip(x, y, z, r)
    ]
    occ.synchronize()
    print(f"Created 1 box and {len(sphere_tags)} sphere(s).")

    if mode == "outside":
        # BooleanDifference: keep box minus sphere interiors
        out, _ = occ.cut(
            [(3, box_tag)],
            [(3, t) for t in sphere_tags],
            removeObject=True, removeTool=True,
        )
        occ.synchronize()
        fluid_vols  = [tag for dim, tag in out if dim == 3]
        sphere_vols = []

    elif mode == "inside":
        # BooleanIntersection: keep only the parts of each sphere inside the box
        out, _ = occ.intersect(
            [(3, t) for t in sphere_tags],
            [(3, box_tag)],
            removeObject=True, removeTool=True,
        )
        occ.synchronize()
        fluid_vols  = []
        sphere_vols = [tag for dim, tag in out if dim == 3]

    else:  # both
        # BooleanFragments: split everything at shared boundaries so that the
        # fluid/sphere interface is meshed conformally.
        # parent_map[0]  → new volumes originating from the box (interstitial)
        # parent_map[1:] → new volumes originating from each sphere
        out, parent_map = occ.fragment(
            [(3, box_tag)],
            [(3, t) for t in sphere_tags],
            removeObject=True, removeTool=True,
        )
        occ.synchronize()
        fluid_vols  = [tag for dim, tag in parent_map[0] if dim == 3]
        sphere_vols = [
            tag
            for pmap in parent_map[1:]
            for dim, tag in pmap
            if dim == 3
        ]

    print(f"  Fluid  volumes : {fluid_vols}")
    print(f"  Sphere volumes : {sphere_vols}")
    return fluid_vols, sphere_vols


# ──────────────────────────────────────────────────────────────────────────────
# Surface classification
# ──────────────────────────────────────────────────────────────────────────────

def classify_surfaces(x0, y0, z0, dx, dy, dz):
    """
    Partition all 2-D entities into four groups by bounding-box position:
      bottom      – z = z0           (inlet)
      top         – z = z0 + dz      (outlet)
      walls       – the four lateral faces
      sphere_surfs – everything else  (sphere boundaries / fluid-sphere interface)

    Returns (bottom, top, walls, sphere_surfs) as lists of surface tags.
    """
    xmax, ymax, zmax = x0 + dx, y0 + dy, z0 + dz
    tol = 1e-6 * min(abs(dx), abs(dy), abs(dz))

    bottom, top, walls, sphere_surfs = [], [], [], []

    for _, tag in gmsh.model.getEntities(2):
        sxmin, symin, szmin, sxmax, symax, szmax = gmsh.model.getBoundingBox(2, tag)

        on_zmin = abs(szmin - z0)   < tol and abs(szmax - z0)   < tol
        on_zmax = abs(szmin - zmax) < tol and abs(szmax - zmax) < tol
        on_xmin = abs(sxmin - x0)   < tol and abs(sxmax - x0)   < tol
        on_xmax = abs(sxmin - xmax) < tol and abs(sxmax - xmax) < tol
        on_ymin = abs(symin - y0)   < tol and abs(symax - y0)   < tol
        on_ymax = abs(symin - ymax) < tol and abs(symax - ymax) < tol

        if on_zmin:
            bottom.append(tag)
        elif on_zmax:
            top.append(tag)
        elif on_xmin or on_xmax or on_ymin or on_ymax:
            walls.append(tag)
        else:
            sphere_surfs.append(tag)

    return bottom, top, walls, sphere_surfs

def classify_surfaces_from_fluid(fluid_vols, sphere_vols, x0, y0, z0, dx, dy, dz):
    """
    Classify the boundary surfaces of the meshed region into four groups:
      bottom      – z = z0           (inlet face)
      top         – z = z0 + dz      (outlet face)
      walls       – the four lateral faces
      sphere_surfs – everything else  (sphere boundaries / fluid-sphere interface)

    The classification uses the center-of-mass (CoM) of each surface.  This is
    reliable for planar box faces because a planar face's CoM lies exactly on
    the plane, even when the face has holes punched through it by boolean ops.

    Parameters
    ----------
    fluid_vols  : list of int  – volume tags for the fluid region
    sphere_vols : list of int  – volume tags for sphere interiors
                  When fluid_vols is empty (mode='inside'), sphere_vols is used
                  as the source for boundary extraction instead.
    x0, y0, z0  : box corner coordinates
    dx, dy, dz  : box extents (must be non-zero; sign determines direction)

    Returns (bottom, top, walls, sphere_surfs) as lists of surface tags.
    """
    xmax, ymax, zmax = x0 + dx, y0 + dy, z0 + dz

    # Use abs() so the tolerances are positive regardless of the sign of each
    # extent (a negative extent is valid GMSH geometry, just reversed direction).
    L = min(abs(dx), abs(dy), abs(dz))

    # tol_plane: CoM must be within this distance of the box face plane.
    # Planar faces have their CoM exactly on the plane (up to floating-point
    # rounding ~1e-15 m), so 1e-6 * L gives a comfortable margin.
    tol_plane = 1e-6 * L

    # tol_area: faces smaller than this are assumed to be numerical slivers
    # from boolean operations (OpenCASCADE precision artefacts can reach
    # ~(1e-7 m)^2 = 1e-14 m^2; 1e-8 * L^2 sits safely above that without
    # risking filtering real sphere-cap patches).
    tol_area = 1e-8 * L * L

    bottom, top, walls, sphere_surfs = [], [], [], []

    # In 'outside' or 'both' modes fluid_vols is populated and its boundary
    # covers both the box faces and the sphere surfaces.
    # In 'inside' mode fluid_vols is empty; fall back to sphere volume boundaries
    # (sphere surfaces + any flat caps where spheres are clipped by the box).
    source_vols = fluid_vols if fluid_vols else sphere_vols
    if not source_vols:
        return bottom, top, walls, sphere_surfs

    bnd = gmsh.model.getBoundary(
        [(3, v) for v in source_vols],
        oriented=False,
        recursive=False,
    )

    surface_tags = list({tag for dim, tag in bnd if dim == 2})

    for tag in surface_tags:
        com  = gmsh.model.occ.getCenterOfMass(2, tag)
        area = gmsh.model.occ.getMass(2, tag)

        # Skip numerical sliver faces produced by boolean operations
        if area < tol_area:
            continue

        if abs(com[2] - z0) < tol_plane:
            bottom.append(tag)
        elif abs(com[2] - zmax) < tol_plane:
            top.append(tag)
        elif (abs(com[0] - x0)   < tol_plane
              or abs(com[0] - xmax) < tol_plane
              or abs(com[1] - y0)   < tol_plane
              or abs(com[1] - ymax) < tol_plane):
            walls.append(tag)
        else:
            sphere_surfs.append(tag)

    return bottom, top, walls, sphere_surfs

# ──────────────────────────────────────────────────────────────────────────────
# Physical groups
# ──────────────────────────────────────────────────────────────────────────────

def assign_physical_groups(fluid_vols, sphere_vols, bottom, top, walls, sphere_surfs):
    """Assign named physical groups; skip any group that is empty."""

    def add(dim, tags, tag, name):
        if not tags:
            return
        gmsh.model.addPhysicalGroup(dim, tags, tag=tag, name=name)
        kind = "Volume" if dim == 3 else "Surface"
        print(f"  Physical{kind}({tag}) '{name}': tags {tags}")

    add(3, fluid_vols,   tag=0,  name="fluid")
    add(3, sphere_vols,  tag=1,  name="spheres")
    add(2, bottom,       tag=10, name="inlet")
    add(2, top,          tag=11, name="outlet")
    add(2, walls,        tag=12, name="walls")
    add(2, sphere_surfs, tag=13, name="sphere_surfaces")


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def main():
    args = build_parser().parse_args()
    x, y, z, r = load_spheres(args.datafile, args.buffer)

    gmsh.initialize()
    gmsh.model.add("packed_bed")
    occ = gmsh.model.occ

    # ── Geometry ──────────────────────────────────────────────────────────────
    fluid_vols, sphere_vols = build_geometry(
        occ, x, y, z, r,
        args.x0, args.y0, args.z0,
        args.dx, args.dy, args.dz,
        args.mode,
    )

    # ── Surface classification ─────────────────────────────────────────────
    #bottom, top, walls, sphere_surfs = classify_surfaces(
    #    args.x0, args.y0, args.z0, args.dx, args.dy, args.dz
    #)
    bottom, top, walls, sphere_surfs = classify_surfaces_from_fluid(
        fluid_vols, sphere_vols,
        args.x0, args.y0, args.z0,
        args.dx, args.dy, args.dz,
    )

    print(
        f"Surfaces — bottom: {len(bottom)}, top: {len(top)}, "
        f"walls: {len(walls)}, sphere: {len(sphere_surfs)}"
    )



    # ── Physical groups ────────────────────────────────────────────────────
    assign_physical_groups(fluid_vols, sphere_vols, bottom, top, walls, sphere_surfs)

    # ── Mesh settings ──────────────────────────────────────────────────────
    gmsh.option.setNumber("Mesh.CharacteristicLengthMin", args.h_min)
    gmsh.option.setNumber("Mesh.CharacteristicLengthMax", args.h_max)
    gmsh.option.setNumber("Mesh.ElementOrder",            args.order)
    gmsh.option.setNumber("Mesh.SecondOrderLinear",       1)
    gmsh.option.setNumber("Mesh.HighOrderOptimize",       1)
    gmsh.option.setNumber("Mesh.SubdivisionAlgorithm",    args.subdivision)

    # ── Generate and save ──────────────────────────────────────────────────
    print(f"Generating 3-D mesh (mode='{args.mode}') …")
    gmsh.model.mesh.generate(3)
    gmsh.write(args.output)
    print(f"Mesh written to '{args.output}'")

    if args.gui:
        gmsh.fltk.run()

    gmsh.finalize()


if __name__ == "__main__":
    main()
