import os, sys
import numpy as np
from collections import defaultdict
from math import sin, cos, pi
import colorsys
import pygame




def stringify(output, screen_height, screen_width,
              pixel_height, pixel_width):
    k, x_pixel, y_pixel = 0, 0, 0
    s = ''
    ns = np.empty([screen_height, screen_width], dtype=str)
    for i in range(screen_height):
        y_pixel += pixel_height
        for j in range(screen_width):
            x_pixel += pixel_width
            #text_display(output[k], x_pixel, y_pixel)                                                                                                  \
                                                                                                                                                         
            ns[i, j] = output[k]
            s += output[k]
            k += 1
        x_pixel = 0
        s += '\n'
    y_pixel = 0
    k = 0
    print(s)


def rotate_coordinates_along_xyz(coordinate_dict, angle, axis):
    X, Y, Z = coordinate_dict["x"], coordinate_dict["y"], coordinate_dict["z"]
    if axis == "X" :
        rotation_matrix = np.asarray([[1.0, 0.0, 0.0], [0.0,  cos(angle), sin(angle)], [0.0, -sin(angle), cos(angle)]])
    elif axis == "Y":
        rotation_matrix = np.asarray([[cos(angle), 0.0, sin(angle)], [0.0,  1.0, 0.0], [-sin(angle), 0.0, cos(angle)]])
    elif axis == "Z":
        rotation_matrix = np.asarray([[cos(angle), sin(angle), 0.0], [-sin(angle),  cos(angle), 0.0], [0.0, 0.0, 1.0]])

    final_XCoordinates, final_YCoordinates, final_ZCoordinates = [], [], []
    numParticles = len(X)
    for i in range(numParticles):
        vec = np.asarray([X[i], Y[i], Z[i]])
        transformed_vec = np.matmul(rotation_matrix, vec)
        final_XCoordinates.append(transformed_vec[0])
        final_YCoordinates.append(transformed_vec[1])
        final_ZCoordinates.append(transformed_vec[2])
    return final_XCoordinates, final_YCoordinates, final_ZCoordinates



def rotate_donuts_along_xyz(donut, angle, axis, K2 = 0, calculate_ooz=False):
    rotation_output = [rotate_coordinates_along_xyz(donut[phi], angle, axis) for phi in donut.keys()]
    rotated_donut = defaultdict(defaultdict)
    phiList = list(donut.keys())
    for iphi, phi in enumerate(donut.keys()):
        phiIdx = phiList.index(phi)
        if phiIdx != iphi :
            raise Warning("Phi index Does not Match !!! Problem. Be Careful.")
        rotated_donut[phi]["x"] = rotation_output[phiIdx][0]
        rotated_donut[phi]["y"] = rotation_output[phiIdx][1]
        rotated_donut[phi]["z"] = [K2 + elem for elem in rotation_output[phiIdx][2]]
        
            
    if calculate_ooz == True :
        for phi in donut.keys():
            rotated_donut[phi]["ooz"] = [1./z for z in rotated_donut[phi]["z"]]

    return rotated_donut

def create_donut_from_circle(InitialCoordinates, PhiRange, axis):
    CoordinatesAfter_RotationBy_Phi_AlongGivenAxis = [rotate_coordinates_along_xyz(InitialCoordinates, phi, axis) for phi in PhiRange]
    Donut = defaultdict(defaultdict)
    for iphi, phi in enumerate(PhiRange):
        Donut[phi]["x"] = CoordinatesAfter_RotationBy_Phi_AlongGivenAxis[iphi][0]
        Donut[phi]["y"] = CoordinatesAfter_RotationBy_Phi_AlongGivenAxis[iphi][1]
        Donut[phi]["z"] = CoordinatesAfter_RotationBy_Phi_AlongGivenAxis[iphi][2]

    return Donut


def hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


def text_display(char, x, y, font, screen, hue=0):
    text = font.render(str(char), True, hsv2rgb(hue, 1, 1))
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)


def paint_on_pygame_terminal_GiovanniCode9393Style(OutputArray,
                                                   PixelHeight, PixelWidth,
                                                   ScreenHeight, ScreenWidth,
                                                   font, screen):
    x_pixel, y_pixel = 0, 0
    k = 0
    for i in range(ScreenHeight):
        y_pixel += PixelHeight
        for j in range(ScreenWidth):
            x_pixel += PixelWidth
            text_display(OutputArray[k], x_pixel, y_pixel, font, screen)
            k += 1
        x_pixel = 0
    y_pixel = 0
    k = 0
