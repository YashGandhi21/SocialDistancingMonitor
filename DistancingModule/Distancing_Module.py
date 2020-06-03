import cv2
import numpy as np
import math

width = 800
height = 600

def distance_between_dots(x1, y1, x2, y2):

        dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return dist

def draw_dots(img, x, y, colour):

        center_coordinates = (x, y)     # Center coordinates
        radius = 4                      # Radius of circle
        if colour == "red":
                color = (0, 0, 255)     # Red color in BGR
        elif colour == "black":
                color = (0, 0, 0)
        elif colour == "green":
                color = (0, 255, 0)
        else:                              
                color = (255, 255, 255)

        thickness = -1                  # Line thickness of -1 px
         
        img = cv2.circle(img, center_coordinates, radius, color, thickness)     # Using cv2.circle() method
        return img

def social_distancing(img, coordinates):
       
        red_dots = []
        for x1, y1 in coordinates:
                check_colour = 0
                for x2, y2 in coordinates:
                        if x1 == x2 and y1 == y2:
                                continue
                        distance = distance_between_dots(x1, y1, x2, y2)
                        
                        if distance < 15:
                                img = draw_dots(img, x1, y1, "red")
                                img = draw_dots(img, x2, y2, "red")
                                red_dots.append((x1, y1))
                                red_dots.append((x2, y2))
        
        temp_red_dots = set(red_dots)
        red_dots = list(temp_red_dots)

        return img, red_dots


def plot_points(img, coordinates):
        for x, y in coordinates:
                img = draw_dots(img, x, y, "white")
        return img

def original_coordinates_of_red_dots(coordinates, red_dots):
        
        red_coordinates = {}
        for new_coordinate, old_coordiante in coordinates.items():
                for red_dot in red_dots:
                        if new_coordinate == red_dot:
                                red_coordinates[red_dot] = old_coordiante

        return red_coordinates


def red_coordinates_from_coordinates(coordinates):
        
        # Make empty black image of size width and height
        img = np.zeros((height, width, 3), np.uint8)

        new_coordinates = list(coordinates.keys())

        img = plot_points(img, new_coordinates)

        img, red_dots = social_distancing(img, new_coordinates)

        red_coordinates = original_coordinates_of_red_dots(coordinates, red_dots)

        return img, red_coordinates


