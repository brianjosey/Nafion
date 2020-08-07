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
probe = load4('R1H92.refl', back_reflectivity=False)

# === Initialize Fit Values ===
# === Constants and Bulk Layers ===
# Constants
NAFION_SLD = 4.157
H2O_SLD = -0.5599
D2O_SLD = 6.3503

# Properties of thick layers
Silicon = SLD(name='Silicon', rho=2.071)
SiOx = SLD(name='SiOx', rho=2.548)
Permalloy = SLD(name='Permalloy', rho=8.829)
Platinum = SLD(name='Platinum', rho=6.5)
Nafion = SLD(name='Bulk Nafion', rho=NAFION_SLD)
Air	 = SLD(name='Air', rho=0.000)

# === Interfacial Layers ===
# Deuteration state
# True if water is D2O, False if H2O
DEUTERATED = False

WATER_SLD = D2O_SLD if DEUTERATED else H2O_SLD

# Nafion Fraction by Layer
# WRL1_frac = Parameter(name='Nafion Fraction-WRL1', value=0.85)
# NRL1_frac = Parameter(name='Nafion Fraction-NRL1', value=0.70)
# WRL2_frac = Parameter(name='Nafion Fraction-WRL2', value=0.82)
# NRL2_frac = Parameter(name='Nafion Fraction-NRL2', value=0.51)
# grad_frac = Parameter(name='Nafion Fraction-Gradient', value=0.763)
# bulk_frac = Parameter(name='Nafion Fraction-Bulk', value = 1.02)

# Interfacial Layer SLD
WRL1 = SLD(name='WRL1', rho=3.30)
NRL1 = SLD(name='NRL1', rho=2.50)
WRL2 = SLD(name='WRL2', rho=3.10)
NRL2 = SLD(name='NRL2', rho=2.85)
grad = SLD(name='Gradient', rho=3.15)
# bulk = SLD(name='Bulk', rho=NAFION_SLD)

# Interfacial Layer Thicknesses
# TO-DO: Use Better Names--These don't match Python best practices: pt_wrl1 not CamelCase!
Pt_WRL1 = Parameter(name='Pt:WRL1', value=0.5)
WRL1_NRL1 = Parameter(name='WRL1:NRL1', value=0.028)
NRL1_WRL2 = Parameter(name='NRL1:WRL2', value=0.01)
WRL2_NRL2 = Parameter(name='WRL2:NRL2', value=0.2124)
NRL2_Grad = Parameter(name='NRL2:Grad', value=0.5471)
grad_bulk = Parameter(name='Grad:Nafion', value = 0.7636)

WRL1_thickness = Parameter(name="WRL1 thickness",value=33.45)
NRL1_thickness = Parameter(name="NRL1 thickness",value=15.14)
WRL2_thickness = Parameter(name="WRL2 thickness",value=11.52)
NRL2_thickness = Parameter(name="NRL2 thickness",value=28.51)
grad_thickness = Parameter(name="Grad thickness",value=33.72)

# TO-DO: Move this constant UP
PT_THICKNESS = 50
Nafion_thickness = 200

# Effective thickness of each layer
Teff1 = Parameter (name="Effective T1", value=1)
Teff1 = pow( (pow(PT_THICKNESS,-4.0) + pow(WRL1_thickness,-4.0) ),-0.25) 

Teff2 = Parameter (name="Effective T2", value=1)
Teff2 = pow( (pow(WRL1_thickness,-4.0) + pow(NRL1_thickness,-4.0) ),-0.25) 

Teff3 = Parameter (name="Effective T3", value=1)
Teff3 = pow( (pow(NRL1_thickness,-4.0) + pow(WRL2_thickness,-4.0) ),-0.25) 

Teff4 = Parameter (name="Effective T4", value=1)
Teff4 = pow( (pow(WRL2_thickness,-4.0) + pow(NRL2_thickness,-4.0) ),-0.25)

Teff5 = Parameter (name="Effective T5", value=1)
Teff5 = pow( (pow(NRL2_thickness,-4.0) + pow(grad_thickness,-4.0) ),-0.25)

Teff6 = Parameter (name="Effective T6", value=1)
Teff6 = pow( (pow(grad_thickness,-4.0) + pow(Nafion_thickness,-4.0) ),-0.25) 

# Interfacial roughness
Pt_int= Pt_WRL1*Teff1
WRL1_int=WRL1_NRL1*Teff2 
NRL1_int=NRL1_WRL2*Teff3 
WRL2_int=WRL2_NRL2*Teff4
NRL2_int=NRL2_Grad*Teff5
grad_int=grad_bulk*Teff6 

# NRL2_int=NRL2_Grad*NRL2_thickness
# grad_int=grad_bulk*grad_thickness

sample = (Silicon(5000,22.58)
        |SiOx(153.0, 3.279)
        |Permalloy(108.2, 9.604, magnetism=Magnetism(rhoM=1.642, thetaM=270.00))
		|Platinum(48.1,0.1)
		|WRL1(WRL1_thickness,WRL1_int)
		|NRL1(NRL1_thickness,NRL1_int)
		|WRL2(WRL2_thickness,WRL2_int)
		|NRL2(NRL2_thickness,NRL2_int)
		|grad(grad_thickness,grad_int)
		|Nafion(203.4,12.87)
        |Air)

# === Parameters ===
# Adjust the fit range of the parameters below.

# Instrument parameters
probe.pp.intensity.range(0.9, 1.1)
probe.pp.intensity.value = 0.9487
probe.mm.intensity.range(0.9, 1.1)
probe.mm.intensity.value = 0.9954


background_pp = Parameter(name='Background PP', value = 1.399e-7)
background_mm = Parameter(name='Background MM', value = 4.582e-7)

background_pp.range(0,10e-5)
background_mm.range(0,10e-5)


probe.pp.background = background_pp
probe.mm.background = background_mm

# Fraction of Nafion in each layer
# WRL1_frac.range(0.0,1.2)
# NRL1_frac.range(0.5,1.3)
# WRL2_frac.range(0.0,1.2)
# NRL2_frac.range(0.5,1.3)
# grad_frac.range(0.5,1.2)
# bulk_frac.range(0.5,1.1)

# Thickness of Interfacial Layers
WRL1_thickness.range(4,40)
NRL1_thickness.range(4,40)
WRL2_thickness.range(4,40)
NRL2_thickness.range(4,40)
grad_thickness.range(4,40)


sample[WRL1].material.rho.range(0.00, 4.5)
sample[NRL1].material.rho.range(0.00, 4.5)
sample[WRL2].material.rho.range(0.00, 4.5)
sample[NRL2].material.rho.range(0.00, 4.5)
sample[grad].material.rho.range(0.00, 4.5)
# sample[bulk].material.rho.range(0.00, 4.5)

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
sample[SiOx].thickness.range(25, 200)
sample[Permalloy].thickness.range(98, 115)
sample[Platinum].thickness.range(30, 70)
sample[Nafion].thickness.range(175, 400)
#sample[Air].thickness.range(0.0000, 100.00)

# Layer Roughnesses
sample[Silicon].interface.range(10, 100)
sample[SiOx].interface.range(0.0000, 20)
sample[Permalloy].interface.range(0.0000, 20)
sample[Platinum].interface.range(0.0000, 10.000)
sample[Nafion].interface.range(0, 20)
#sample[Air].interface.range(0.0000, 17.702)

# UPDATED LAYER ROUGHNESSES FOLLOWING JDScript 211-217
Pt_WRL1.range(0.0, 0.55)
WRL1_NRL1.range(0.0, 0.55)
NRL1_WRL2.range(0.0, 0.55)
WRL2_NRL2.range(0.0, 0.55)
NRL2_Grad.range(0.0, 0.55)
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