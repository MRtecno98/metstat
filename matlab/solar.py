from numpy import dot, array, radians, sin, cos, pi, linspace, arange
from matplotlib.pyplot import subplots, show, subplots_adjust
from random import random

VCC = 3.3

SMPS = False
I_MCU =  1.5e-3 if SMPS else 2.7e-3
I_MCU_S2 = 2.8e-6

Emax = 1000 # Maximum irradiance in W/m^2
A = 0.05**2 # Area of solar panel in m^2
eta = 0.20 # Efficiency of solar panel

daytime = 12 * 3600 # hours in seconds

# phi: azimuth difference between face and sun, between [0, 2pi]
# gamma: tilt angle of the cube, between [0, pi/2]

time_steps = 100

# x, y, z: coordinate system
# xc, yc, zc: cube's coordinate system, rotated by gamma around z-axis
# s: irradiation direction vector, function of theta, which is a function of time

x = array([1, 0, 0])
y = array([0, 1, 0])
z = array([0, 0, 1])

# theta is a function of time
def s(theta, phi):
	return array([
		-sin(phi)*cos(theta),
		sin(theta),
		cos(phi)*cos(theta),
	])

def P_cell(theta, phi, face):
	# I = irradiance on the face
	I = Emax * max(0, dot(-s(theta, phi), face))

	return I * A * eta

def P_total(theta, gamma, phi):
	total = 0
	for face in faces(gamma):
		cell = P_cell(theta, phi, face)
		total += cell
	return total

# time: [0, daytime]
def theta(time):
	return (time / daytime) * pi

def faces(gamma):
	xc = array([cos(gamma), sin(gamma), 0])
	yc = array([sin(gamma), cos(gamma), 0])
	zc = z

	return [xc, yc, -xc, -yc, zc, -zc]

def rcolor():
	return (random(), random(), random())

time = linspace(0, daytime, time_steps)

time_h = time / 3600

fig, ax = subplots(2,1, sharex=True)

pwr1, pwr2 = ax[0], ax[1]

pwr1.set_ylabel('Power (W)')
pwr1.set_xlabel('Time (hours)')

pwr1.set_title('Solar power for phi=0° parametrized to tilt angle gamma')

phi = radians(0)
for gamma_deg in arange(0, 90, 15):
	gamma = radians(gamma_deg)

	power = [P_total(theta(t), gamma, phi) for t in time]
		
	pwr1.plot(time_h, power, label='gamma={}°'.format(gamma_deg), color=rcolor())

pwr2.set_ylabel('Power (W)')
pwr2.set_xlabel('Time (hours)')

pwr2.set_title('Solar power for gamma=30° parametrized to azimuth phi')

gamma = radians(30)
for phi_deg in arange(0, 180, 45):
	phi = radians(phi_deg)

	power = [P_total(theta(t), gamma, phi) for t in time]
		
	pwr2.plot(time_h, power, label='phi={}°'.format(phi_deg), color=rcolor())

fig.tight_layout()
fig.legend(loc='upper right', fancybox=True, shadow=True)

fig, gm = subplots(1,1, sharex=True)

gm.set_ylabel('Power (W)')
gm.set_xlabel('Tilt angle gamma (degrees)')
gm.set_title('Solar power for phi=0° parametrized to time of day')

phi = radians(0)
gm_space = linspace(0, pi/2, 100)
for t_h in arange(0, 12, 2):
	t = t_h * 3600
	thet = theta(t)

	power = [P_total(thet, gm_angle, phi) for gm_angle in gm_space]

	gm.plot(gm_space * 180 / pi, power, label='time={}:00'.format(t_h), color=rcolor())
	

fig.legend(loc='upper right', fancybox=True, shadow=True)
fig.tight_layout()

show()
