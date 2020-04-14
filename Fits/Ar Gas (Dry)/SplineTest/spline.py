from refl1d.names import *
from numpy import *
# Load data and create a probe
probe = load4('R1_Ar.refl')
probe.pp.intensity.value = 0.4
probe.pp.sample_broadening.value = 0.01
probe.pp.theta_offset.value = 0

probe.mm.intensity = probe.pp.intensity
probe.mm.theta_offset = probe.pp.theta_offset
probe.mm.sample_broadening = probe.pp.sample_broadening

# Define Materials
Fe_rho = 8.024
Co_rho = 2.265
Fe2Co_rho = 6.04
Gd_rho = 0.4
Gd_irho = 3.3

# Enter initial values for sld in 10^-6 A^-2
Silicon = SLD(name="Silicon",rho=2.07)
SiOx = SLD(name="SiOx",rho=3.475)
Permalloy = SLD(name="Permalloy", rho=9.239) #, magnetism=Magnetism(rhoM=1.9420))
Platinum = SLD(name="Platinum", rho=6.4460)
Water = SLD(name="Water", rho=1.5)
Nafion = SLD(name="Nafion", rho=3.7050)
Air = SLD(name="Air", rho=0.00)

# slds.append(SLD(name='Silicon', rho=2.0710, irho=0.0000))
# slabs.append(slds[0](0.0000, 35.490, magnetism=Magnetism(rhoM=0.0000, thetaM=0.0000)))
# s.add( slabs[0])

# slds.append(SLD(name='SiOx', rho=2.1100, irho=0.0000))
# slabs.append(slds[1](35.100, 3.5590, magnetism=Magnetism(rhoM=0.0000, thetaM=0.0000)))
# s.add( slabs[1])

# slds.append(SLD(name='Permalloy', rho=9.2390, irho=0.0000))
# slabs.append(slds[2](108.00, 8.5220, magnetism=Magnetism(rhoM=1.9420, thetaM=270.00)))
# s.add( slabs[2])

# slds.append(SLD(name='Platinum', rho=6.4460, irho=0.0000))
# slabs.append(slds[3](48.250, 0.0000, magnetism=Magnetism(rhoM=0.0000, thetaM=0.0000)))
# s.add( slabs[3])

# slds.append(SLD(name='Water', rho=1.5000, irho=0.0000))
# slabs.append(slds[4](10.000, 0.0000, magnetism=Magnetism(rhoM=0.0000, thetaM=0.0000)))
# s.add( slabs[4])

# slds.append(SLD(name='Nafion', rho=3.7050, irho=0.0000))
# slabs.append(slds[5](286.60, 7.7020, magnetism=Magnetism(rhoM=0.0000, thetaM=0.0000)))
# s.add( slabs[5])

# slds.append(SLD(name='Air', rho=0.0000, irho=0.0000))
# slabs.append(slds[6](0.0000, 0.0000, magnetism=Magnetism(rhoM=0.0000, thetaM=0.0000)))
# s.add( slabs[6])


free_t = 300 # total thickness of freeform layer
# create a nuclear freeform object
N = 5

nuc = FreeLayer(thickness=free_t, below=Platinum, above=Air,
					z=numpy.linspace(0,1,N),
					rho=numpy.linspace(0,1,N),
					irho=numpy.linspace(0,1,N),
					name="nuclear"
					)
for i in range(0,N):
	nuc.rho[i].value = 3.705
	nuc.irho[i].value = 0.000

# Extra parameters
x = list(range(N))
y = list(range(N))

for i in range(0,N):
    x[i] = Parameter.default(0.33, limits=(0,1000),name= "x %s"%(i))
    y[i] = Parameter.default(0.33, limits=(0,1000),name= "y %s"%(i))

# DEFINE A LAYER STRUCTURE
# Each layer is defined as:
# material(thickness, roughness, Magnetism(rhoM,thetaM))
# thickness & roughness are in A
# rhoM is in 10^-6 A^-2
# thetaM is in degrees (270 is parallel to H)
#			0
sample=(Silicon(5000,35.490)
#			1
		|SiOx(35.1, 3.5590)
#			2
		|Permalloy(108, 8.5220, Magnetism(1.9420, 270))
#			3
		|Platinum(48.25, 0)
#			4
		|nuc
#			5
		|Air)

# CONSTRAINTS
for i in range(0,N):
    nuc.rho[i] = ((1-x[i])*((y[i]*Fe_rho)+((1-y[i])*Co_rho)))+(x[i]*Gd_rho)
    nuc.irho[i]= x[i]*Gd_irho
# DEFINE FITTING PARAMETERS
# Beam parameters
if 1:
    probe.pp.intensity.range(0.01,3)
if 0:
    probe.pp.theta_offset.range(-0.02,0.02)
if 1:
    probe.pp.sample_broadening.range(0,0.1)
# Si
if 1:
    sample[Silicon].interface.range(0,150)
# freeform layer
if 1:
    nuc.thickness.range(200,600)
if 1:
    for i in range(0,N):
        #nuc.rho[i].range(0,Fe_rho)
        #nuc.irho[i].range(0,Gd_irho)
        x[i].range(0,1)
        y[i].range(0,1)
        nuc.z[i].range(0,1)
        #mag.rhoM[i].range(0,7)

# PROBLEM DEFINITION
# step_interfaces = False corresponds to Nevot-Croce Approximation,
# True corresponds to direct calculation from the profile
# for the latter, microslabbing is defined by dz (in Angstroms)
M = Experiment(sample=sample, probe=probe, dz=1,step_interfaces=False)
problem = FitProblem(M)






























