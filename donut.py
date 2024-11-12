import os, sys
from math import cos, sin
import math
import pygame
import colorsys
from argparse import ArgumentParser as AP
from collections import deque as DQ
import numpy as np
# Base Code was taken from https://github.com/codegiovanni/Donut_2.0/blob/main/donut.py

parser = AP()
parser.add_argument("--DeltaAngleX",    default=0.035,dest="DeltaAngleX",    type=float)
parser.add_argument("--DeltaAngleZ",    default=0.035,dest='DeltaAngleZ',    type=float)
parser.add_argument("--StartingAngleX", default=0.035,dest="StartingAngleX", type=float)
parser.add_argument("--StartingAngleZ", default=0.035,dest="StartingAngleZ", type=float)
parser.add_argument("--Width",          default=800,  dest="Width",          type=int)
parser.add_argument("--Height",         default=800,  dest="Height",         type=int)
parser.add_argument("--R1",             default=10,   dest="R1",             type=int)
parser.add_argument("--R2",             default=20,   dest="R2",             type=int)
parser.add_argument("--K2",             default=200,  dest="K2",             type=int)
parser.add_argument("--PixelW",         default=20,   dest="PixelW",         type=int)
parser.add_argument("--PixelH",         default=20,   dest="PixelH",         type=int)
parser.add_argument("--CharOption",     default=0,    dest="CharOption",     type=int)
parser.add_argument("--shiftThetaRangeBy", default=0, dest="ShiftThetaRangeBy",type=int)
parser.add_argument("--shiftPhiRangeBy",   default=0, dest="ShiftPhiRangeBy", type=int)
parser.add_argument("--shiftThetaRange",   default=False, type=bool)
parser.add_argument("--shiftPhiRange",     default=False, type=bool)
parser.add_argument("--IgnoreBackSidePixels", default=False, type=bool)
parser.add_argument("--verboseLevel",      default=0, type=int)
args= parser.parse_args()

DeltaAngleX = args.DeltaAngleX
DeltaAngleZ = args.DeltaAngleZ
StartingAngleX = args.StartingAngleX
StartingAngleZ = args.StartingAngleZ
Width = args.Width
Height = args.Height
R1 = args.R1
R2 = args.R2
K2 = args.K2
pixel_width = args.PixelW
pixel_height = args.PixelH
CharOption = args.CharOption
ShiftThetaRangeBy = args.ShiftThetaRangeBy
ShiftPhiRangeBy = args.ShiftPhiRangeBy
shiftThetaRange = args.shiftThetaRange
shiftPhiRange = args.shiftPhiRange
IgnoreBackSidePixels = args.IgnoreBackSidePixels
verboseLevel = args.verboseLevel
###################################################
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
hue = 0
Pi = math.pi
TwoPi = 2*Pi
os.environ['SDL_VIDEO_CENTERED'] = '1'
RES = Width, Height
FPS = 60

x_pixel = 0
y_pixel = 0

screen_width = Width // pixel_width
screen_height = Height // pixel_height
screen_size = screen_width * screen_height
#####################################################
AngleOfRotation_AroundAxis = {}
AngleOfRotation_AroundAxis["X"] = StartingAngleX #Pi/2 #TwoPi
AngleOfRotation_AroundAxis["Z"] = StartingAngleZ #0.0 #Pi/2
DeltaAngleOfRotation_AroundAxis = {}
DeltaAngleOfRotation_AroundAxis["X"] = DeltaAngleX
DeltaAngleOfRotation_AroundAxis["Z"] = DeltaAngleZ

theta_spacing = 0.10
phi_spacing = 0.03

charOptions = {}
charOptions[0] = ".,-~:;=!*#$@"
charOptions[1] = ". . . . . . . ."
charOptions[2] = ".. .. .. .. .. "
charOptions[3] = "... ... ... ..."
charOptions[4] = "..............."

chars = charOptions[CharOption]

K1 = screen_height * K2 * 3 / (8 * (R1 + R2))

pygame.init()

screen = pygame.display.set_mode(RES)
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 20, bold=True)


def hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


def text_display(char, x, y):
    text = font.render(str(char), True, hsv2rgb(hue, 1, 1))
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)

def stringify(output):
    k, x_pixel, y_pixel = 0, 0, 0
    s = ''
    ns = np.empty([screen_height, screen_width], dtype=str)
    for i in range(screen_height):
        y_pixel += pixel_height
        for j in range(screen_width):
            x_pixel += pixel_width
            #text_display(output[k], x_pixel, y_pixel)                                                                                                                    
            ns[i, j] = output[k]
            s += output[k]
            k += 1
        x_pixel = 0
        s += '\n'
    y_pixel = 0
    k = 0
    print(s)
    
k = 0

paused = False
running = True
while running:
    clock.tick(FPS)
    pygame.display.set_caption("FPS: {:.2f}".format(clock.get_fps()))
    screen.fill(BLACK)

    output = [' '] * screen_size
    zbuffer = [0] * screen_size
    ThetaRange, PhiRange = [], []
    ThetaStart, ThetaEnd = 0.0, TwoPi
    PhiStart, PhiEnd = 0.0, TwoPi
    theta, phi = ThetaStart, PhiStart
    while theta < ThetaEnd :
        ThetaRange.append(theta)
        theta += theta_spacing
    ThetaRange.append(ThetaEnd)
    while phi	< PhiEnd :
        PhiRange.append(phi)
        phi += phi_spacing
    PhiRange.append(PhiEnd)

    ############################################
    if shiftThetaRange == True :
        #print("Shifting Theta By "+str(ShiftThetaRangeBy))
        #print("OldThetaRange : ")
        #print(ThetaRange)
        ThetaRange = DQ(ThetaRange)
        ThetaRange.rotate(ShiftThetaRangeBy)
        ThetaRange = list(ThetaRange)
        #print("NewThetaRange : ")
        #print(ThetaRange)
    if shiftPhiRange == True :
        #print("Shifting Phi By "+str(ShiftPhiRangeBy))
        #print("OldPhiRange : ")
        #print(PhiRange)
        PhiRange = DQ(PhiRange)
        PhiRange.rotate(ShiftPhiRangeBy)
        PhiRange = list(PhiRange)
        #print("NewPhiRange : ")
        #print(PhiRange)
    # Now loop over X and Y Points on a Plane for a specific angle of rotation
    # along X axis and Y axis. We change/increment these angles at the end of the two
    # nested loop of theta and phi
    X = AngleOfRotation_AroundAxis["X"]
    Z = AngleOfRotation_AroundAxis["Z"]
    sinX, cosX = sin(X), cos(X)
    sinZ, cosZ = sin(Z), cos(Z)
    for itheta, theta in enumerate(ThetaRange):  # theta goes around the cross-sectional circle of a torus, from 0 to 2pi
        costheta = cos(theta)
        sintheta = sin(theta)
        circlex = R2 + R1 * costheta
        circley = R1 * sintheta

        for iphi, phi in enumerate(PhiRange):  # phi goes around the center of revolution of a torus, from 0 to 2pi
            cosphi = cos(phi)
            sinphi = sin(phi)

            # 3D (x, y, z) coordinates after rotation
            x = circlex * (cosZ * cosphi + sinX * sinZ * sinphi) - circley * cosX * sinZ
            y = circlex * (sinZ * cosphi - sinX * cosZ * sinphi) + circley * cosX * cosZ
            z = K2 + cosX * circlex * sinphi + circley * sinX
            ooz = 1 / z  # one over z

            # x, y projection
            xp = int(screen_width / 2 + K1 * ooz * x)
            yp = int(screen_height / 2 - K1 * ooz * y)

            position = xp + screen_width * yp

            # luminance (L ranges from -sqrt(2) to sqrt(2))
            L = cosphi * costheta * sinZ - cosX * costheta * sinphi - sinX * sintheta + cosZ * (
                        cosX * sintheta - costheta * sinZ * sinphi)

            if IgnoreBackSidePixels == True and ooz < zbuffer[position]:
                if verboseLevel > 2 :
                    print("ooz less than front pixel z postion for theta index "+str(itheta)+" and phi index "+str(iphi))
                continue
            
            zbuffer[position] = ooz  # larger ooz means the pixel is closer to the viewer than what's already plotted
            luminance_index = int(L * 8)  # we multiply by 8 to get luminance_index range 0..11 (8 * sqrt(2) = 11)
            #print("PrintLumi ", L, luminance_index)
            lenchars = len(chars)
            lumi_idx = luminance_index % lenchars
            output[position] = chars[lumi_idx]

    for i in range(screen_height):
        y_pixel += pixel_height
        for j in range(screen_width):
            x_pixel += pixel_width
            text_display(output[k], x_pixel, y_pixel)
            k += 1
        x_pixel = 0
    y_pixel = 0
    k = 0
    stringify(output)

    AngleOfRotation_AroundAxis["X"] += DeltaAngleOfRotation_AroundAxis["X"]
    AngleOfRotation_AroundAxis["Z"] += DeltaAngleOfRotation_AroundAxis["Z"]

    hue += 0.005

    if not paused:
        pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                paused = not paused
