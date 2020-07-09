#!/usr/bin/env python
# coding: utf-8

# Author: Brian P. Josey
# Date Created: 2020-06-09
# Date Modified: 2020-07-07
# Language: Python 3.7.7

from refl1d.names import *
from numpy import mod, exp, arange, linspace
import math

# === Data Files ===
# Load reflectivity file
probe = load4('R1_H92.refl', back_reflectivity=False)

# === Initialize Fit Values ===
# === Constants and Bulk Layers ===
# Constants
NAFION_SLD = 4.157
H2O_SLD = -0.5599
D2O_SLD = 6.3503

# Properties of thick layers
Silicon = SLD(name='Silicon', rho=2.071)
SiOx = SLD(name='SiOx', rho=3.469)
Permalloy = SLD(name='Permalloy', rho=9.429)
Platinum = SLD(name='Platinum', rho=6.349)
Nafion = SLD(name='Bulk Nafion', rho=NAFION_SLD)
Air	 = SLD(name='Air', rho=0.000)

# === Interfacial Layers ===
# Deuteration state
# True if water is D2O, False if H2O
DEUTERATED = False

WATER_SLD = D2O_SLD if DEUTERATED else H2O_SLD

# Nafion Fraction by Layer
NRL1_frac = Parameter(name='Nafion Fraction-NRL1', value=1.05)
WRL1_frac = Parameter(name='Nafion Fraction-WRL1', value=0.85)
NRL2_frac = Parameter(name='Nafion Fraction-NRL2', value=1.05)
WRL2_frac = Parameter(name='Nafion Fraction-WRL2', value=0.85)
grad_frac = Parameter(name='Nafion Fraction-Gradient', value=0.95)
bulk_frac = Parameter(name='Nafion Fraction-Bulk', value = 1.02)

# Interfacial Layer SLD
NRL1 = SLD(name='NRL1', rho=(NAFION_SLD + WATER_SLD) * NRL1_frac - WATER_SLD)
WRL1 = SLD(name='WRL1', rho=(NAFION_SLD + WATER_SLD) * WRL1_frac - WATER_SLD)
NRL2 = SLD(name='NRL2', rho=(NAFION_SLD + WATER_SLD) * NRL2_frac - WATER_SLD)
WRL2 = SLD(name='WRL1', rho=(NAFION_SLD + WATER_SLD) * WRL2_frac - WATER_SLD)
grad = SLD(name='Gradient', rho=(NAFION_SLD + WATER_SLD) * grad_frac - WATER_SLD)
bulk = SLD(name='Bulk', rho=(NAFION_SLD + WATER_SLD) * bulk_frac - WATER_SLD)

# Interfacial Layer Thicknesses
# TO-DO: Use Better Names
Pt_NRL1 = Parameter(name='Pt:NRL1', value=0.5)
NRL1_WRL1 = Parameter(name='NRL1:WRL1', value=0.2)
WRL1_NRL2 = Parameter(name='WRL1:NRL2', value=0.5)
NRL2_WRL2 = Parameter(name='NRL2:WRL2', value=0.2)
WRL2_Grad = Parameter(name='WRL2:Grad', value=0.2)
grad_bulk = Parameter(name='Grad:Nafion', value = 0.55)

NRL1_thickness = Parameter(name="NRL1 thickness",value=10.83)
WRL1_thickness = Parameter(name="WRL1 thickness",value=16.23)
NRL2_thickness = Parameter(name="NRL2 thickness",value=14.66)
WRL2_thickness = Parameter(name="WRL2 thickness",value=15.43)
grad_thickness = Parameter(name="Grad thickness",value=139.60)

# TO-DO: Move this constant UP
PT_THICKNESS = 50

# Effective thickness of each layer
Teff1 = Parameter (name="Effective T1", value=1)
Teff1 = pow( (pow(PT_THICKNESS,-4.0) + pow(NRL1_thickness,-4.0) ),-0.25) 

Teff2 = Parameter (name="Effective T2", value=1)
Teff2 = pow( (pow(NRL1_thickness,-4.0) + pow(WRL1_thickness,-4.0) ),-0.25) 

Teff3 = Parameter (name="Effective T3", value=1)
Teff3 = pow( (pow(WRL1_thickness,-4.0) + pow(NRL2_thickness,-4.0) ),-0.25) 

Teff4 = Parameter (name="Effective T4", value=1)
Teff4 = pow( (pow(NRL2_thickness,-4.0) + pow(WRL2_thickness,-4.0) ),-0.25) 

# Interfacial roughness
Pt_int= Pt_NRL1*Teff1
NRL1_int=NRL1_WRL1*Teff2 
WRL1_int=WRL1_NRL2*Teff3 
NRL2_int=NRL2_WRL2*Teff4 

WRL2_int=WRL2_Grad*WRL2_thickness
grad_int=grad_bulk*grad_thickness

sample = (Silicon(5000,44.84)
        |SiOx(30.04, 2.96)
        |Permalloy(107.5, 9.105, magnetism=Magnetism(rhoM=1.9420, thetaM=270.00))
		|Platinum(50.0,3.8)
		|NRL1(NRL1_thickness,NRL1_int)
		|WRL1(WRL1_thickness,WRL1_int)
		|NRL2(NRL2_thickness,NRL2_int)
		|WRL2(WRL2_thickness,WRL2_int)
		|grad(grad_thickness,grad_int)
		|Nafion(300,8.5)
        |Air)

# === Parameters ===
# Adjust the fit range of the parameters below.

# Instrument parameters
probe.pp.intensity.range(0.9, 1.1)
probe.pp.intensity.value = 1.0
probe.mm.intensity.range(0.9, 1.1)
probe.mm.intensity.value = 1.0


background_pp = Parameter(name='Background PP', value = 6.03e-8)
background_mm = Parameter(name='Background MM', value = 6.03e-8)

background_pp.range(0,10e-5)
background_mm.range(0,10e-5)


probe.pp.background = background_pp
probe.mm.background = background_mm

# Fraction of Nafion in each layer
NRL1_frac.range(0.7,1.3)
WRL1_frac.range(0.0,1.2)
NRL2_frac.range(0.7,1.3)
WRL2_frac.range(0.0,1.2)
grad_frac.range(0.7,1.2)
bulk_frac.range(0.7,1.1)

# Thickness of Interfacial Layers
NRL1_thickness.range(4,30)
WRL1_thickness.range(4,30)
NRL2_thickness.range(4,30)
WRL2_thickness.range(4,30)
grad_thickness.range(10,350)

# Layer nSLDs
#sample[Silicon].material.rho.range(1.071, 3.071)
sample[SiOx].material.rho.range(0.700, 5.000)
sample[Permalloy].material.rho.range(8.239, 10.239)
sample[Platinum].material.rho.range(5.349, 7.349)
sample[Nafion].material.rho.range(2.705, 4.705)
#sample[Air].material.rho.range(-1.000, 1.000)

# Layer magnetic SLD (RHOM)
#sample[Silicon].magnetism.rhoM.range(-1.0000, 1.0000)
#sample[SiOx].magnetism.rhoM.range(-1.0000, 1.0000)
sample[Permalloy].magnetism.rhoM.range(0.94200, 2.9420)
#sample[Platinum].magnetism.rhoM.range(-1.0000, 1.0000)
#sample[Air].magnetism.rhoM.range(-1.0000, 1.0000)

# Layer Thicknesses
#sample[Silicon].thickness.range(0.0000, 100.00)
sample[SiOx].thickness.range(25, 100.0)
sample[Permalloy].thickness.range(98, 115)
sample[Platinum].thickness.range(30, 70)
sample[Nafion].thickness.range(200, 400)
#sample[Air].thickness.range(0.0000, 100.00)

# Layer Roughnesses
sample[Silicon].interface.range(30, 75)
sample[SiOx].interface.range(0.0000, 20)
sample[Permalloy].interface.range(0.0000, 20)
sample[Platinum].interface.range(0.0000, 10.000)
sample[Nafion].interface.range(0, 20)
#sample[Air].interface.range(0.0000, 17.702)

# UPDATED LAYER ROUGHNESSES FOLLOWING JDScript 211-217
Pt_NRL1.range(0.0, 0.55)
NRL1_WRL1.range(0.0, 0.55)
WRL1_NRL2.range(0.0, 0.55)
NRL2_WRL2.range(0.0, 0.55)
WRL2_Grad.range(0.0, 0.55)
grad_bulk.range(0.0, 0.55)

#======EXPERIMENT PARAMETERS=======
theta_offset=Parameter(name='Theta_Offset',value=0.0)
#theta_offset.range(-0.01,0.01)
#probe.theta_offset=theta_offset
#--Uncomment the above two lines if you want to fit theta-offset. Not recommended for NR. (XRR OK)

#step=True #Calculation of reflectivity from actual data profile with micro-slab interfaces (planar).
#step=False #Calculation of reflectivity uses Parratt formalism for INTERFACIAL ROUGHNESS, by Nevot-Croce. 
step = False

M=Experiment(probe=probe,sample=sample)
problem=FitProblem(M)