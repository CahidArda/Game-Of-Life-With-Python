from turtle import Screen, Turtle
from time import sleep
import numpy as np

class MyTurtle:
    
    def __init__(self):
        self.trt = Turtle()
        self.trt.color("#242424")   #colour of gameboard lines
        self.trt.hideturtle()

    def drawLine(self, cor1, cor2):
        self.trt.penup()
        self.trt.goto(cor1[0], cor1[1])
        self.trt.pendown()
        self.trt.goto(cor2[0], cor2[1])
        self.trt.penup()

class Tile:

    def __init__(self, indx, tileSize):
        self.cor = [indx[0]*(tileSize+1), -indx[1]*(tileSize+1)]    #store pixel coordinates of the tile
        self.indx = indx                                            #store index values of the tile
        self.tileSize = tileSize                                    #store universal tile size

    #fills the tile with the given colour when called
    def fillTile(self, color):
    	fillerTurtle = Turtle()
    	fillerTurtle.penup()
    	fillerTurtle.goto(self.cor[0]+1, self.cor[1]-1)

    	fillerTurtle.color(color)
    	fillerTurtle.begin_fill()
    	for i in range(3):
    		fillerTurtle.forward(self.tileSize)
    		fillerTurtle.right(90)

    	fillerTurtle.forward(self.tileSize)
    	fillerTurtle.end_fill()
    	fillerTurtle.hideturtle()

class Gameboard:

    def __init__(self, numberOfTiles, tileSize, screenSize, screen):
        self.trt = MyTurtle()   #used to draw the gameBoard
        self.screen = screen    #used to stop player input after failiure

        self.numberOfTiles = numberOfTiles
        self.tileSize = tileSize            #stores universal size of a tile
        self.screenSize = screenSize        #stores dimensions of the board (pixelwise)

        self.tiles = []             #stores every single tile object

        #fill 'tiles' with Tile objects and 'checkedTiles' with False
        for y in range(numberOfTiles[1]):
            subTiles = []
            for x in range(numberOfTiles[0]):
                subTiles.append(Tile([x,y], self.tileSize))
            self.tiles.append(subTiles)

        self.drawGameboard()         
    
    def drawGameboard(self):
        for y in range(self.numberOfTiles[1]+1):    #add vertical lines
            self.trt.drawLine( [0, -(self.tileSize+1)*y] , [self.screenSize[0], -(self.tileSize+1)*y] )

        for x in range(self.numberOfTiles[0]+1):     #draw horizonral lines
            self.trt.drawLine( [(self.tileSize+1)*x, 0] , [(self.tileSize+1)*x, -self.screenSize[1]] )

    def getTile(self, indx):
        return self.tiles[indx[1]][indx[0]]

    def get_all_tile_indexes(self):
        res = []
        for x in range(self.numberOfTiles[0]):
            for y in range(self.numberOfTiles[1]):
                res.append([x,y])
        return res

    #checks if a given index is within the boundries of the gameboard
    def withinLimits(self, indx):
        x = indx[0]
        y = indx[1]
        return not ((x<0) or (x>=self.numberOfTiles[0]) or (y<0) or (y>=self.numberOfTiles[1]))


class Simulation:
    def __init__(self, gameboard):
        self.gameboard = gameboard
        self.live_tiles = []
        self.tile_values = np.zeros((gameboard.numberOfTiles[1], gameboard.numberOfTiles[0]), dtype=int)

    def add_live_cell(self, indx):
        if indx not in self.live_tiles:
            self.live_tiles.append(indx)
            self.gameboard.getTile(indx).fillTile("white")
            for neighbour_index in self.get_neighbour_indexes(indx):
                self.tile_values[neighbour_index[1]][neighbour_index[0]] += 1
    
    def remove_live_cell(self, indx):
        if indx in self.live_tiles:
            self.live_tiles.remove(indx)
            self.gameboard.getTile(indx).fillTile("#285078")
            
            for neighbour_index in self.get_neighbour_indexes(indx):
                self.tile_values[neighbour_index[1]][neighbour_index[0]] -= 1

    def get_neighbour_indexes(self, indx):
        neigbour_indexes = []
        for x in range(-1,2):
            for y in range(-1,2):
                new_indx = [indx[0]+x, indx[1]+y]

                if self.gameboard.withinLimits(new_indx) and new_indx!=indx:
                    neigbour_indexes.append(new_indx)
        return neigbour_indexes

    def get_number_of_live_neigbours(self, indx):
        return self.tile_values[indx[1]][indx[0]]

    def tile_is_live_in_next_state(self, indx):
        number_of_live_neigbours = self.get_number_of_live_neigbours(indx)
        
        if number_of_live_neigbours== 0:
            return False
        elif (number_of_live_neigbours==2 or number_of_live_neigbours==3) and indx in self.live_tiles:
            return True
        elif number_of_live_neigbours==3 and indx not in self.live_tiles:
            return True
        else:
            return False
        
    
    def update_state(self):
        to_add = []
        to_remove = []

        for indx in self.gameboard.get_all_tile_indexes():
            if self.tile_is_live_in_next_state(indx):
                to_add.append(indx)
            else:
                to_remove.append(indx)

        for indx in to_add:
            self.add_live_cell(indx)
        for indx in to_remove:
            self.remove_live_cell(indx)


shutdown = False
def close(x,y):
    global shutdown
    shutdown = True

#parameters
map_size = 16
tileSize = 32
number_of_initial_live_tiles = 100


numberOfTiles = [map_size, map_size]
screenSize = [numberOfTiles[0]*(tileSize+1)-1, numberOfTiles[1]*(tileSize+1)-1]

screen = Screen()
screen.setup(screenSize[0], screenSize[1])
screen.setworldcoordinates(-10,-20-screenSize[1], 20+screenSize[0], 10)
screen.bgcolor("black")
screen.tracer(0,0)          #for making drawing instant

screen.onclick(close)

game = Gameboard(numberOfTiles, tileSize, screenSize, screen)
sim = Simulation(game)

random_tuples = np.random.randint(0, map_size, (number_of_initial_live_tiles,2)).tolist()
for tpl in random_tuples:
    sim.add_live_cell(tpl)

while not shutdown:
    sim.update_state()
    screen.update()             #for making drawing instant
    sleep(0.1)

screen.mainloop()