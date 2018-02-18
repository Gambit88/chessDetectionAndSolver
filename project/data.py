import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

KING = 1
QUEEN = 4
BISHOP = 3
KNIGHT = 0
ROCK = 5
PAWN = 2

DATA_IMG_PATHS = ['./CHESS/Set2/Pices/BK1.jpg', './CHESS/Set2/Pices/BK2.jpg', './CHESS/Set2/Pices/BK3.jpg', './CHESS/Set2/Pices/BK4.jpg',
                  './CHESS/Set2/Pices/QK1.jpg', './CHESS/Set2/Pices/QK2.jpg', './CHESS/Set2/Pices/QK3.jpg', './CHESS/Set2/Pices/QK4.jpg',
                  './CHESS/Set2/Pices/RP1.jpg',  './CHESS/Set2/Pices/RP2.jpg', './CHESS/Set2/Pices/RP3.jpg', './CHESS/Set2/Pices/RP4.jpg'
                  ]
DATA_IMG_PATHS_2 = ['./CHESS/Set2/Pices/NB1.jpg', './CHESS/Set2/Pices/NB2.jpg', './CHESS/Set2/Pices/NB3.jpg', './CHESS/Set2/Pices/NB4.jpg',
                    './CHESS/Set2/Pices/NB5.jpg', './CHESS/Set2/Pices/NB6.jpg', './CHESS/Set2/Pices/NB7.jpg', './CHESS/Set2/Pices/NB8.jpg',
                    './CHESS/Set2/Pices/KQ1.jpg', './CHESS/Set2/Pices/KQ2.jpg', './CHESS/Set2/Pices/KQ3.jpg', './CHESS/Set2/Pices/KQ4.jpg',
                    './CHESS/Set2/Pices/KQ5.jpg', './CHESS/Set2/Pices/KQ6.jpg', './CHESS/Set2/Pices/KQ7.jpg', './CHESS/Set2/Pices/KQ8.jpg',
                    './CHESS/Set2/Pices/PR1.jpg',  './CHESS/Set2/Pices/PR2.jpg', './CHESS/Set2/Pices/PR3.jpg', './CHESS/Set2/Pices/PR4.jpg',
                    './CHESS/Set2/Pices/PR5.jpg',  './CHESS/Set2/Pices/PR6.jpg', './CHESS/Set2/Pices/PR7.jpg', './CHESS/Set2/Pices/PR8.jpg'
                    ]
DATA_LOWER_BOUND_BLACK = [[0, 0, 20], [0, 0, 20], [0, 0, 20], [0, 0, 20],
                          [0, 0, 20], [0, 0, 20], [0, 0, 20], [0, 0, 20],
                          [0, 0, 20], [0, 0, 20], [0, 0, 20], [0, 0, 20]
                          ]
DATA_UPPER_BOUND_BLACK = [[179, 255, 90], [179, 255, 100], [179, 255, 80], [179, 255, 80],
                          [179, 255, 80], [179, 255, 80], [
                              179, 255, 80], [179, 255, 120],
                          [179, 255, 70], [179, 255, 100], [
                              179, 255, 100], [179, 255, 100]
                          ]
DATA_LOWER_BOUND_WHITE = [[10, 0, 0], [10, 0, 0], [10, 0, 0], [10, 0, 0],
                          [10, 0, 0], [10, 0, 0], [10, 0, 0], [10, 0, 0],
                          [10, 0, 0], [10, 0, 0], [10, 0, 0], [10, 0, 0]
                          ]
DATA_UPPER_BOUND_WHITE = [[36, 255, 255], [36, 255, 255], [36, 255, 255], [36, 255, 255],
                          [36, 255, 255], [36, 255, 255], [
                              36, 255, 255], [36, 255, 255],
                          [36, 255, 255], [36, 255, 255], [
                              36, 255, 255], [36, 255, 255]
                          ]
DATA_UPPER_AREA_BLACK = [4500, 4500, 4500, 1500,
                         6500, 5500, 5500, 1600, 1500, 1500, 1500, 1500]
DATA_LOWER_AREA_BLACK = [1500, 1500, 1500, 500,
                         2500, 2500, 2500, 500, 1000, 1000, 955, 500]
DATA_UPPER_AREA_WHITE = [4500, 4500, 4500, 1500,
                         6000, 3000, 3000, 3000, 3000, 3000, 3000, 3000]
DATA_LOWER_AREA_WHITE = [1500, 1500, 1500, 500,
                         4000, 2000, 2000, 500, 1500, 1500, 1500, 500]

DATA_LOWER_BOUND_BLACK_2 = [[0, 0, 20], [0, 0, 20], [0, 0, 20], [0, 0, 20],
                            [0, 0, 20], [0, 0, 20], [0, 0, 20], [0, 0, 20],
                            [0, 0, 20], [0, 0, 20], [0, 0, 20], [0, 0, 20],
                            [0, 0, 20], [0, 0, 20], [0, 0, 20], [0, 0, 20],
                            [0, 0, 20], [0, 0, 20], [0, 0, 20], [0, 0, 20],
                            [0, 0, 20], [0, 0, 20], [0, 0, 20], [0, 0, 20]
                            ]
DATA_UPPER_BOUND_BLACK_2 = [[179, 255, 90], [179, 255, 110], [179, 255, 110], [179, 255, 120],
                            [179, 255, 120], [179, 255, 120], [
                                179, 255, 120], [179, 255, 140],
                            [179, 255, 120], [179, 255, 120], [
                                179, 255, 120], [179, 255, 120],
                            [179, 255, 120], [179, 255, 120], [
                                179, 255, 120], [179, 255, 120],
                            [179, 255, 120], [179, 255, 120], [
                                179, 255, 120], [179, 255, 120],
                            [179, 255, 120], [179, 255, 120], [
                                179, 255, 120], [179, 255, 120]
                            ]
DATA_LOWER_BOUND_WHITE_2 = [[10, 0, 0], [10, 0, 0], [10, 0, 0], [10, 0, 0],
                            [10, 0, 0], [10, 0, 0], [10, 0, 0], [10, 0, 0],
                            [10, 0, 0], [10, 0, 0], [10, 0, 0], [10, 0, 0],
                            [10, 0, 0], [10, 0, 0], [10, 0, 0], [10, 0, 0],
                            [10, 0, 0], [10, 0, 0], [10, 0, 0], [10, 0, 0],
                            [10, 0, 0], [10, 0, 0], [10, 0, 0], [10, 0, 0]
                            ]
DATA_UPPER_BOUND_WHITE_2 = [[36, 255, 255], [36, 255, 255], [36, 255, 255], [36, 255, 255],
                            [36, 255, 255], [36, 255, 255], [
                                36, 255, 255], [36, 255, 255],
                            [36, 255, 255], [36, 255, 255], [
                                36, 255, 255], [36, 255, 255],
                            [36, 255, 255], [36, 255, 255], [
                                36, 255, 255], [36, 255, 255],
                            [36, 255, 255], [36, 255, 255], [
                                36, 255, 255], [36, 255, 255],
                            [36, 255, 255], [36, 255, 255], [
                                36, 255, 255], [36, 255, 255]
                            ]

DATA_UPPER_AREA_BLACK_2 = [4500, 1500, 1500, 2500, 2500, 2400, 1500, 2500, 2500, 2500,
                           3000, 3000, 3000, 3000, 3000, 3000, 3000, 1100, 3000, 3000, 3000, 1850, 1850, 1850]
DATA_LOWER_AREA_BLACK_2 = [2500, 800, 1000, 1000, 1000, 1500, 1200, 1200, 1200, 1200,
                           1200, 1200, 1200, 1200, 1200, 1200, 1200, 950, 1200, 1200, 1200, 1200, 1200, 1200]
DATA_UPPER_AREA_WHITE_2 = [2500, 2500, 1500, 2500, 2500, 2500, 2500, 2500,
                           2500, 3000, 3000, 3000, 3000, 3000, 3000, 3000,
                           2000, 1000, 1000, 1500, 1500, 1500, 1500, 1000]
DATA_LOWER_AREA_WHITE_2 = [2000, 800, 800, 800, 800, 800, 800, 800,
                           800, 800, 800, 800, 800, 800, 800, 800,
                           800, 400, 400, 400, 400, 900, 600, 600]


def saveDataMap():
    data = {}
    data[KNIGHT] = []
    data[KING] = []
    data[PAWN] = []
    data[BISHOP] = []
    data[QUEEN] = []
    data[ROCK] = []
    for i in range(0, len(DATA_IMG_PATHS)):
        img = cv.imread(DATA_IMG_PATHS[i], cv.IMREAD_COLOR)
        img = cv.resize(img, (1200, 900))
        blur = cv.GaussianBlur(img, (5, 5), 0)
        blur1 = cv.bilateralFilter(blur, 9, 75, 75)

        imgHSV = cv.cvtColor(blur1, cv.COLOR_BGR2HSV)

        lowerBoundBlack = np.array(DATA_LOWER_BOUND_BLACK[i])
        upperBoundBlack = np.array(DATA_UPPER_BOUND_BLACK[i])

        lowerBoundWhite = np.array(DATA_LOWER_BOUND_WHITE[i])
        upperBoundWhite = np.array(DATA_UPPER_BOUND_WHITE[i])

        maskBlack = cv.inRange(imgHSV, lowerBoundBlack, upperBoundBlack)
        maskWhite = cv.inRange(imgHSV, lowerBoundWhite, upperBoundWhite)

        kernel = np.ones((3, 3), np.uint8)
        dilationB = cv.dilate(maskBlack, kernel, iterations=1)
        dilationW = cv.dilate(maskWhite, kernel, iterations=1)
        im2, contoursB, hierarchy2 = cv.findContours(
            dilationB, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        im3, contoursW, hierarchy3 = cv.findContours(
            dilationW, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        for countour in contoursB:
            area = cv.contourArea(countour)
            if area < DATA_UPPER_AREA_BLACK[i] and area > DATA_LOWER_AREA_BLACK[i]:
                index = i//4
                if(index == 0):
                    print("Knight")
                if(index == 1):
                    print("King")
                if(index == 2):
                    print("Pawn")
                data[index].append(countour)

        for countour in contoursW:
            area = cv.contourArea(countour)
            if area < DATA_UPPER_AREA_WHITE[i] and area > DATA_LOWER_AREA_WHITE[i]:
                index = i//4
                if(index == 0):
                    print("Bishop")
                if(index == 1):
                    print("Queen")
                if(index == 2):
                    print("Rock")
                data[index+3].append(countour)
    for i in range(0, len(DATA_IMG_PATHS_2)):
        img = cv.imread(DATA_IMG_PATHS_2[i], cv.IMREAD_COLOR)
        img = cv.resize(img, (1200, 900))
        blur = cv.GaussianBlur(img, (5, 5), 0)
        blur1 = cv.bilateralFilter(blur, 9, 75, 75)

        imgHSV = cv.cvtColor(blur1, cv.COLOR_BGR2HSV)

        lowerBoundBlack = np.array(DATA_LOWER_BOUND_BLACK_2[i])
        upperBoundBlack = np.array(DATA_UPPER_BOUND_BLACK_2[i])

        lowerBoundWhite = np.array(DATA_LOWER_BOUND_WHITE_2[i])
        upperBoundWhite = np.array(DATA_UPPER_BOUND_WHITE_2[i])

        maskBlack = cv.inRange(imgHSV, lowerBoundBlack, upperBoundBlack)
        maskWhite = cv.inRange(imgHSV, lowerBoundWhite, upperBoundWhite)

        kernel = np.ones((3, 3), np.uint8)
        dilationB = cv.dilate(maskBlack, kernel, iterations=1)
        dilationW = cv.dilate(maskWhite, kernel, iterations=1)
        im2, contoursB, hierarchy2 = cv.findContours(
            dilationB, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        im3, contoursW, hierarchy3 = cv.findContours(
            dilationW, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        for countour in contoursB:
            area = cv.contourArea(countour)
            if area < DATA_UPPER_AREA_BLACK_2[i] and area > DATA_LOWER_AREA_BLACK_2[i]:
                index = i//8
                if(index == 0):
                    print("Bishop")
                if(index == 1):
                    print("Queen")
                if(index == 2):
                    print("Rock")
                data[index+3].append(countour)

        for countour in contoursW:
            area = cv.contourArea(countour)
            if area < DATA_UPPER_AREA_WHITE_2[i] and area > DATA_LOWER_AREA_WHITE_2[i]:
                index = i//8
                if(index == 0):
                    print("Knight")
                if(index == 1):
                    print("King")
                if(index == 2):
                    print("Pawn")
                data[index].append(countour)

    print(len(data[0]))
    print(len(data[1]))
    print(len(data[2]))
    print(len(data[3]))
    print(len(data[4]))
    print(len(data[5]))
    data[KNIGHT] = np.array(data[KNIGHT])
    data[KING] = np.array(data[KING])
    data[PAWN] = np.array(data[PAWN])
    data[BISHOP] = np.array(data[BISHOP])
    data[QUEEN] = np.array(data[QUEEN])
    data[ROCK] = np.array(data[ROCK])
    data = np.array(list(data.items()))
    np.save('chessBaseData', data)

def checkFigure():
    img = cv.imread('./CHESS/Set2/Pices/NB3.jpg', cv.IMREAD_COLOR)
    img = cv.resize(img, (1200, 900))
    blur = cv.GaussianBlur(img, (5, 5), 0)
    blur1 = cv.bilateralFilter(blur, 9, 75, 75)

    imgHSV = cv.cvtColor(blur1, cv.COLOR_BGR2HSV)

    lowerBound = np.array([10, 0, 0])
    upperBound = np.array([36, 255, 255])

    mask = cv.inRange(imgHSV, lowerBound, upperBound)

    kernel = np.ones((3, 3), np.uint8)
    dilation = cv.dilate(mask, kernel, iterations=1)
    gradient = cv.morphologyEx(dilation, cv.MORPH_GRADIENT, kernel)
    im2, contours, hierarchy = cv.findContours(
        dilation, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    cnt = []
    for countour in contours:
        area = cv.contourArea(countour)
        if area < 1500 and area > 800:
            cnt.append(countour)

    cv.drawContours(img, cnt, -1, (255, 0, 255), 3)

    cv.imshow("contures", img)
    cv.imshow("mask", mask)
    #cv.imshow("closing", dilation)
    cv.waitKey()

#checkFigure()