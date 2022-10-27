import pandas as pd
import numpy  as np
import time
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from pathlib import Path

from pyparsing import col

def boolstr_to_floatstr(v):
    if v == 'True':
        return '1'
    elif v == 'False':
        return '0'
    else:
        return v

def extract_data_from_one_file(file_path):
    df_test_data = pd.read_excel(file_path)
    for column in df_test_data:
        ## Capture of the data of interest
        if (df_test_data[column].name == "Temps (sec) - Vref"):
            # Time [s]
            t               = np.array(df_test_data[column])  
        elif (df_test_data[column].name == "Valeur  Calibrées - Capteur Pression 0-25 (kPa)"):
            # Pressure [kPa]
            pressure_25kpa  = np.array(df_test_data[column])  
        elif (df_test_data[column].name == "Valeur  Calibrées - Capteur Pression 0-250 (kPa)"):
            # Pressure [kPa]
            pressure_250kpa = np.array(df_test_data[column])  
        elif (df_test_data[column].name == "Valeur  Calibrées - Débit (ml/sec)"):
            # Set flow [ml/s]
            set_flow        = np.array(df_test_data[column])  
    ## Selection of the proper pressure sensor ()
    selector     = np.vectorize(boolstr_to_floatstr)(pressure_25kpa< 25).astype(float)
    not_selector = np.vectorize(boolstr_to_floatstr)(pressure_25kpa>=25).astype(float)
    pressure = pressure_25kpa*selector + pressure_250kpa*(not_selector)

    dataset = pd.DataFrame({'t'              : t              ,
                            'pressure'       : pressure       ,
                            'set_flow'       : set_flow       })
    return dataset

def extract_steady_data(dataset_complet,type_seq,start_seq_str):
    volumetric_flows     = []
    pressure_drops       = []
    pressure_drop_errors = []

    start_seq = np.array([float(x) for x in start_seq_str.split(";")])
    for i_start_time,start_time in enumerate(start_seq):
        if (type_seq=="120s_3niveaux"):
            set_flow_times = np.array([0  , 152,  316])
            lower_bound_tol= 20
            upper_bound_tol= 100
        elif (type_seq=="60s_6niveaux"):
            set_flow_times = np.array([0  , 86 ,  178, 276, 380, 490])
            lower_bound_tol= 10
            upper_bound_tol= 35
        elif (type_seq=="60s_3niveaux"):
            set_flow_times = np.array([0  , 86 ,  178])
            lower_bound_tol= 10
            upper_bound_tol= 35
            
        for i_set_flow_time,set_flow_time in enumerate(set_flow_times):
            lower_time_bound = start_time + set_flow_time + lower_bound_tol
            upper_time_bound = start_time + set_flow_time + upper_bound_tol
            boolean_selector = (np.array(dataset_complet['t'])>lower_time_bound) \
                                * (np.array(dataset_complet['t'])<=upper_time_bound)

            pressure_subset = np.array(dataset_complet['pressure'])[boolean_selector]
            pressure_min    = pressure_subset.min()
            pressure_max    = pressure_subset.max()
            pressure_mean   = pressure_subset.mean()
            set_flow_subset = np.array(dataset_complet['set_flow'])[boolean_selector]
            set_flow_mean   = set_flow_subset.mean()

            volumetric_flows    .append(set_flow_mean)
            pressure_drops      .append(pressure_mean)
            pressure_drop_errors.append(0.5*(pressure_max-pressure_min))

    dataset = pd.DataFrame({'volumetric_flows'     : volumetric_flows    ,
                            'pressure_drops'       : pressure_drops      ,
                            'pressure_drop_errors' : pressure_drop_errors})
    return dataset

def extract_no_flow_pressure(dataset_complet,no_flow_time_str):
    no_flow_time     = float(no_flow_time_str)
    lower_time_bound = no_flow_time + 0
    upper_time_bound = no_flow_time + 10
    boolean_selector = (np.array(dataset_complet['t'])>lower_time_bound) \
                        * (np.array(dataset_complet['t'])<=upper_time_bound)

    pressure_subset = np.array(dataset_complet['pressure'])[boolean_selector]
    pressure_mean   = pressure_subset.mean()
    return pressure_mean

def direct_function(x, a):
    return a * x

class constants():
    viscosity = 1e-3 # [Pa*s] / water viscosity at 20C
    thickness = 0.01 # [m]    / height of monolith cylinder
    diameter  = 0.01 # [m]    / diameter of monolith cylinder

def compute_permeability(dataset_steady):
    xdata        = dataset_steady['volumetric_flows']
    ydata        = dataset_steady['pressure_drops']
    popt, pcov   = curve_fit(direct_function, xdata, ydata)

    # permeability = volumetric_flow*dynamic_viscosity*medium_thickness/ cross_area*deltaP
    # https://en.wikipedia.org/wiki/Permeability_(Earth_sciences)
    cst          = constants()
    deltaP_over_Q= popt
    cross_area   = np.pi * 0.25 * cst.diameter**2
    permeability = cst.viscosity*cst.thickness/(deltaP_over_Q*cross_area)
    return permeability            

def output_graphs(all_monolith_names,
                    all_dataset_steady,
                    all_permeabilities):
    # We create one figure with all pressure drops and volumetric flows
    fig, ax = plt.subplots()
    colors = iter(plt.cm.rainbow(np.linspace(0, 1, len(all_monolith_names))))
    for i, monolith_name in enumerate(all_monolith_names):
        current_color = next(colors)
        ax.errorbar(x    =all_dataset_steady[i]['volumetric_flows'],
                    y    =all_dataset_steady[i]['pressure_drops'],
                    yerr =all_dataset_steady[i]['pressure_drop_errors'],
                    label=monolith_name+" exp.",
                    fmt="o",
                    c = current_color)
        xdata = np.linspace(0,
                            np.max(all_dataset_steady[i]['volumetric_flows']),
                            num      = 100,
                            endpoint = True)
        cst          = constants()
        cross_area   = np.pi * 0.25 * cst.diameter**2
        deltaP_over_Q = (cst.viscosity*cst.thickness)/(all_permeabilities[i]*cross_area)
        ax.plot(xdata,
                direct_function(xdata, deltaP_over_Q),
                label=monolith_name+" reg.",
                c = current_color)
    ax.set_xlabel("Volumetric flow [ml/s]")
    ax.set_ylabel("Pressure drop [kPa]")
    ax.set_title("Flow through various monoliths")
    ax.legend()
    plt.show()

def handle_all_files():
    all_monolith_names   = []
    all_dataset_steady   = []
    all_permeabilities   = []

    ## Read all the names of the tests to process
    tests_summary_file_name = Path('','tests_summary.xlsx')
    df_tests_summary        = pd.read_excel(tests_summary_file_name)
    for index_line, row in df_tests_summary.iterrows():
        if row['to_compute']==1:
            time_start = time.time()

            file_name = row['file_name'] + '.xlsx'
            file_path = Path('data',file_name)

            dataset_complet = extract_data_from_one_file(file_path)
            no_flow_pressure= extract_no_flow_pressure(dataset_complet,row['no_flow_time'])
            dataset_complet['pressure'] = dataset_complet['pressure'] - no_flow_pressure
            dataset_steady_unsorted  = extract_steady_data(dataset_complet ,
                                                  row['type_seq'] ,
                                                  row['start_seq'])
            dataset_steady           = dataset_steady_unsorted.sort_values(by=['volumetric_flows'])
            permeability    = compute_permeability(dataset_steady)
            
            all_monolith_names.append(row['monolith_name'])
            all_dataset_steady.append(dataset_steady)
            all_permeabilities.append(permeability)

            print(file_name)
            print("Permeability [m^2]: " + str(permeability*1e0))
            time_end = time.time()
            print("STOP" + str(index_line) + ". Time: " + str(time_end-time_start) + " s")

    output_graphs(all_monolith_names,
                    all_dataset_steady,
                    all_permeabilities)

def main():
    time_start = time.time()
    handle_all_files()
    time_end   = time.time()
    print('Finished treatment. Elapsed time: '+ str(time_end-time_start) + ' s')

main()