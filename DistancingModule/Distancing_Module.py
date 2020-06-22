import cv2
import numpy as np
import math


def distanceBetweenDots(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist


def drawDots(img, x, y, colour):
    center_coordinates = (x, y)  # Center coordinates
    radius = 4  # Radius of circle
    if colour == "red":
        color = (0, 0, 255)  # Red color in BGR
    elif colour == "black":
        color = (0, 0, 0)
    elif colour == "green":
        color = (0, 255, 0)
    else:
        color = (255, 255, 255)

    thickness = -1  # Line thickness of -1 px

    img = cv2.circle(img, center_coordinates, radius, color, thickness)  # Using cv2.circle() method
    return img


def monitorSocialDistancing(img, coordinates, minTreshold, distance_factor):
    red_dots = []
    for x1, y1 in coordinates:
        check_colour = 0
        for x2, y2 in coordinates:
            if x1 == x2 and y1 == y2:
                continue
            distance = distanceBetweenDots(x1, y1, x2, y2)

            if distance < minTreshold:
                img = drawDots(img, x1, y1, "red")
                img = drawDots(img, x2, y2, "red")
                red_dots.append((x1, y1))
                red_dots.append((x2, y2))
                img = cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 1)
                img = cv2.putText(img, str(float("{:.2f}".format(distance + distance_factor))), ( int((x1 + x2)/2) - 20, int((y1 + y2) /2) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 0, cv2.LINE_AA)

    temp_red_dots = set(red_dots)
    red_dots = list(temp_red_dots)

    return img, red_dots


def plotPoints(img, coordinates):
    for x, y in coordinates:
        img = drawDots(img, x, y, "white")
    return img


def originalCoordinatesOfRedDots(coordinates, red_dots):
    red_coordinates = {}
    for new_coordinate, old_coordiante in coordinates.items():
        for red_dot in red_dots:
            if new_coordinate == red_dot:
                red_coordinates[red_dot] = old_coordiante

    return red_coordinates


def fetchRedCoordinatesFromCoordinates(coordinates, minTreshold, widthOfFrame, heightOfFrame, distance_factor = 115):
    # Make empty black image of size width and height
    img = np.zeros((heightOfFrame, widthOfFrame, 3), np.uint8)

    new_coordinates = list(coordinates.keys())

    img = plotPoints(img, new_coordinates)

    img, red_dots = monitorSocialDistancing(img, new_coordinates, minTreshold, distance_factor)

    red_coordinates = originalCoordinatesOfRedDots(coordinates, red_dots)

    return img, red_coordinates
