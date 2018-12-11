import numpy as np
import cv2

class AsciiConvert():

    def __init__(self, width, height, inverted):
        self.resolution = (height, width)
        self.image_resolution = (width, height)
        self.characters_per_row = 0
        self.characters_per_col = 0
        self.char_string = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'.   "
        if inverted:
            reversed(self.char_string)
        self.inverted_bool = inverted
        self.print_image = []

    def translate(self, value, leftMin, leftMax, rightMin, rightMax):
        # Figure out how 'wide' each range is
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - leftMin) / float(leftSpan)

        # Convert the 0-1 range into a value in the right range.
        return round(rightMin + (valueScaled * rightSpan))

    def convertToSize(self, image):
        self.print_image = []
        for i in range(self.resolution[0]):
            self.print_image.append([])
            for j in range(self.resolution[1]):
                if self.inverted_bool:
                    self.print_image[i].append(' ')
                else:
                    self.print_image[i].append('$')
        return cv2.resize(image, self.image_resolution)

    def convertFrame(self, frame):
        self.print_image = []
        new_frame  = self.convertToSize(frame)
        num_cols = self.resolution[1]
        num_rows = self.resolution[0]
        # print(num_rows, num_cols)
        for i in range(num_rows):
            self.convertLine(new_frame, i, num_cols)

    def convertLine(self, frame, line_num, size):
        for i in range(size):
            self.convertToChar(frame, frame[line_num][i], line_num, i)

    def convertToChar(self, frame, pixel_value, x, y):
        char = self.char_string[self.translate(pixel_value, 0, 255, 0, len(self.char_string) - 1)]
        self.addToArray(char, x, y)

    def addToArray(self, char, x, y):
        # if y >= len(self.print_image[0]) or x >= len(self.print_image):
        #     print(len(self.print_image), len(self.print_image[0]), x, y)
        self.print_image[x][y] = char

    def printToScreen(self, scrn, start_row, start_col):
        start_cnew = start_col
        for row in self.print_image:
            for char in row:
                scrn.addstr(start_row, start_col, char)
                start_col+=1
            start_col = start_cnew
            start_row+=1

    def updateResolution(self, w, h):
        self.print_image = []
        self.resolution = (h, w)
        self.image_resolution(w, h)
