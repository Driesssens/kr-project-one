
from pylab import *
x = linspace(1, 5, 100)
y = x ** 3 - 3 * exp(-x/100)*x ** 2 + 5/(1+log(x))
figure()
plot(x, y, 'r')
xlabel('x')
ylabel('y')
title('title')
show()

