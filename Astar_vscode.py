import pygame
import math
from queue import PriorityQueue

WIDTH = 800
window = pygame.display.set_mode((WIDTH,WIDTH))conda 
pygame.display.set_caption("A* path finding Algorithm")

GREEN = (51,255,87) # OUTLINE OF NODES TRAVERSED
RED = (231,76,60)  # NODES TRAVERSED
BLACK = (52, 73, 94) # BARRIER 
WHITE = (208, 211, 212) # BACKGROUND
DARKGREEN = (19, 141, 117) # PATH 
YELLOW = (241, 196, 15) # START POINT
PURPLE = (125, 60, 152) # END POINT
GREY = (133, 146, 158)  # EXTRA 


class Spot:   # spot is nothing but the cubes/nodes in the visualization.
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self. col = col
        self.x = row * width # this will give us the exact position of a specific cube 
        self.y = col *width  # same as above  (Why row/col * width?) because if the there are 50 cubes and total width is 800
                                                                    # then 800/50 = 16 (width of each cube) and we go to a specific row and multiply it with 16 to get the exact co-ordinate
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col 
    
    def is_closed(self):
        return self.color == RED
    
    def is_open(self):
        return  self.color == GREEN
    
    def is_barrier(self):
        return self.color == BLACK 
         
    def is_start(self):
        return self.color == YELLOW

    def is_end(self):
        self.color == PURPLE 

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN
    
    def make_path(self):
        self.color = DARKGREEN
    
    def make_barrier(self):
        self.color = BLACK
    
    def make_end(self):
        self.color = PURPLE
    
    def make_start(self):
        self.color = YELLOW

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):  # this is a function which makes sure that that the start and end nodes are not surrounded by barriers, and also makes sure the nodes dont fall out of the grid
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():   # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():   # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():   # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])
 
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():   # RIGHT 
            self.neighbors.append(grid[self.row][self.col + 1])

    def __lt__(self, other):
        return False 
 
def h(p1,p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2)  # manhattan distance for the heuristic functions 

def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()


def algorithm(draw, grid,start,end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0,count,start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from,end,draw)
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current]+1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()
    return False



      

 

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i,j,gap,rows)
            grid[i].append(spot)
    return grid

def draw_grid(window, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(window, GREY, (0,i*gap),(width, i*gap))
        pygame.draw.line(window, GREY, (i*gap,0),(i*gap,width))
        
#main draw function which is goingh to draw everything
def draw(window,grid,rows, width):
    window.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(window)
    draw_grid(window,rows, width)
    pygame.display.update()

def get_clicked_position(pos, rows, width):
    gap = width // rows
    y,x = pos

    row = y // gap
    col = x // gap
    return row, col

def main(window,width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False
    while run:
        draw(window,grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            
            if pygame.mouse.get_pressed()[0]:  # get_pressed()[0], here [0] tells us that we are clicking the left mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()
 
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                
                elif spot != start and spot != end:
                    spot.make_barrier()
            if pygame.mouse.get_pressed()[2]:  # [2] means right mouse button and [1] means middle mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type ==  pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)   # so here we are applying the update_neighbors function to all the spots in the grid
                    algorithm(lambda: draw(window,grid,ROWS,width), grid, start, end)
                if event.key == pygame.K_c:
                    start = None
                    end =None
                    grid = make_grid(ROWS, width)
    pygame.quit()

main(window,WIDTH)




