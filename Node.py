import pygame

DARK_BLUE = (9, 50, 93)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (198, 108, 198)
PURPLE = (129, 50, 129)
LIGHT_BLUE = (0, 204, 255)
LIGHT_GREEN = (0, 204, 102)
YELLOW = (255, 255, 102)


class Node:
    def __init__(self, row, column, width, total_rows):
        self.row = row
        self.column = column
        self.x = row * width
        self.y = column * width
        self.color = WHITE
        self.width = width
        self.total_rows = total_rows
        self.neighbours = []
        self.prev = None
        self.visited = False

    def start(self):
        self.visited = True
        self.color = PINK

    def stop(self):
        self.color = PURPLE

    def obstacle(self):
        self.color = DARK_BLUE

    def clear_node(self):
        self.color = WHITE

    def get_position(self):
        return self.row, self.column

    def is_obstacle(self):
        return self.color == DARK_BLUE

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = LIGHT_BLUE

    def make_stop(self):
        print("Make stop")
        self.color = PURPLE

    def make_path(self):
        self.color = YELLOW

    def draw_node(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    def neighbours_update(self, array):
        if self.column < self.total_rows - 1 and not array[self.row][self.column + 1].is_obstacle():  # LEFT
            self.neighbours.append(array[self.row][self.column + 1])

        if self.column > 0 and not array[self.row][self.column - 1].is_obstacle():  # RIGHT
            self.neighbours.append(array[self.row][self.column - 1])

        if self.row > 0 and not array[self.row - 1][self.column].is_obstacle():  # UP
            self.neighbours.append(array[self.row - 1][self.column])

        if self.row < self.total_rows - 1 and not array[self.row + 1][self.column].is_obstacle():  # DOWN
            self.neighbours.append(array[self.row + 1][self.column])
