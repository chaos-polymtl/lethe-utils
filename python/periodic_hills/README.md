# Post-processing scripts for the periodic hills case

This folder contains the necessary tools to post-process simulations for the periodic_hills test cases:

Extraction of literature data:
1. Results from Breuer simulations and Rapp experiments are available in the lit folder with the appropriate format.
2. Use `literature_data_extraction.py` script to extract the data with appropriate format to use in all the other scripts. 


Extraction of lethe data:
1. Create csv data files from the paraview files obtained by running the simulation with Lethe. 
   Place them in a folder named lethe_data.
2. Extract the corresponding data using the `lethe_data_extraction.py` tool. 
3. Use specific post-processing scripts:
   * `plot_data_with_geometry_baseline.py`
   * `plot_data_time_averaging_per_data_type_two_meshes_horizontal.py`
   * `plot_data_time_stepping_per_data_type_two_meshes_horizontal.py`
   * `plot_data_with_geometry_mesh_refinement.py`
   * `plot_data_with_geometry_high_order.py`
   * `plot_data_with_geometry_higher_reynolds.py`
   * `reattachment_plot_mesh_refinement.py`

Other scripts available in the folder:

* The `breuer2009_data_comparison.py` script compares two different sources for the data of the Breuer article. This code is intended mostly as a verification and should not be used when post-processing simulation data.

* The `near_wall_processing.py` script outputs the reattachment point, average y+ and maximum y+ along the lower wall for Lethe simulations, and plots y+.

* The `y_plus_on_geometry.py` script plots y+ superimposed over the periodic hill geometry.

**Note:** In all the scripts there are inputs such as: the Reynolds number of the simulation, the path to the lethe extracted data, the file names of the lethe data and the corresponding labels for the plot. Whenever zoom-in plots are available, the limits are hardcoded as well. 