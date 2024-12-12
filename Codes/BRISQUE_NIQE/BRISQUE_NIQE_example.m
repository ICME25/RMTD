
clear all; close all; clc; 
file = dir(fullfile("", "*.png"))
num = length(file)
density1 = 0.0
min1 = 100.0
max1 = 0.0
minus1 = 0
density2 = 0.0
min2 = 100.0
max2 = 0.0
minus2 = 0
for i=1:num
    image = imread(strcat("", file(i).name));
    tmp1 = brisque(image)
    tmp2 = niqe(image)
    density1 = density1 + tmp1
    density2 = density2 + tmp2
    if(tmp1 < min1)
        min1 = tmp1;
    end
    if(tmp1 < 0)
        minus1 = minus1 + 1;
    end
    if(tmp1 > max1)
        max1 = tmp1;
    end
    if(tmp2 < min2)
        min2 = tmp2;
    end
    if(tmp2 < 0)
        minus2 = minus2 + 1;
    end
    if(tmp2 > max2)
        max2 = tmp2;
    end
end
density1 = density1 / num
disp(min1)
disp(max1)
disp(minus1)
density2 = density2 / num
disp(min2)
disp(max2)
disp(minus2)

