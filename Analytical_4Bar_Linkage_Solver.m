clc, clear

% Link Lengths
a = 40;   % mm
b = 120;  % mm
c = 80;   % mm
d = 100;  % mm

% Ask user for input angle
deg2 = input('Enter the input angle deg2 in degrees: ');

% Ratios
K1 = d/a;
K2 = d/c;
K3 = (a^2 - b^2 + c^2 + d^2) / (2*a*c);
K4 = d/b;
K5 = (c^2 - d^2 - a^2 - b^2) / (2*a*b);

% Parameters
A = cosd(deg2) - K1 - K2*cosd(deg2) + K3;
B = -2*sind(deg2);
C = K1 - (K2 + 1)*cosd(deg2) + K3;

D = cosd(deg2) - K1 + K4*cosd(deg2) + K5;
E = -2*sind(deg2);
F = K1 + (K4 - 1)*cosd(deg2) + K5;

% Discriminants
disc4 = B^2 - 4*A*C;
disc3 = E^2 - 4*D*F;

if disc4 >= 0
    deg4_open   = 2*atand((-B - sqrt(disc4))/(2*A));
    deg4_closed = 2*atand((-B + sqrt(disc4))/(2*A));
else
    deg4_open   = NaN;
    deg4_closed = NaN;
    disp('No real solution for deg4 at this input angle')
end

if disc3 >= 0
    deg3_open   = 2*atand((-E - sqrt(disc3))/(2*D));
    deg3_closed = 2*atand((-E + sqrt(disc3))/(2*D));
else
    deg3_open   = NaN;
    deg3_closed = NaN;
    disp('No real solution for deg3 at this input angle')
end

% Display results
fprintf('\nResults for deg2 = %.2f degrees\n', deg2)
fprintf('deg4 open   = %.4f degrees\n', deg4_open)
fprintf('deg4 closed = %.4f degrees\n', deg4_closed)
fprintf('deg3 open   = %.4f degrees\n', deg3_open)
fprintf('deg3 closed = %.4f degrees\n', deg3_closed)
