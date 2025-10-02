# SPDX-FileCopyrightText: Copyright (c) 2022-2024 The Lethe Authors
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception OR LGPL-2.1-or-later

# Listing of Parameters
#----------------------

set dimension = 3

#---------------------------------------------------
# Simulation Control
#---------------------------------------------------

subsection simulation control
  set time step         = 1e-5
  set time end          = 7.5
  set log frequency     = 10000
  set output frequency  = 10000000
  set output path       = ./out_{{N_NODES}}/
  set output boundaries = true
end

#---------------------------------------------------
# Model parameters
#---------------------------------------------------

subsection model parameters
  subsection contact detection
    set contact detection method                = dynamic
    set dynamic contact search size coefficient = 0.9
    set neighborhood threshold                  = 1.3
  end
  subsection load balancing
    set load balance method = frequent
    set frequency           = 50000
  end
  set particle particle contact force method = hertz_mindlin_limit_overlap
  set particle wall contact force method     = nonlinear
  set rolling resistance torque method       = constant
  set integration method                     = velocity_verlet
end

#---------------------------------------------------
# Physical Properties
#---------------------------------------------------

subsection lagrangian physical properties
  set g                        = 0.0, -9.81, 0.0
  set number of particle types = 1
  subsection particle type 0
    set size distribution type            = uniform
    set diameter                          = 0.00224
    set number of particles               = {{N_PARTICLES}}
    set density particles                 = 2500
    set young modulus particles           = 1e6
    set poisson ratio particles           = 0.3
    set restitution coefficient particles = 0.94
    set friction coefficient particles    = 0.2
    set rolling friction particles        = 0.1786
  end
  set young modulus wall           = 1e6
  set poisson ratio wall           = 0.3
  set friction coefficient wall    = 0.2
  set restitution coefficient wall = 0.9
  set rolling friction wall        = 0.1786
end

#---------------------------------------------------
# Insertion Info
#---------------------------------------------------

subsection insertion info
  set insertion method                               = volume
  set inserted number of particles at each time step = {{N_PARTICLES}}
  set insertion frequency                            = 25000
  set insertion box points coordinates               = -0.06, 0.10644, 0.00004 : 0.06,  0.16020, {{INSERT_Z}}
  set insertion direction sequence                   = 2,0,1
  set insertion distance threshold                   = 1.5
  set insertion maximum offset                       = 0.1
  set insertion prn seed                             = 20
end

#---------------------------------------------------
# Mesh
#---------------------------------------------------

subsection mesh
  set type               = dealii
  set grid type          = subdivided_hyper_rectangle
  set grid arguments     = 1,3,{{N_REFINEMENT_Z}} : -0.06272, -0.16244, 0 : 0.06272, 0.16244, {{Z_DEPT}}: true 
  set initial refinement = 4
end

#---------------------------------------------------
# Floating Walls
#---------------------------------------------------

subsection floating walls
  set number of floating walls = 1
  subsection wall 0
    subsection point on wall
      set x = 0
      set y = 0
      set z = 0
    end
    subsection normal vector
      set nx = 0
      set ny = 1
      set nz = 0
    end
    set start time = 0
    set end time   = 4
  end
end


#---------------------------------------------------
# Solid Objects
#---------------------------------------------------
subsection solid objects
  subsection solid surfaces
    set number of solids = 1
    subsection solid object 0 
      subsection mesh
        set type                = gmsh
        set file name           = ./{{GMSH}}
        set simplex             = true
        set initial refinement  = 0
        set initial translation = 0, 0, 0
      end
      subsection translational velocity
        set Function expression = 0 ; 0 ; 0
      end
      set output solid object = false
    end
  end
end


#---------------------------------------------------
# Boundary conditions DEM
#---------------------------------------------------

subsection DEM boundary conditions
  set number of boundary conditions = 1
   subsection boundary condition 0
    set type               = periodic
    set periodic id 0      = 4
    set periodic id 1      = 5
    set periodic direction = 2
  end
end
