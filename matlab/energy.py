from numpy import dot, array, radians, cumsum, pi, linspace, sign, argmax
from matplotlib.pyplot import subplots, show
from random import random

from collections.abc import Callable
from scipy import signal

from numpy.typing import NDArray

import solar
from solar import rcolor

VCC = 3.3

SMPS = False
I_MCU =  1.5e-3 if SMPS else 2.7e-3
I_MCU_S2 = 2.8e-6

BAT_VCC = 3.7
BAT_AH = 5.0 # Ampere-hour

def pos_square(time, on=None, duty=None, period=1):
	if duty is None and on is None:
		raise ValueError("Either 'duty' or 'on' must be provided")
	
	duty = duty or (on / period) # type: ignore
	return (signal.square(2*pi*(time / period), duty=duty) + 1) / 2

consumers = [
	('MCU', lambda t: VCC * (pos_square(t, on=60, period=3600) * (I_MCU - I_MCU_S2) + I_MCU_S2)),
]

consumer_colors = {n : rcolor() for n, _ in consumers}

def cap_cumsum(arr: NDArray, max: float, min: float = 0, start: float = 0) -> NDArray:
	result = list()

	total = start
	result.append(total)
	
	for i in range(len(arr)-1):
		total += arr[i]
		if total > max:
			total = max
		elif total < min:
			total = min
		result.append(total)
	return array(result)

def calc_charge(bat_vcc, bat_ah) -> float:
	return bat_vcc * bat_ah * 3600

# axis: matplotlib axis
# time: array of time points in seconds
# gamma: tilt angle of the cube in degrees
# phi: azimuth difference between face and sun in degrees
# initial_charge: initial battery charge in Joules
# max_charge: maximum battery charge in Joules
def plot_energy(axis, time, gamma=30, phi=15, initial_charge: float = 0, max_charge=None, consm_axis=None):
	max_charge = max_charge or initial_charge

	axis.set_xlabel('Time (hours)')
	axis.grid(True, linestyle='-', alpha=0.5)

	time_h = time / 3600
	timestep = time[1] - time[0]

	power = axis
	energy = axis.twinx()

	power.set_ylabel('Power (W)')
	energy.set_ylabel('Battery (J)')
	if consm_axis:
		consm_axis.set_ylabel('Consumption (mW)')
		consm_axis.set_yscale('log')
		consm_axis.grid(True, linestyle='-', alpha=0.5, which='both')

	consumers_time = [(n, func(time)) for n, func in consumers]
	
	power_time = array(list(map(
		lambda t: solar.P_total(
			solar.theta(t), radians(gamma), radians(phi)),
		time
	)))
	
	power_total = power_time - sum(arr for _, arr in consumers_time)

	#energy_time = cumsum(power_total * timestep) + initial_charge
	energy_time = cap_cumsum(power_total * timestep, max=max_charge, min=0, start=initial_charge)

	power.plot(time_h, power_time, label='Power generated', color='orange')
	power.plot(time_h, power_total, label='Power total', color='black')

	max_consm, min_consm = float("-inf"), float("inf")
	for n, func in consumers_time:
		max_consm = max(max_consm, max(abs(func)))
		min_consm = min(min_consm, min(abs(func)))

		# power.plot(time_h, func, label=f'{n} consumption', color=consumer_colors[n])
		if consm_axis:
			consm_axis.plot(time_h, func*1000, label=f'{n} consumption', color=consumer_colors[n])
	if consm_axis:
		padding = (max_consm - min_consm) * 0.5 * 100
		consm_axis.set_ylim(min(0, (min_consm - padding) * 1000), (max_consm + padding) * 1000)

	energy.plot(time_h, energy_time, label='Battery charge', color='blue')

	power.legend(loc='upper left')
	energy.legend(loc='upper right')
	if consm_axis:
		consm_axis.legend(loc='upper right')

hstart, hend = 0,12
time = linspace(hstart*3600, hend*3600, solar.time_steps)

fig, axes = subplots(2,1, sharex=True, layout='constrained', num='Energy totaling')
main, consm = axes

plot_energy(main, time, gamma=30, phi=15, initial_charge=calc_charge(BAT_VCC, BAT_AH), consm_axis=consm)

if __name__ == '__main__':
	show()
