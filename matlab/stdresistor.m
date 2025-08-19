function [val] = stdresistor(target)
%STDRESISTOR returns the closest standard resistor value
%   Detailed explanation goes here
arguments (Input)
    target
end

arguments (Output)
    val
end

RESISTORS = [1, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0, ... 
    3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1];

STD_RESISTORS = [];
for r = RESISTORS
    for i = 0:6
        STD_RESISTORS(end+1) = r*(10^i);
    end
end

[~, i] = min(abs(STD_RESISTORS - target));

val = STD_RESISTORS(i);
end