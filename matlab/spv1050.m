clc
clear all

% for both resistor ladders
Rt = 15000000 % Total resistance (min. leak)
I = 0.5e-6  % Max leakage current

% UVP (UnderVoltage Protection) EOC (End of Charge) Resistors

Vbg = 1.23;  % Reference voltage for UVC/EOC compare

% TODO: TO BE DEFINED (depending on battery)
Veoc = 4.25; % End of charge level
Vuvp = 0.5;  % Undervoltage protection level

R6 = (Vbg / Veoc)*Rt;
R5 = (Vbg / Vuvp)*Rt - R6;
R4 = Rt - R5 - R6;

% MPPT (Max power point tracking) Resistors

% TODO: TO BE MEASURED
Voc_max = 2.2;  % Max open circuit voltage at source
MPPTr   = 0.75; % MPPT ratio (Vmp_typ / Voc_typ)

Vmpp_max = Voc_max - 0.1; % Max range of the MPP pin (sugg. by DS)

if ~(Rt > (Voc_max/I) * MPPTr)
    println("Not enough total resistance to meet leakage " + ...
            "current requirements");
end

R1 = Rt * (1 - (Vmpp_max / Voc_max));
R2 = Rt * (Vmpp_max / Voc_max) * (1 - MPPTr);
R3 = Rt * (Vmpp_max / Voc_max) * MPPTr;

% Display results

name = ["R1";"R2";"R3";"R4";"R5";"R6"];
values = [R1;R2;R3;R4;R5;R6];
standard = arrayfun(@(x) siprefix(stdresistor(x)), values);

fprintf(['R1: %+e Ohms\nR2: %+e Ohms\nR3: %+e Ohms\n' ...
    'R4: %+e Ohms\nR5: %+e Ohms\nR6: %+e Ohms\n'], ...
    R1, R2, R3, R4, R5, R6);

table(name, values, standard)