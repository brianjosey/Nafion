
from refl1d.names import *
from copy import copy

# === Data files ===
# old-style loader for reflpak data:
# instrument template, load s1, s2, sample_width, and sample broadening
# sample_broadening = FWHM - 0.5*(s1+s2)/(d1-d2)
# for NG1, d1 = 1905 mm, d2 = 355.6 mm
# instrument = NCNR.NG1(Tlo=0.5, slits_at_Tlo=0.2, slits_below=0.2) 

# probe object combines instrument and data
probe = load4('R1H92.refl', back_reflectivity=False)
#xs_probes = [Probe(T=numpy.linspace(0.23020, 9.6000, 251), L=5.0000) for xs in range(4)]
#probe = PolarizedNeutronProbe(xs_probes, Aguide=270.00, H=0.0000)

# === Stack ===
# the roughnesses of each layer are set to zero to begin with

s = Stack()
slds = []
slabs = []

slds.append(SLD(name='Silicon', rho=2.074, irho=0.0000))
slabs.append(slds[0](0.0000, 35.490, magnetism=Magnetism(rhoM=0.0000, thetaM=270.00)))
s.add( slabs[0])

slds.append(SLD(name='SiOx', rho=3.469, irho=0.0000))
slabs.append(slds[1](35.100, 3.5590, magnetism=Magnetism(rhoM=0.0000, thetaM=270.00)))
s.add( slabs[1])

slds.append(SLD(name='Permalloy', rho=9.123, irho=0.0000))
slabs.append(slds[2](108.00, 8.5220, magnetism=Magnetism(rhoM=1.9420, thetaM=270.00)))
s.add( slabs[2])

slds.append(SLD(name='Platinum', rho=6.357, irho=0.0000))
slabs.append(slds[3](48.250, 0.0000, magnetism=Magnetism(rhoM=0.0000, thetaM=270.00)))
s.add( slabs[3])

slds.append(SLD(name='Water', rho=1.5000, irho=0.0000))
slabs.append(slds[4](10.000, 0.0000, magnetism=Magnetism(rhoM=0.0000, thetaM=270.00)))
s.add( slabs[4])

slds.append(SLD(name='Nafion', rho=3.7050, irho=0.0000))
slabs.append(slds[5](286.60, 7.7020, magnetism=Magnetism(rhoM=0.0000, thetaM=270.00)))
s.add( slabs[5])

slds.append(SLD(name='Air', rho=0.0000, irho=0.0000))
slabs.append(slds[6](0.0000, 0.0000, magnetism=Magnetism(rhoM=0.0000, thetaM=270.00)))
s.add( slabs[6])
    
# === Constraints ===
# thickness, interface (roughness) etc. are parameters and
# can be constrained, e.g.
# s[0].thickness = s[2].thickness

# inD2O[0].interface = inair[0].interface
# (to tie the first layer to have exactly the same thickness as the third layer)

# NB - list and array counting in python starts at zero!

# === Fit parameters ===
# "range" specifies a fitting range in terms of min/max value
# "pmp" specifices fitting range in terms of +/-  %
# "pm" specifies fitting range in terms of +/- value

# THETA OFFSET
# this parameter accounts for theta misalignment
# probe.theta_offset.range(-.01,.01)

# INTENSITY: check to see if cross-section is included in the probe defined by data files;
# if so, set the intensity for that cross-section to be equal to the pp intensity
#if hasattr(probe, 'pm'): probe.pm.intensity = probe.pp.intensity
#if hasattr(probe, 'mp'): probe.mp.intensity = probe.pp.intensity
#if hasattr(probe, 'mm'): probe.mm.intensity = probe.pp.intensity
probe.pp.intensity.range(0.9,1.1)
probe.pp.intensity.value = 1.0

probe.mm.intensity.range(0.9,1.1)
probe.mm.intensity.value = 1.0


# DISABLE CROSS-SECTIONS
# probe.xs[1] = None # disables PM
# probe.xs[2] = None # disables MP

# LAYER RHOs
#s[0].material.rho.range(1.0710, 3.0710)
s[1].material.rho.range(2.0710, 5.0000)
s[2].material.rho.range(8.2390, 10.239)
s[3].material.rho.range(5.4460, 7.4460)
s[4].material.rho.range(-1.000, 7.0000)
s[5].material.rho.range(2.7050, 4.7050)
#s[6].material.rho.range(-1.0000, 1.0000)

# LAYER RHOMs
#s[0].magnetism.rhoM.range(-1.0000, 1.0000)
#s[1].magnetism.rhoM.range(-1.0000, 1.0000)
s[2].magnetism.rhoM.range(0.94200, 2.9420)
#s[3].magnetism.rhoM.range(-1.0000, 1.0000)
#s[4].magnetism.rhoM.range(-1.0000, 1.0000)
#s[5].magnetism.rhoM.range(-1.0000, 1.0000)
#s[6].magnetism.rhoM.range(-1.0000, 1.0000)

# LAYER THETAMs
#s[0].magnetism.rhoM.range(-30.000, 30.000)
#s[1].magnetism.rhoM.range(-30.000, 30.000)
#s[2].magnetism.rhoM.range(240.00, 300.00)
#s[3].magnetism.rhoM.range(-30.000, 30.000)
#s[4].magnetism.rhoM.range(-30.000, 30.000)
#s[5].magnetism.rhoM.range(-30.000, 30.000)
#s[6].magnetism.rhoM.range(-30.000, 30.000)

# LAYER THICKNESSES
#s[0].thickness.range(0.0000, 100.00)
s[1].thickness.range(0.0000, 135.10)
s[2].thickness.range(8.0000, 208.00)
s[3].thickness.range(0.0000, 148.25)
s[4].thickness.range(0.0000, 110.00)
s[5].thickness.range(186.60, 386.60)
#s[6].thickness.range(0.0000, 100.00)

# LAYER ROUGHNESSES
s[0].interface.range(0.0000, 50.000)
s[1].interface.range(0.0000, 15.000)
s[2].interface.range(0.0000, 20.000)
s[3].interface.range(0.0000, 10.000)
s[4].interface.range(0.0000, 10.000)
s[5].interface.range(0.0000, 20.000)

# === Problem definition ===
# a model object consists of a sample and a probe,
# zed is the step size in Angstroms to be used for rendering the profile
# increase zed to speed up the calculation
zed = 1    

# step = True corresponds to a calculation of the reflectivity from an actual profile
# with microslabbed interfaces.  When step = False, the Nevot-Croce
# approximation is used to account for roughness.  This approximation speeds up
# the caclulation tremendously, and is reasonably accuarate as long as the
# roughness is much less than the layer thickness
step = False

model = Experiment(sample=s, probe=probe, dz=zed, step_interfaces = step)
## simultaneous fitting: if you define two models
## models = model1, model2
## problem = MultiFitProblem(models=models)

# fitting a single model:
problem = FitProblem(model)

problem.name = "R1H92.refl"
