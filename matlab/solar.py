from numpy import dot, array, radians, sin, cos, pi, linspace, arange
from matplotlib.pyplot import subplots, show
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

time_steps = 1000

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

	return [xc, yc, zc, -xc, -yc, -zc]

def rcolor():
	return (random(), random(), random())

time = linspace(0, daytime, time_steps)
time_h = time / 3600

phi_range = arange(0, 361, 72)
gamma_range = arange(0, 91, 18)
theta_range = theta(time)

gamma_colors = {gamma : rcolor() for gamma in gamma_range}

fig, ax = subplots(len(phi_range) // 2, 2, sharex=True, layout='constrained', num='Solar power')

for i, phi_deg in enumerate(phi_range):
	row = i % (len(phi_range) // 2)
	column = i // (len(phi_range) // 2)
	if i > (len(phi_range) // 2) - 1:
		row = (len(phi_range) // 2) - row - 1
		
	axis = ax[row, column]

	axis.set_ylabel('Power (W)')
	axis.set_xlabel('Time (hours)')
	axis.grid(True, linestyle='-', alpha=0.5)

	axis.set_title(f'Solar power for phi={phi_deg}°')

	phi = radians(phi_deg)
	for gamma_deg in gamma_range:
		gamma = radians(gamma_deg)

		power = [P_total(theta, gamma, phi) for theta in theta_range]
			
		axis.plot(time_h, power, label=f'gamma={gamma_deg}°' if i == 0 else None, color=gamma_colors[gamma_deg])

fig.legend(loc='outside center right')

fig, gm = subplots(1,1, sharex=True, num='Gamma comparison', layout='constrained')

gm.set_ylabel('Power (W)')
gm.set_xlabel('Tilt angle gamma (degrees)')
gm.set_title('Solar power for phi=0° parametrized to time of day')
gm.grid(True, linestyle='-', alpha=0.5)

phi = radians(0)
gm_space = linspace(0, pi/2, 100)
for t_h in arange(0, 12, 2):
	t = t_h * 3600
	thet = theta(t)

	power = [P_total(thet, gm_angle, phi) for gm_angle in gm_space]

	gm.plot(gm_space * 180 / pi, power, label='time={}:00'.format(t_h), color=rcolor())
	
fig.legend(loc='upper right')

if __name__ == '__main__':
	show()
