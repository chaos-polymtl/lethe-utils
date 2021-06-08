# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 12:01:59 2020

@author: ghaza
"""

import math
import numpy as np
import pandas as pd
from numpy import linalg as LA
from sympy.abc import x, y, z, X, Y, Z, t, r
from sympy.solvers import solve
from scipy.optimize import minimize
import sympy
from scipy.optimize import fsolve
import time


start_time = time.time()


global position_particle

n_file = ["1", "2", "3", "4", "8", "9", "14", "15", "16", "17"]

#The function "find_h_rho" calculate the rho and h for all the positions

def find_h_rho(position_detector_face,position_detector_middle):

    detector_orientation=[]
    V_rho=[]
    V_h=[]

    #This "for" loop calculates the orientation of the detector using two points on the detector axis (e'z)
    for i in range (0,3):
        detector_orientation.append(position_detector_face[i]-position_detector_middle[i])

    detector_orientation= detector_orientation/LA.norm(detector_orientation)


    #Loop over all the positions to calculate rho and h  

    for j in range (0,len(position_particle)):

        #Distance vector is a vector from a point on the detector face to the particle position (Xdp)
        distance_vector=[]
        for i in range (0,3):
            distance_vector.append(position_particle[j][i]-position_detector_face[i])

        #Projection of the distance vector on the detector axis which is parallel to the z' axis
        #k is (z'p)

        K=np.dot(distance_vector,detector_orientation)
        h=np.fabs(K)
        V_h.append(h)

        # to calculate pho use equation 29

        rho=np.fabs(LA.norm(h*detector_orientation-distance_vector))
        V_rho.append(rho)



    return V_rho,V_h

#rho and h as output of this function will be used in solid angle calculation   


"""
"""

def solid_angle (position_detector_face,
                 position_detector_middle):
    """
    The following constants are extracted from this article: "Optimization of detector positioning in the radioactive particle tracking technique".
    """
    r_cristal=0.0381
    l_cristal=0.0762
    r_reactor=0.1
    mu_d=21.477
    mu_r=10
    Monte_Carlo_iteration=10000

    #Psi is calculated based on Equation 3 in the document, which is the detector efficiency

    V_Psi=[]

    #Call the function that calculates rho and h for each position

    V_rho,V_h=find_h_rho(position_detector_face,position_detector_middle)

    #Loop over all the position to do the Monte Carlo calculation for each mesh point

    for j in range (0,len(position_particle)):


        """
        The following vector starting with (V_...) store related parameter for each iteration
        of the Monte Carlo for a specific position
        """
        V_depth_detector=[]

        Psi=0

        #Start the Monte Carlo simulation

        for i in range (Monte_Carlo_iteration):

            """
            First "if" condition defines that the particle position is in the detector's face 
            or it can view the detector from both lateral and top side.
            """
            if V_rho[j] < r_cristal:
                tetha_max = np.arctan((r_cristal+V_rho[j])/V_h[j])
                tetha_cri = np.arctan((r_cristal-V_rho[j])/V_h[j])
                tetha_min = 0.0

                #Here the np.random generate the random number for theta calculation

                tetha=np.arccos(math.cos(tetha_min)- np.random.random_sample() *
                                (math.cos(tetha_min)-math.cos(tetha_max)))


                W_tetha=((math.cos(tetha_min) - math.cos(tetha_max))/2)


                if tetha < tetha_cri :

                    alpha_max = math.pi
                    alpha=alpha_max*(2* np.random.random_sample()-1)
                    W_alpha=1

                    OA = V_rho[j] * math.cos(alpha) + pow(pow(r_cristal,2) -
                                                          (pow(V_rho[j],2)*pow(math.sin(alpha),2)),0.5)
                else:
                    alpha_max = math.acos((pow(V_rho[j], 2) + pow((V_h[j] * math.tan(tetha)), 2) -
                                           pow(r_cristal, 2)) / (2 * V_h[j] * V_rho[j] * math.tan(tetha)))

                    alpha=alpha_max*(2* np.random.random_sample()-1)

                    W_alpha=(alpha_max/math.pi)
                    OA = V_rho[j] * math.cos(alpha) + pow(pow(r_cristal,2) -
                                                          (pow(V_rho[j],2)*pow(math.sin(alpha),2)),0.5)

                """
                depth_detector is the ray's path length inside the detector which is 
                calculated using a function out side of the "solid angle", path_length_detector
                """
                depth_detector=path_length_detector_one(OA,V_h[j],V_rho[j],r_cristal,l_cristal,alpha,tetha)
                V_depth_detector.append(depth_detector)

                """
                depth is the ray's path length inside the reactor which is calculated using a function
                out side of the "solid angle", path_length_reactor
                """
                depth=path_length_reactor(alpha,tetha,r_reactor,position_detector_face,
                                          position_detector_middle,position_particle[j])



                Psi+=W_alpha*W_tetha*(1-np.exp(-1*mu_d*depth_detector))*np.exp(-1*mu_r*depth)
                #Psi+=W_alpha*W_tetha*(1-np.exp(-1*mu_d*depth_detector))

            else:
                alpha_max = np.arcsin(r_cristal/V_rho[j])
                alpha=alpha_max*(2*np.random.random_sample()-1)
                W_alpha=(alpha_max/math.pi)

                OB = V_rho[j] * math.cos(alpha) - pow(pow(r_cristal,2) -
                                                      (pow(V_rho[j],2)*pow(math.sin(alpha),2)),0.5)



                OA = V_rho[j] * math.cos(alpha) + pow(pow(r_cristal,2) -
                                                      (pow(V_rho[j],2)*pow(math.sin(alpha),2)),0.5)


                tetha_min = np.arctan(OB/(V_h[j]+l_cristal))
                tetha_max = np.arctan(OA/V_h[j])
                tetha_cri = np.arctan(OB/V_h[j])
                tetha = np.arccos(math.cos(tetha_min) - np.random.random_sample() * (math.cos(tetha_min)- math.cos(tetha_max)))

                W_tetha=((math.cos(tetha_min) - math.cos(tetha_max))/2)
                depth_detector=path_length_detector_two(OA,OB,V_rho[j],r_cristal
                                                        ,l_cristal,alpha,tetha,V_h[j],tetha_cri)
                V_depth_detector.append(depth_detector)



                depth=path_length_reactor(alpha,tetha,r_reactor,position_detector_face,
                                          position_detector_middle,position_particle[j])





                Psi+=W_alpha*W_tetha*(1-np.exp(-1*mu_d*depth_detector))*np.exp(-1*mu_r*depth)
                #Psi+=W_alpha*W_tetha*(1-np.exp(-1*mu_d*depth_detector))


        Psi=Psi/Monte_Carlo_iteration
        V_Psi.append(Psi)


    print("Epsilons : ",V_Psi)

    return (V_Psi)


"""        
"""

def path_length_detector_one(OA,h,rho,r_cristal,l_cristal,alpha,tetha):
    #Point source viewing only the top of the detector
    tetha_one= np.arctan(OA/(h+l_cristal))
    tetha_two= np.arctan(OA/h)
    if tetha < tetha_one:
        depth_detector=l_cristal/np.cos(tetha)
    elif tetha>tetha_one and tetha<tetha_two:
        depth_detector=(OA/np.sin(tetha))-(h/np.cos(tetha))

    return depth_detector

"""
"""

def path_length_detector_two(OA,OB,rho,r_cristal,l_cristal,alpha,tetha,h,tetha_cri):
    #Point source viewing the top and the lateral surface of the detector
    if tetha<tetha_cri:
        if (h+l_cristal)*np.tan(tetha)<OA:
            depth_detector=((h+l_cristal)/np.cos(tetha))-OB/np.sin(tetha)
        else:
            depth_detector=(OA-OB)/np.sin(tetha)
    else:
        if (h+l_cristal)*np.tan(tetha)<OA:
            depth_detector=l_cristal/np.cos(tetha)
        else:
            depth_detector=(OA/np.sin(tetha))-(h/np.cos(tetha))

    return depth_detector


"""
"""

def path_length_reactor(alpha,tetha,r_reactor,position_detector_face,
                        position_detector_middle,position_particle):


    detector_orientation=[]
    newOrigin=[]
    position_particle_translation=[]
    intersection_point=[]
    intersection_point_1=[]
    intersection_point_2=[]
    distance_vector_1=[]
    distance_vector_2=[]
    depth_vector=[]
    distance_vector=[]

    for i in range (0,3):
        detector_orientation.append(position_detector_face[i]-position_detector_middle[i])


    detector_orientation= detector_orientation/LA.norm(detector_orientation)


    for i in range (0,3):
        distance_vector.append(position_particle[i]-position_detector_face[i])


    K=np.dot(distance_vector,detector_orientation)
    h=np.fabs(K)
    #M is Equation 63 in document
    M=h*detector_orientation
    xprime=K*detector_orientation-distance_vector
    exprime=xprime/LA.norm(xprime)
    eyprime=np.cross(detector_orientation,exprime)

    #This for loop calculate the origin of particle-detector coordinate system(Equation 62)
    for i in range (0,3):

        newOrigin.append(position_particle[i]-M[i])

    #This for loop calculate the new position of particle just because of tanslation (Equation 59 to 61)
    for i in range (0,3):
        position_particle_translation.append(position_particle[i]-newOrigin[i])

    #A is the transformation matrix, on each position we apply rotation by the matrix (A) after the translation
    A=np.array((exprime,eyprime,detector_orientation))
    A_inv=np.linalg.inv(A)

    B=np.array([position_particle_translation[0],position_particle_translation[1]
                   ,position_particle_translation[2]])

    #Position of the particle in new origin(Eq 64 in document)
    particle_new=np.matmul(A,B)

    #X,Y,Z is the line equation (from particle position to the detector which has intersaction with the vessel)(Equatin 46 to 48)
    X=particle_new[0]+t*math.sin(tetha)*math.cos(alpha)
    Y=particle_new[1]+t*math.sin(alpha)*math.sin(tetha)
    Z=particle_new[2]+t*math.cos(math.pi-tetha)

    B=[X,Y,Z]


    #From here we calculate equation 66 to 68
    x=newOrigin[0]
    y=newOrigin[1]
    z=newOrigin[2]

    #This for loop calculates the parameters x,y,z (old coordinate) based on X,Y,Z (new coordinate)
    for i in range (0,3):
        x+=A_inv[0][i]*B[i]
        y+=A_inv[1][i]*B[i]
        z+=A_inv[2][i]*B[i]

    intersection_point.append(x)
    intersection_point.append(y)
    intersection_point.append(z)

    #Solve the parametric equation of the circle to find "t"
    func=pow(x,2)+pow(y,2)-pow(r_reactor,2)
    F=sympy.lambdify(t,func)
    M=fsolve(F,(-1,1))

    #print("t : ",M)

    #Substituting parameter t
    for i in range(0,3):

        point_1=intersection_point[i].subs(t,M[0])
        intersection_point_1.append(point_1)
        point_2=intersection_point[i].subs(t,M[1])
        intersection_point_2.append(point_2)

    """
    As the line can have two intersection with the circle we choose the intersection point which is closer to the detector
    """
    for i in range(0,3):
        distance_vector_1.append(position_detector_face[i]-intersection_point_1[i])
        distance_vector_2.append(position_detector_face[i]-intersection_point_2[i])


    #Convert sympy float to normal float type
    distance_vector_1=str(distance_vector_1)
    distance_vector_1=eval(distance_vector_1)
    distance_vector_2=str(distance_vector_2)
    distance_vector_2=eval(distance_vector_2)

    distance_1=np.fabs(LA.norm(distance_vector_1))
    distance_2=np.fabs(LA.norm(distance_vector_2))




    if distance_2>distance_1:
        for i in range(0,3):
            depth_vector.append(position_particle[i]-intersection_point_1[i])
    else:
        for i in range(0,3):
            depth_vector.append(position_particle[i]-intersection_point_2[i])

    depth_vector=str(depth_vector)
    depth_vector=eval(depth_vector)
    depth=np.fabs(LA.norm(depth_vector))



    return depth

"""
"""
for n in n_file:
    #Open the file the that includes particle positions (Mesh reading)

    position_particle= np.loadtxt("./Test" + n + ".txt")

    def count (position_detector_face,position_detector_middle):
        T=1
        nui=2
        R=2e6
        tui=1e-5
        phi=0.4
        V_count=[]
        V_Psi=solid_angle(position_detector_face,position_detector_middle)


        for i in range(0,len(position_particle)):
            V_count.append((T*nui*R*phi*V_Psi[i])/(1+(tui*nui*R*phi*V_Psi[i])))

        print("File : Test" + n + ".txt")
        print(V_count)

        data = {"particle_positions_x" : position_particle[:,0], "particle_positions_y" :  position_particle[:,1],
                "particle_positions_z" : position_particle[:,2], "detector_id" : np.zeros(len(position_particle), dtype=int),
                "counts" : V_count}
        df = pd.DataFrame(data)
        df.to_csv("/home/audrey/work/rpt_python/data/Test" + n + ".csv", index=False)

        return(V_count)


    count([0.15,0,0.17],[0.17,0,0.17])

print("--- %s seconds ---" % (time.time() - start_time))
#count([0.01,0.17,0.1],[0.01,0.19,0.1])
#solid_angle([0.15,0,0.3],[0.17,0,0.3])
#find_h_rho([0.15,0,0.17],[0.17,0,0.17])

