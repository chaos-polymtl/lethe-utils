
# 1.1 **Function documentation** 

Documentation to explain the VTU file translation and the initial condition's equation writing.

---

## 1.2 Translate function: [source code](./scr/initial_condition_functions.py)
```python
def translate_vtu_file(initial_filename, decimals, directory_vtu):
```
    VTU file translation in an array ([x,y,z,r] for each particle)

    Inputs:
        - prm :
            - initial_filename : VTU file name that needs translation (name.vtu)
            - decimals : number of decimals in initial conditions equation
            - directory_vtu : VTU file directory
    Output :
        - Array with position and radius of each particle
            -data_table=[x,y,z,r]

The first step is to translate the VTU file of the simulation. To be able to use this function, you need to have the name of the VTU file, the wished decimals number and the file directory. Those input will be introduced by the writing function. The output of the function is an array with the particles positions and the radius of each one. 


    ⚠️ The `translate_vtu_file` will not be call in the python file. 

---

## 1.3 Writing function: [source code](./scr/initial_condition_functions.py)
```python
def writing_initial_conditions(
    initial_filename,
    decimals=5,
    dimension='3D',
    directory_txt=os.path.abspath("."),
    directory_vtu=os.path.abspath(".") 
):
```
    Function to write initial conditions in a txt file (with indented if())
    Inputs:
        - prm :
            - initial_filename : VTU file name that needs translation (name.vtu)
            - decimals : Wished number of decimals in initial conditions equation
            - dimension : '3D' or '2D' (3D by default)
            - directory_txt : Wished txt file directory
            - directory_vtu : VTU file directory    
        Output :
            - Initial conditions equation txt file

The `writing_initial_conditions` is the only function call to generate the equation. This function take 5 parameters. The first one (`initial_filename`) is obligatory. This is the name of the VTU file ([VTU file example](./example/vtu_file/out.50_particles.vtu)). The second parameter is the wished decimals numbers. The third parameter is the dimension of the simulation, by default the parameter is set to `3D`. By default, the function will use 5 decimals number. The function has by default the present directory. ⚠️ If the VTU file is located in another directory, you must enter the path. You can place the txt file in an existent folder, but you need to specify the path. 


The output is a txt file with the initial condition equation. The equation form is for 2 particles :
```
((x-x_0)^2+(y-y_0)^2+(z-z_0)^2<(r_2)^2?1:((x-x_1)^2+(y-y_1)^2+(z-z_1)^2<(r_1)^2?1:0))
    if the condition is true
        return id=1
    if the condition is false 
        return id=0
```
The ID allows differentiating the two fluids in a VOF, the main goal of those functions,

# You can see an example of the use of these functions [here](example_heat_flux.md).
---



