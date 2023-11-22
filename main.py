import numpy as np
import cv2 as cv

IMAGE_SHAPE = (500, 500, 3)
CENTER = (IMAGE_SHAPE[0] // 2, IMAGE_SHAPE[1] // 2)
RADIUS = IMAGE_SHAPE[0] - CENTER[0] - 10

cv.namedWindow('window', cv.WINDOW_KEEPRATIO)


class Circle:
    def __init__(self):
        self.MIN_EOF_ANGLE = 7  # мин. угол у конечного сегмента
        self.angles = [7, 9, 12, 16]
        self.cmy = [[0, 100, 100], [0, 49, 100], [0, 0, 100], [100, 0, 100],
                    [100, 0, 0], [100, 100, 0], [60, 100, 20], [0, 100, 0]]
        self.alphabet = [['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З'],
                         ['И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П'],
                         ['Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч'],
                         ['Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']]

        # I think, это полное дерьмо
        # лучше бы сделала это с помощью массива + датакласса с полями цвета и угла
        self.circle = {'colors': [], 'angles': []}
        self.circle_len = 0

    def find_sym(self, sym):
        for row in range(len(self.alphabet)):
            if sym in self.alphabet[row]:
                return (row, self.alphabet[row].index(sym))

    def add_segment(self, value):
        if ord(value) not in range(ord('А'), ord('Я') + 1):
            print('No such letter')
            return False

        row, col = self.find_sym(value)
        angle = self.angles[row]
        color = self.cmy[col]

        if self.circle_len + angle > 360 - self.MIN_EOF_ANGLE:
            print('The word is long. Encoded ', len(
                self.circle['angles']), ' symbols.')
            return False

        self.circle['colors'].append(color)
        self.circle['angles'].append(angle)
        self.circle_len = self.circle_len + angle
        return True

    def clear(self):
        c.circle = []
        c.circle_len = 0

    def end_circle(self):
        last_angle = 360 - self.circle_len
        self.circle['colors'].append((100, 100, 100))
        self.circle['angles'].append(last_angle)
        self.circle_len = 360

    def _cmyk_to_rgb(self, cmy: tuple[int, int, int]) -> tuple:
        return tuple(map(int, tuple(map(lambda c: (1 - c/100) * 255, cmy))))

    def draw_circle(self):
        # TODO: твое, максим
        image = np.zeros(IMAGE_SHAPE)
        image[:, :, :] = (255, 255, 255)
        cv.circle(image, CENTER, RADIUS, (0, 0, 0), 5)
        current_angle = -90
        
        for i in range(len(self.circle['colors'])):
            cmyk = self.circle['colors'][i]
            angle = self.circle['angles'][i]
            r, g, b = self._cmyk_to_rgb(cmyk)
            # print(cmyk, r, g, b)
            image = cv.ellipse(image, CENTER, (RADIUS, RADIUS), 0,
                       current_angle, current_angle+angle, (b/255, g/255, r/255), -1)
            current_angle += angle

        cv.imshow('window', image)


c = Circle()

word = ''
while word == '':
    word = input('Введите слово для кодирования: ')
    for letter in word:
        if not c.add_segment(letter):
            c.clear()
            word = ''
            break

c.end_circle()
c.draw_circle()
# HINT: если слово закодировалось, то итог можно посмотреть в с.circle (словарь из angles и colors)
print(c.circle)
cv.waitKey(0)
cv.destroyAllWindows()
