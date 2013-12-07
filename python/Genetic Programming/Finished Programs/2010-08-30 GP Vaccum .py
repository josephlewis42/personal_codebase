from pyevolve import *
import math
import pprint

NORTH = 0
SOUTH = 2
EAST  = 1
WEST  = 3

lowest_score_yet = 100 #Print out the lowest scores.

loc_x = 1
loc_y = 1
direction = 0

grid = []
def setup_map():
   global grid
   global loc_x
   global loc_y
   global direction
   loc_x = 1
   loc_y = 1
   direction = 2
   grid = [["x","x","x","x","x","x","x","x","x","x","x","x"],
           ["x",0,0,0,0,0,0,0,0,0,0,"x"],
           ["x",0,0,0,0,0,0,0,0,0,0,"x"],
           ["x",0,0,0,0,0,0,0,0,0,0,"x"],
           ["x",0,0,0,0,0,0,0,0,0,0,"x"],
           ["x",0,0,0,0,0,0,0,0,0,0,"x"],  #10x10 Grid, 1-10, 1-10
           ["x",0,0,0,0,0,0,0,0,0,0,"x"],  #Upper Left is 0,0
           ["x",0,0,0,0,0,0,0,0,0,0,"x"],  #Must be refrenced [y][x]
           ["x",0,0,0,0,0,0,0,0,0,0,"x"],
           ["x",0,0,0,0,0,0,0,0,0,0,"x"],
           ["x",0,0,0,0,0,0,0,0,0,0,"x"],
           ["x","x","x","x","x","x","x","x","x","x","x","x"]]

def eval_grid():
   total_zeros = 0
   
   for x in range(len(grid)):
      for y in range(len(grid[x])):
         if grid[y][x] == 0:
            total_zeros += 1

   return total_zeros

def gp_turn_right(z):
   global direction
   direction +=1
   if direction > 3:
      direction = 0
   return wall_on_right()

def gp_turn_left(z):
   global direction
   direction -=1
   if direction < 0:
      direction = 3
   return wall_on_left()

def can_move_forward():
   global direction
   global loc_x
   global loc_y
   global grid
   
   if direction == 0: #North
      a = grid[loc_y - 1][loc_x] != "x"
   if direction == 1: #East
      a = grid[loc_y][loc_x + 1] != "x"
   if direction == 2: #South
      a = grid[loc_y + 1][loc_x] != "x"
   if direction == 3: #West
      a = grid[loc_y][loc_x - 1] != "x"

   if a == True:
      return 1
   else:
      return -1

def wall_on_right():
   global direction
   global loc_x
   global loc_y
   global grid
   
   if direction == 3: #North is on right
      a = grid[loc_y - 1][loc_x] != "x"
   if direction == 0: #East is on right
      a = grid[loc_y][loc_x + 1] != "x"
   if direction == 1: #South is on right
      a = grid[loc_y + 1][loc_x] != "x"
   if direction == 2: #West is on right
      a = grid[loc_y][loc_x - 1] != "x"

   if a == True:
      return 1
   else:
      return -1

def wall_on_left():
   global direction
   global loc_x
   global loc_y
   global grid
   
   if direction == 1: #North is on left
      a = grid[loc_y - 1][loc_x] != "x"
   if direction == 2: #East is on left
      a = grid[loc_y][loc_x + 1] != "x"
   if direction == 3: #South is on left
      a = grid[loc_y + 1][loc_x] != "x"
   if direction == 0: #West is on left
      a = grid[loc_y][loc_x - 1] != "x"

   if a == True:
      return 1
   else:
      return -1

def gp_if_gt_zero(a,b,c):
   if a > 0:
      return b
   else:
      return c

def place_marker():
   global grid
   grid[loc_y][loc_x] = 1

def gp_go_forward(z):
   global loc_x
   global loc_y

   place_marker()

   if can_move_forward() == 1:
      if direction == 0: #NORTH
         loc_y -= 1
      if direction == 1: #EAST
         loc_x += 1
      if direction == 2: #SOUTH
         loc_y += 1
      if direction == 3: #WEST
         loc_x -= 1
   return 1

def gp_go_forward_until_stop(z):
   while can_move_forward() == 1:
      gp_go_forward("")

   return -1
   
error_accum = Util.ErrorAccumulator()


def rangef(min, max, step):
   result = []
   while 1:
      result.append(min)
      min = min+step
      if min>=max:
         break
   return result

def eval_func(chromosome):
   global error_accum
   global lowest_score_yet
   error_accum.reset()
   code_comp = chromosome.getCompiledCode()

   setup_map()
   #print grid

   eval(code_comp, globals(), locals())
   
   evaluated = eval_grid()

   #Print out the significant patterns.
   if evaluated < lowest_score_yet:
      lowest_score_yet = evaluated
      pprint.pprint(grid)
   
   target = 0 #0 empty spaces is target
   error_accum += (target, evaluated)

   return error_accum.getRMSE()

def main_run():
   genome = GTree.GTreeGP()
   genome.setParams(max_depth=10, method="ramped")
   genome.evaluator.set(eval_func)
   ga = GSimpleGA.GSimpleGA(genome)

   ga.setParams(gp_terminals = ['wall_on_right()','wall_on_left()','can_move_forward()'], gp_function_prefix = "gp")

   ga.setMinimax(Consts.minimaxType["minimize"])
   ga.setGenerations(100)
   ga.setMutationRate(0.08)
   ga.setCrossoverRate(1.0)
   ga.setPopulationSize(50)
   ga.evolve(freq_stats=5)
   print ga.bestIndividual()
if __name__ == "__main__":
   main_run()

