from refl1d.names import *
from copy import copy
## === Data files ===
data_file = 'R1XRR.refl'
slits = 0.018
instrument = NCNR.XRay(slits_below=slits, Tlo = 1.4975, slits_at_Tlo=slits, Thi = 1.4975, slits_above = slits)
probe = instrument.load(data_file,back_reflectivity=False)
#probe = Probe(T=numpy.linspace(0.68102, 18.312, 251), L=5.0000)

## === Stack ===
##
## First, we create a 'material' for each layer, which has an real and imaginary
## scattering length density, stored in a Refl1d object called 'SLD'
sld0 = SLD(name='Silicon', rho=20.070, irho=0.45800)
sld1 = SLD(name='SiOx', rho=33.940, irho=6.8710)
sld2 = SLD(name='Permalloy', rho=66.490, irho=0.0000)
sld3 = SLD(name='Interace', rho=100.00, irho=3.7500)
sld4 = SLD(name='Platinum', rho=133.90, irho=7.4510)
sld5 = SLD(name='Air', rho=0.0000, irho=0.0000)

## Then layers are created, each with its own 'material'.  If you want to force
## two layers to always match SLD you can use the same material in multiple layers.
## The roughnesses of each layer are set to zero to begin with:
layer0 = Slab(material=sld0, thickness=0.0000, interface=18.650)
layer1 = Slab(material=sld1, thickness=40.550, interface=3.2240)
layer2 = Slab(material=sld2, thickness=108.00, interface=6.7510)
layer3 = Slab(material=sld3, thickness=10.000, interface=6.7510)
layer4 = Slab(material=sld4, thickness=49.490, interface=3.6570)
layer5 = Slab(material=sld5, thickness=0.0000, interface=0.0000)

sample = Stack()
sample.add(layer0)
sample.add(layer1)
sample.add(layer2)
sample.add(layer3)
sample.add(layer4)
sample.add(layer5)

## can also be specified as:
# sample = layer0 | layer1 | layer2 | layer3 | layer4 | layer5
  
## === Constraints ===
## thickness, interface (roughness) etc. are parameters and
## can be constrained, e.g.
# layer0.thickness = layer2.thickness
## (to tie the first layer to have exactly the same thickness as the third layer)
# layer1.interface = layer2.interface
## (to make the roughness between layer1 and layer2 the same as between layer2 and layer3)
# layer0.material = layer4.material
## (make their sld properties match, real and imaginary)
# sld0.rho = sld1.rho
## (to force only the real rho to match for two materials)

## === Fit parameters ===
## "range" specifies a fitting range in terms of min/max value
## "pmp" specifies fitting range in terms of +/-  %
## "pm" specifies fitting range in terms of +/- value

## THETA OFFSET
## this parameter accounts for theta misalignment
## probe.theta_offset.range(-.01,.01)

## INTENSITY
probe.intensity.range(0.95,1.05)

## LAYER RHOs
sld0.rho.range(19.070, 21.070)
sld1.rho.range(32.940, 34.940)
sld2.rho.range(65.490, 67.490)
sld3.rho.range(99.000, 101.00)
sld4.rho.range(132.90, 134.90)
sld5.rho.range(-1.0000, 1.0000)

## LAYER ABSORPTIONS (imaginary rho)
sld0.irho.range(-0.54200, 1.4580)
sld1.irho.range(5.8710, 7.8710)
sld2.irho.range(-1.0000, 1.0000)
sld3.irho.range(2.7500, 4.7500)
sld4.irho.range(6.4510, 8.4510)
sld5.irho.range(-1.0000, 1.0000)

## LAYER THICKNESSES
layer0.thickness.range(0.0000, 100.00)
layer1.thickness.range(0.0000, 140.55)
layer2.thickness.range(8.0000, 208.00)
layer3.thickness.range(0.0000, 110.00)
layer4.thickness.range(0.0000, 149.49)
layer5.thickness.range(0.0000, 100.00)

## LAYER ROUGHNESSES
###################################################################
## the 'interface' associated with layer0 is the boundary between #
## layer0 and layer1, and similarly for layer(N) and layer(N+1)   #
###################################################################
layer0.interface.range(8.6500, 28.650)
layer1.interface.range(0.0000, 13.224)
layer2.interface.range(0.0000, 16.751)
layer3.interface.range(0.0000, 16.751)
layer4.interface.range(0.0000, 13.657)

## === Problem definition ===
## a model object consists of a sample and a probe,
## zed is the step size in Angstroms to be used for rendering the profile
## increase zed to speed up the calculation
zed = 1    

## step = True corresponds to a calculation of the reflectivity from an actual profile
## with microslabbed interfaces.  When step = False, the Nevot-Croce
## approximation is used to account for roughness.  This approximation speeds up
## the calculation tremendously, and is reasonably accuarate as long as the
## roughness is much less than the layer thickness
step = False

model = Experiment(sample=sample, probe=probe, dz=zed, step_interfaces = step)
## simultaneous fitting: if you define two models
# models = model1, model2
# problem = MultiFitProblem(models=models)

# fitting a single model:
problem = FitProblem(model)

problem.name = "R1XRR.refl"
