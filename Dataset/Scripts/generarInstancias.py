import numpy as np
import random

def generarInstancia(N, V):
   M = np.zeros((N, N))
   f = 0
   demanda = []
   for r in range(N):
      for n in range(f, N):
         if(r == n):
            M[r][n] = 0
         else:
            M[r][n] = random.randint(500, 1500)
            M[n][r] = M[r][n]
      f = f + 1
      
      if(r == 0):
         demanda.append(0)
      else:
         demanda.append(random.randint(1, 8))

   demanda = np.array(demanda)
   capacidad = np.array([random.randint(25, 35)]*V)
   return M, demanda, capacidad

def main():
   instancias = 10_000
   N = 25
   V = 6
   
   matrices, demandas, capacidades = [], [], []

   print("Generando {:,} instancias".format(instancias))
   for i in range(instancias):
      M, demanda, capacidad = generarInstancia(N, V)
      matrices.append(M)
      demandas.append(demanda)
      capacidades.append(capacidad)
      print("\rGenerando...  {:.2%}".format((i+1)/instancias), end=" ")
   print("\nSe generaron {:,} instancias".format(instancias))

   matrices = np.array(matrices, dtype=int)
   demandas = np.array(demandas, dtype=int)
   capacidades = np.array(capacidades, dtype=int)

   np.save("../Instancias/matrices.npy", matrices)
   np.save("../Instancias/demandas.npy", demandas)
   np.save("../Instancias/capacidades.npy", capacidades)

if __name__ == "__main__":
   main()