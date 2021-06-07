import pygame
from collections import deque
from Node import *

SCREEN_WIDTH = 1000

GREY = (128, 128, 128)

WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH))
pygame.display.set_caption("Visualization of Path Finding Algorithm")


def make_array(rows, screen_width):
    array = []
    node_size = screen_width // rows
    for i in range(rows):
        array.append([])
        for j in range(rows):
            node = Node(i, j, node_size, rows)
            array[i].append(node)
    return array


def draw(window, array, rows, screen_width):
    for row in array:
        for node in row:
            node.draw_node(window)
    node_size = screen_width // rows
    for i in range(rows):
        pygame.draw.line(window, GREY, (0, i * node_size), (screen_width, i * node_size), 1)
    for j in range(rows):
        pygame.draw.line(window, GREY, (j * node_size, 0), (j * node_size, screen_width))
    pygame.display.update()


def get_mouse_position(position, screen_width, rows):
    node_size = screen_width // rows
    y, x = position
    row = y // node_size
    column = x // node_size
    return row, column


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def dij_algorithm(draw, start, end):
    que = deque()
    came_from = {}
    que.append(start)
    while len(que) > 0:
        current_node = que.popleft()
        if current_node == end:
            temp = current_node
            while temp.prev:
                came_from[temp] = temp.prev
                temp = temp.prev
            reconstruct_path(came_from, end, draw)
            end.make_stop()
            return True

        for neighbour in current_node.neighbours:
            if not neighbour.visited:
                neighbour.visited = True
                neighbour.prev = current_node
                que.append(neighbour)

        draw()
        if current_node != start:
            current_node.make_closed()
    return False


def main(screen_width, window):
    ROWS = 50
    nodes_array = make_array(ROWS, screen_width)
    start = None
    stop = None
    run = True

    while run:
        for event in pygame.event.get():
            draw(WINDOW, nodes_array, ROWS, SCREEN_WIDTH)
            if pygame.mouse.get_pressed()[0]:
                position = pygame.mouse.get_pos()
                row, column = get_mouse_position(position, screen_width, ROWS)
                node = nodes_array[row][column]
                if not start and node != stop:
                    start = node
                    start.start()
                elif not stop and node != start:
                    stop = node
                    stop.stop()
                elif node != stop and node != start:
                    node.obstacle()

            elif pygame.mouse.get_pressed()[2]:
                position = pygame.mouse.get_pos()
                row, column = get_mouse_position(position, screen_width, ROWS)
                node = nodes_array[row][column]
                if node == start:
                    start.visited = False
                    start = None
                elif node == stop:
                    stop = None
                node.clear_node()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    for row in nodes_array:
                        for node in row:
                            node.neighbours_update(nodes_array)
                    dij_algorithm(lambda: draw(window, nodes_array, ROWS, screen_width), start, stop)
                if event.key == pygame.K_c:
                    start = None
                    stop = None
                    nodes_array = make_array(ROWS, screen_width)
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()


main(SCREEN_WIDTH, WINDOW)
