
import random

# Example from: https://towardsdatascience.com/speed-up-jupyter-notebooks-20716cbe2025
def estimate_pi(n=1e6) -> "area":
    """Estimate pi with monte carlo simulation.
    
    Arguments:
        n: number of simulations
    """
    in_circle = 0
    total = n
    
    while n != 0:
        prec_x = random.random()
        prec_y = random.random()
        if pow(prec_x, 2) + pow(prec_y, 2) <= 1:
            in_circle += 1 # inside the circle
        n -= 1
         
    return 4 * in_circle / total

estimate_pi()
