#!/usr/bin/python


from pyevolve import *
import math

error_accum = Util.ErrorAccumulator()

def gp_add(a, b):
   return a+b
def gp_sub(a,b):
   return a-b
def gp_mul(a, b):
   return a*b
def gp_div(a,b):
   '''
   "Safe" division, if divide by 0, return 1.
   '''
   if b == 0:
      return 1.0
   else:
      return a/(b*1.0)
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
   error_accum.reset()
   code_comp = chromosome.getCompiledCode()
   for x in rangef(-1, 1, .1):
      evaluated = eval(code_comp)
      target = x**2 + x + 1
      error_accum += (target, evaluated)

   return error_accum.getRMSE()

def main_run():
   genome = GTree.GTreeGP()
   genome.setParams(max_depth=5, method="ramped")
   genome.evaluator.set(eval_func)
   ga = GSimpleGA.GSimpleGA(genome)

   ga.setParams(gp_terminals = ['x', '1'], gp_function_prefix = "gp")

   ga.setMinimax(Consts.minimaxType["minimize"])
   ga.setGenerations(100)
   ga.setMutationRate(0.08)
   ga.setCrossoverRate(1.0)
   ga.setPopulationSize(100)
   ga.evolve(freq_stats=5)
   print ga.bestIndividual()
if __name__ == "__main__":
   main_run()

