#!/usr/bin/env python
# coding: utf-8
from refl1d.names import *
from numpy import mod, exp, arange, linspace
import math

# Set up the problem for the fit
Probe.view = 'log' #Scale options for data viewing: linear, log, fresnel, Q**4
data_file_n='R1_Ar.refl' #Enter filename for .refl data you want to model.

probe=load4('R1_Ar.refl',back_reflectivity=False)

Silicon = SLD(name = "Silicon", rho = 2.148)
SiOx = SLD(name = "SiOx", rho = 3.000)
Permalloy = SLD(name = "Permalloy", rho = 9.429)
Platinum = SLD(name = "Platinum", rho = 6.349)
Water = SLD (name = "Water", rho = 1.5)
Nafion = SLD(name = "Nafion", rho = 3.705)
Air = SLD(name = "Air", rho = 0.000)


#===Layer Thicknesses (z)===
Platinum_Thickness=Parameter(name="Platinum thickness", value=50.0)
Water_Thickness=Parameter(name="Water thickness", value=10.0)
Nafion_Thickness=Parameter(name="Nafion thickness", value=280.0)

# Set the initial value for the width of the thicknesses between Platinum/Water and Water/Nafion
Platinum_FracWidth=Parameter(name="Platinum:Water(W/T)",value=0.30)
Water_FracWidth=Parameter(name="Water:Nafion(W/T)",value=0.30)

# Calculate the effective thickness as 'resistors in parallel'
T_eff0=Parameter(name="Effective Tickness Platinum:Water",value=20.0)
T_eff0=pow((pow(Platinum_Thickness,-4.0)+pow(Water_Thickness,-4.0)),-0.25)

T_eff1=Parameter(name="Effective Thickness Water:Nafion",value=50.0)
T_eff1=pow((pow(Water_Thickness,-4.0)+pow(Nafion_Thickness,-4.0)),-0.25)

# Set the fitting range for the width of the thicknesses between layers
Platinum_FracWidth.range(0.0,0.55)
Water_FracWidth.range(0.0,0.55)

Platinum_Water=(Platinum_FracWidth)*(T_eff0)
Water_Nafion=(Water_FracWidth)*(T_eff1)

# Initialize the sample
sample = (Silicon(5000,44.84)
#			1
        |SiOx(30.04, 2.96)
#           2
        |Permalloy(107.5, 9.105, magnetism=Magnetism(rhoM=1.9420, thetaM=270.00))
#           3
		|Platinum(Platinum_Thickness,Platinum_Water)

		|Water(Water_Thickness,Water_Nafion)

		|Nafion(Nafion_Thickness,8.5)
        
        |Air)


# FITTING PARAMETERS
# Ranges for instrument parameters

probe.pp.intensity.range(0.9,1.1)
probe.pp.intensity.value = 1.0
probe.mm.intensity.range(0.9,1.1)
probe.mm.intensity.value = 1.0

# LAYER RHOs
#sample[Silicon].material.rho.range(1.0710, 3.0710)
sample[SiOx].material.rho.range(0.700, 5.000)
sample[Permalloy].material.rho.range(8.2390, 10.239)
sample[Platinum].material.rho.range(5.4460, 7.4460)
sample[Nafion].material.rho.range(2.7050, 4.7050)
#sample[Air].material.rho.range(-1.0000, 1.0000)

# LAYER RHOMs
#sample[Silicon].magnetism.rhoM.range(-1.0000, 1.0000)
#sample[SiOx].magnetism.rhoM.range(-1.0000, 1.0000)
sample[Permalloy].magnetism.rhoM.range(0.94200, 2.9420)
#sample[Platinum].magnetism.rhoM.range(-1.0000, 1.0000)
#sample[Air].magnetism.rhoM.range(-1.0000, 1.0000)

# LAYER THICKNESSES
#sample[Silicon].thickness.range(0.0000, 100.00)
sample[SiOx].thickness.range(25, 45)
sample[Permalloy].thickness.range(98, 115)
sample[Platinum].thickness.range(30, 70)
sample[Nafion].thickness.range(200, 400)
#sample[Air].thickness.range(0.0000, 100.00)

# LAYER ROUGHNESSES
sample[Silicon].interface.range(30, 50)
sample[SiOx].interface.range(0.0000, 20)
sample[Permalloy].interface.range(0.0000, 20)
sample[Platinum].interface.range(0.0000, 10.000)
sample[Nafion].interface.range(0, 20)
#sample[Air].interface.range(0.0000, 17.702)


#======EXPERIMENT PARAMETERS=======
theta_offset=Parameter(name='Theta_Offset',value=0.0)
#theta_offset.range(-0.01,0.01)
#probe.theta_offset=theta_offset
#--Uncomment the above two lines if you want to fit theta-offset. Not recommended for NR. (XRR OK)

#step=True #Calculation of reflectivity from actual data profile with micro-slab interfaces (planar).
#step=False #Calculation of reflectivity uses Parratt formalism for INTERFACIAL ROUGHNESS, by Nevot-Croce. 
step = False

intensity=Parameter(name='Intensity',value=0.9509)
intensity.range(0.9,1.5)
probe.intensity=intensity

background=Parameter(name='Background',value=1e-10)
background.range(0,10e-7)
probe.background=background

M=Experiment(probe=probe,sample=sample)
problem=FitProblem(M)