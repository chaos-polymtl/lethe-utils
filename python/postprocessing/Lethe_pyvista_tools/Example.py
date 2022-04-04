#To use the Lethe_pyvista_tools, you need to have python 3
#installed in your computer

#The modules necessary to run Lethe pyvista tools are:
#Pandas: pip install pandas
#PyVista: pip install pyvista

#To use Lethe_pyvista_tools, put the "Lethe_pyvista_tools.py" file inside
#The same directory as your python script and procceed as follows

#This line imports all Lethe_pyvista_tools functionalities
from Lethe_pyvista_tools import *

#This script prints out the content of your prm file as dictionary
#To run Lethe_pyvista_tools you need to specify the path to your
#case and the name of the .prm file
example = Lethe_pyvista_tools('PATH TO YOUR CASE', 'NAME_OF_YOUR_PARAMETERS_FILE.prm')

print('This is the dictionary of your .prm file:')
print(example.prm_dict)
print('To print out any value inside the dictionary, ask for it using ["parameter_name"] right after .prm_dict variable')

print('The path to the case can be seen using: example.case_path')

#To read the data to pyvista dataframe, use the following with
#the .pvd file as argument
example.read_lethe_to_pyvista('NAME_OF_YOUR_PVD_FILE.pvd')

#The read_lethe_to_pyvista method writes out the attributes .time_list,
#.list_vtu and reads the '.vtu' files inside the pointed folder as pyvista dataframes.
print('List of all .vtu: ')
print(example.list_vtu)
print('Time list, if transient: ')
print(example.time_list)

#Each .vtu file will correspond to a dataframe named df, such that the first vtu can be
#accessed through .df_0, the second .df_1, and so on.
print(example.df_0)

#This should print out the name of the arrays in the first vtu file of your case
print('Name of the arrays in your pyvista dataframe: ')
print(example.df_0.array_names)

#To further information about pyvista, refer to https://docs.pyvista.org/index.html