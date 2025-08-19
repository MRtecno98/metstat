function [str] = siprefix(value)
%MAGNCHAR Return string representation of integer with SI prefix for
%magnitude
%   Detailed explanation goes here
arguments (Input)
    value
end

arguments (Output)
    str
end

ORD = ["", "k", "M", "G", "T", "P", "E"];

o = floor(log10(value) / 3);

str = sprintf("%.2f%s", value / 10^(3*o), ORD(o + 1));
end