from cmu_graphics import *
import math

#banked curve physics
#similar to a racer car in a course
#as theta increases the amount the speed decreases also increases
def bankedCurve(theta):
    theta = abs(theta)
    radians = theta / 180 
    accel = (9.8 * math.cos(radians)) * math.sin(radians)
    return accel

#based on normal force and theta we can find accel for the left/right direction
#as you hold one of the keys continious theta increases and how fast skier
#moves left or right also increases
def forceTurn(theta, hillAngle):
    theta = abs(theta)
    radians = theta / 180
    force = math.cos(hillAngle) * math.sin(radians)
    acceleration = force * 10 ** 4
    return acceleration