#!/usr/bin/env python

"""

The waves.py module contains an assortment of tools for working with
linear wave theory calculations.

"""
# py2/3 compatible:
from __future__ import absolute_import, division, print_function, unicode_literals

import  numpy as np


def wave_number(g, omega, h):

    p = omega**2 * h / g
    q = dispersion(p)
    k = q * omega**2 / g

    return k

def frequency(g, k, h):

    omega = np.sqrt( g*k*np.tanh(k*h) )

    return omega

def dispersion(p, Tol = 1e-14, MaxIter = 100):
    """

    finds q, given p

    q = gk/omega^2     non-d wave number
    p = omega^2 h / g   non-d water depth

    """
    #First guess (from Fenton and McKee):
    q = np.tanh( p**0.75 )** (-2.0/3.0)

    iter = 0
    f = q * np.tanh(q*p) - 1
    while abs(f) > Tol:
        qp = q*p
        fp = qp / ( np.cosh(qp)**2 ) + np.tanh(qp) 
        q = q - f/fp
        f = q * np.tanh(q*p) - 1
        iter += 1
        if iter > MaxIter:
            raise Exception("Maximum number of iterations reached in dispersion()")
    return q

def max_u(a, omega, g, h, z):

    k = wave_number(g, omega, h)
    u = a * omega * ( np.cosh( k*(h+z) ) / np.sinh( k*h ) )

    return u

def amp_scale_at_depth(g, omega, h, z):

    k = wave_number(g, omega, h)

    return   np.cosh(k*(h+z))  /  np.cosh(k*(h))

    
def celerity(k, h, g):

    C = np.sqrt( g/k * np.tanh(k*h) )
    
    return C

def group_speed(k, h, g):

    n = 1.0/2 * (1 + ( 2*k*h / np.sinh(2*k*h) ) )
    Cg = n * celerity(k, h, g)

    return Cg

def shoaling_coeff(omega, g, h0, h2):
    """

    Compute the shoaling coeff for two depths: ho and h1.

    Pass in h0 = None for deep water

    """
    

    k2  =  wave_number(g,omega,h2)
    Cg2 = group_speed(k2, h2, g)
    if h0 is not None:
        k0 =  wave_number(g,omega,h0)

        Cg0 = group_speed(k0, h0, g)

        Ks = np.sqrt(Cg0/Cg2)

        return Ks
    else: #Deep water
        return np.sqrt((g / (2*omega)) / Cg2)



if __name__ == "__main__":

    import pylab

##    print "Computing velocity at the bottom"
##    print "Please use all SI units"

##    g = 9.806

##    H = input("Wave height? =>")
##    h = input("Depth ? =>")
##    T = input("Period? =>")

##    a = H/2
##    omega = 2*np.pi/T
##    z = -h
    
##    k = wave_number(g,omega,h)
##    MaxU = max_u(a,omega,g,k,h,z)

##    print "the maximum velocity at the bottom is: %f m/s", MaxU
##    print "Computing velocity at the bottom"
##    print "Please use all SI units"


#     g = 9.806
#     h = 55

#     print "In a water depth of 55m (180ft): "

#     k = 2 * np.pi / (2 * h)

#     omega = frequency(g, k, h)

#     T = 2 * np.pi / omega

#     print "The minimum period of waves affecting the bottom is %f seconds"%T

    
#     print "the shoaling coeff is:"
#     print shoaling_coeff(omega, g, None, h )
#     print "Which is negligable"


#     #bins, Es = ReadNDBCSpectrum("46042w2004.txt")
#     bins, Es, dates = ReadNDBCSpectrum("Winter2004.txt")

#     print "Periods:", 1 / bins
#     # convert bins (Hz) to k:
#     omega = 2 * np.pi * bins
#     k = wave_number(g, omega, h)

#     print "Wave Numbers:", k

#     # convert to energy at the bottom:
#     Eb = Es / (np.sinh(k*h)**2)

#     print "Energy at Top:",
#     print Es[0:1]
#     print "Energy at Bottom:",
#     print Eb[0:1]
#     #print "Ratio:"
#     #print Eb[0:1] / Es[0:1]

#     # total energy
#     Etotal = np.sum(Eb, 1)# sum across rows

# ##    # Plot energy:
# ##    pylab.contour(1/bins, np.arange(len(Eb)), Eb )
# ##    pylab.xlabel("Period")
# ##    pylab.show()

#     pylab.figure(2)
#     pylab.contour(1/bins, np.arange(50), Eb[1330:1380, :] )
#     pylab.xlabel("Period")
#     pylab.show()

        
#     # find the Maximum
#     MaxTime  = np.argmax(Etotal)
#     print "time of max Energy"
#     print dates[MaxTime]
#     MaxDay_s = Es[MaxTime]
#     MaxDay_b = Eb[MaxTime]

#     #Equivalent wave height
#     domega = omega[1] - omega[0] # this assumes the bins are all the same size!
#     dHz = bins[1] - bins[0]
#     #print "domega:", domega

#     Hmax_s = np.sqrt(8 * MaxDay_s * domega)
#     Hmax_b = np.sqrt(8 * MaxDay_b * domega)
#     #Hmax_s = np.sqrt(8 * MaxDay_s * dHz)
#     #Hmax_b = np.sqrt(8 * MaxDay_b * dHz)
#     print "Hmax_s:", Hmax_s 
#     print "Hmax_b:", Hmax_b 
 
#     Umax_s = Hmax_s/2 * omega
#     Umax_b = Hmax_b/2 * omega

    
#     Umax_s2 = max_u(Hmax_s/2, omega, g, k, h, z = 0)
#     Umax_b2 = max_u(Hmax_s/2, omega, g, k, h, z = -h)

#     print "Umax_b:",  Umax_b

#     MaxU_i = np.argmax(Umax_b)

#     print "During a storm on", dates[MaxTime]
#     print "Maximum Wave height is: %.2f"%Hmax_s[MaxU_i]

#     print "Maximum velocity at the surface is %.2f m/s:"%Umax_s[MaxU_i]
#     print "Maximum velocity at bottom is %.2f m/s:"%Umax_b[MaxU_i]

#     print "Maximum velocity at the surface is %.2f m/s:"%Umax_s2[MaxU_i]
#     print "Maximum velocity at bottom is %.2f m/s:"%Umax_b2[MaxU_i]

#     print "At a period of %.1f seconds"%(2*np.pi/omega[MaxU_i])
#     print "The Wavelength at that period is %.1f meters"%(2*np.pi/k[MaxU_i])
    







