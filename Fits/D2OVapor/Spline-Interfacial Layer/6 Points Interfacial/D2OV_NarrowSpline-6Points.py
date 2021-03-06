from refl1d.names import *
from numpy import *

# Load data and create a probe
probe = load4('R1_D2OVap.refl')
probe.pp.intensity.value = 0.4
probe.pp.sample_broadening.value = 0.01
probe.pp.theta_offset.value = 0

#probe.mm.intensity = probe.pp.intensity
#probe.mm.theta_offset = probe.pp.theta_offset
#probe.mm.sample_broadening = probe.pp.sample_broadening

# Define material SLDs in 10^-6 A^-2
WATERRHO = 6.331       # H2O, rho_D2O =   -0.5609
NAFIONRHO = 4.058		 # Nominally 3.705
NAFION_IRHO = 0.000

# Enter initial values for SLDs in 10^-6 A^-2
Silicon = SLD(name = "Silicon", rho = 2.148)
SiOx = SLD(name = "SiOx", rho = 3.000)
Permalloy = SLD(name = "Permalloy", rho = 9.429)
Platinum = SLD(name = "Platinum", rho = 6.349)
Water = SLD (name = "Water", rho = 1.5)
Nafion = SLD(name = "Nafion", rho = 3.705)
Air = SLD(name = "Air", rho = 0.000)

# Setup and Initialize Spline
FREE_THICKNESS = 100        # Freeform layer thickness (A)
NUM_POINTS = 6              # Number of control points

nuclear_spline = FreeLayer(thickness = FREE_THICKNESS,
                        below = Platinum,
                        above = Nafion,
                        z = numpy.linspace(0,1,NUM_POINTS),
                        rho = numpy.linspace(0,1,NUM_POINTS),
                        irho = numpy.linspace(0,1,NUM_POINTS),
                        name = "Interfacial"
                        )

# Initialize nSLDs
for point in range(0, NUM_POINTS):
    nuclear_spline.rho[point].value = 3.705
    nuclear_spline.irho[point].value = 0.000

# Extra parameters
water_frac = list(range(NUM_POINTS))

for point in range(0, NUM_POINTS):
    water_frac[point] = Parameter.default(0.33, limits=(0, 1000), name = "Water fraction %s"%(point))

# DEFINE A LAYER STRUCTURE
# Each layer is defined as:
# material (thickness, roughness, Magnetism(rhoM, thetaM))
# thicknesses & roughnesses are in A
# rhoM is in 10^-6 A^-2
# thetaM is in degrees where 270 is parallel to H

#           0
sample=(Silicon(5000,44.84)
#           1
        |SiOx(30.04, 2.96)
#           2
        |Permalloy(107.5, 9.105, magnetism=Magnetism(rhoM=1.9420, thetaM=270.00))
#           3
        |Platinum(50.28, 0.2639)
#           4
        |nuclear_spline
#           5
		|Nafion(280, 8.5)
#			6
        |Air)

for point in range(0, NUM_POINTS):
    nuclear_spline.rho[point] = (((1 - water_frac[point]) * NAFIONRHO) + (water_frac[point] * WATERRHO))

# === Fit parameters ===
# Comment out parameters not fitted
# "range" specifies a fitting range in terms of min/max value
# "pmp" specifices fitting range in terms of +/-  %
# "pm" specifies fitting range in terms of +/- value

# Probe
probe.pp.intensity.range(0.9,1.1)
probe.pp.intensity.value = 1.0
probe.mm.intensity.range(0.9,1.1)
probe.mm.intensity.value = 1.0
#probe.pp.sample_broadening.range(0,0.1)
# probe.pp.theta_offset.range(-0.02,0.02)

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
sample[SiOx].thickness.range(25, 55)
sample[Permalloy].thickness.range(98, 115)
sample[Platinum].thickness.range(30, 70)
sample[Nafion].thickness.range(200, 400)
#sample[Air].thickness.range(0.0000, 100.00)

# LAYER ROUGHNESSES
sample[Silicon].interface.range(30, 75)
sample[SiOx].interface.range(0.0000, 20)
sample[Permalloy].interface.range(0.0000, 20)
sample[Platinum].interface.range(0.0000, 10.000)
sample[Nafion].interface.range(0, 20)
#sample[Air].interface.range(0.0000, 17.702)

# freeform layer
if 1:
    nuclear_spline.thickness.range(5, 150)
if 1:
    for i in range(0,NUM_POINTS):
        water_frac[i].range(0,1)
        nuclear_spline.z[i].range(0,1)


# PROBLEM DEFINITION
# From Brian Kirby:
# step_interfaces = False corresponds to Nevot-Croce Approximation, (Useful for magnetic problems)
# True corresponds to direct calculation from the profile
# for the latter, microslabbing is defined by dz (in Angstroms)
M = Experiment(sample=sample, probe=probe, dz=1,step_interfaces=False)
problem = FitProblem(M)