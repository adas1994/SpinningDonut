import os, sys
from math import cos, sin
import math
import pygame
import colorsys
from argparse import ArgumentParser as AP
from collections import deque as DQ
from collections import defaultdict
import numpy as np
import myfuncs 
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
font = pygame.font.SysFont('Arial', 20, bold=True)
screen = pygame.display.set_mode(RES)
clock = pygame.time.Clock()

    
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
        ThetaRange = DQ(ThetaRange)
        ThetaRange.rotate(ShiftThetaRangeBy)
        ThetaRange = list(ThetaRange)
        
    if shiftPhiRange == True :
        PhiRange = DQ(PhiRange)
        PhiRange.rotate(ShiftPhiRangeBy)
        PhiRange = list(PhiRange)
        
        
    # Now loop over X and Y Points on a Plane for a specific angle of rotation
    # along X axis and Y axis. We change/increment these angles at the end of the two
    # nested loop of theta and phi
    X = AngleOfRotation_AroundAxis["X"]
    Z = AngleOfRotation_AroundAxis["Z"]
    sinX, cosX = sin(X), cos(X)
    sinZ, cosZ = sin(Z), cos(Z)
    SinThetaRange = [sin(theta) for theta in ThetaRange]
    CosThetaRange = [cos(theta) for theta in ThetaRange]
    CircleXRange = [R2 + R1 * cosTheta for cosTheta in CosThetaRange]
    CircleYRange = [R1 * sinTheta for sinTheta in SinThetaRange]
    CircleZRange = [0.0 for i in range(len(CircleYRange))]
    InitialCoordinates = {}
    InitialCoordinates["x"] = CircleXRange
    InitialCoordinates["y"] = CircleYRange
    InitialCoordinates["z"] = CircleZRange
    
    
    DonutCreatedFrom2DCircle = myfuncs.create_donut_from_circle(InitialCoordinates, PhiRange, "Y")
    Rotated_Donut_AlongXAxis = myfuncs.rotate_donuts_along_xyz(DonutCreatedFrom2DCircle, X, "X", K2 = 0, calculate_ooz = False)
    Rotated_Donut_AlongZAxis = myfuncs.rotate_donuts_along_xyz(Rotated_Donut_AlongXAxis, Z, "Z", K2 = K2, calculate_ooz = True)

    # x, y projection
    XYPoints_ProjectedOnScreen = defaultdict(defaultdict)
    Positions = defaultdict(defaultdict)
    for phi in Rotated_Donut_AlongZAxis.keys():
        XYPoints_ProjectedOnScreen[phi]["x"] = [int(screen_width / 2 + K1 * ooz * x) for x,ooz in
                                                zip(Rotated_Donut_AlongZAxis[phi]["x"], Rotated_Donut_AlongZAxis[phi]["ooz"])]
        XYPoints_ProjectedOnScreen[phi]["y"] = [int(screen_height / 2 - K1 * ooz * y) for y,ooz in
                                                zip(Rotated_Donut_AlongZAxis[phi]["y"], Rotated_Donut_AlongZAxis[phi]["ooz"])]

        XYPoints_ProjectedOnScreen[phi]["position"] = [xp + screen_width * yp for xp, yp in
                                                       zip(XYPoints_ProjectedOnScreen[phi]["x"], XYPoints_ProjectedOnScreen[phi]["y"])]
        Positions[phi] = XYPoints_ProjectedOnScreen[phi]["position"]

    # luminance (L ranges from -sqrt(2) to sqrt(2))
    Lumi = defaultdict(list)
    lenchars = len(chars)
    for phi in XYPoints_ProjectedOnScreen.keys() :
        T1Vec = np.array([cos(phi) * costheta * sinZ for costheta in CosThetaRange])
        T2Vec = np.array([cosX * costheta * sin(phi) for costheta in CosThetaRange])
        T3Vec = np.array([sinX * sintheta for sintheta in SinThetaRange])
        T4Vec = np.array([cosZ * (cosX * sintheta - costheta * sinZ * sin(phi)) for sintheta, costheta in zip(SinThetaRange, CosThetaRange)])
        Lumi[phi] = [int(elem * 8) % lenchars for elem in T1Vec - T2Vec -T3Vec + T4Vec]
        # we multiply by 8 to get luminance_index range 0..11 (8 * sqrt(2) = 11)

    for phi in Positions.keys():
        OOZsVec_ForFinalDonutConfig = Rotated_Donut_AlongZAxis[phi]["ooz"]
        for ipos, pos in enumerate(Positions[phi]) :
            
            if IgnoreBackSidePixels == True and ooz < zbuffer[position]:
                if verboseLevel > 2 :
                    print("ooz less than front pixel z postion for theta index "+str(itheta)+" and phi index "+str(iphi))
                continue
            zbuffer[pos] = Rotated_Donut_AlongZAxis[phi]["ooz"][ipos]
            # larger ooz means the pixel is closer to the viewer than what's already plotted
            output[pos] = chars[Lumi[phi][ipos]]


    """
    ##############################################################################
    ip = PhiRange[0]
    ks = XYPoints_ProjectedOnScreen[ip].keys()
    for k in ks:
        print(k)
        v = XYPoints_ProjectedOnScreen[ip][k]
        lv = len(v)
        print(v)
        print(lv)
        print("****************************************************")
    print(len(zbuffer))
    #sys.exit()
    ##############################################################################
    """
    myfuncs.paint_on_pygame_terminal_GiovanniCode9393Style(output, pixel_height, pixel_width, screen_height, screen_width, font, screen)
    myfuncs.stringify(output, screen_height, screen_width, pixel_height, pixel_width)

    #################################################################################
    # Change X and Z angle for next round of drawing
    AngleOfRotation_AroundAxis["X"] += DeltaAngleOfRotation_AroundAxis["X"]
    AngleOfRotation_AroundAxis["Z"] += DeltaAngleOfRotation_AroundAxis["Z"]
    #################################################################################
    # Block for drawing on Pygame terminal
    # Code from Giovanni (https://www.youtube.com/@giovannicode9393)
    # Don't bother to change
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
    #######################################################
