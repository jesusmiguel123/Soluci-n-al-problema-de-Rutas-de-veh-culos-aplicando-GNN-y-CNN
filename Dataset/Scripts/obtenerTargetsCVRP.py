import numpy as np
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def obteniendoGrafo(data, manager, routing, solution):
   rutas, pesos, distancias, cargas = [], [], [], []
   total_distance, total_load = 0, 0
   for vehicle_id in range(data['num_vehicles']):
      r, p = [], []
      index = routing.Start(vehicle_id)
      route_distance, route_load = 0, 0
      while not routing.IsEnd(index):
         node_index = manager.IndexToNode(index)
         r.append(node_index)
         p.append(data['demands'][node_index])
         route_load += data['demands'][node_index]
         previous_index = index
         index = solution.Value(routing.NextVar(index))
         route_distance += routing.GetArcCostForVehicle(
            previous_index, index, vehicle_id
         )
      r.append(manager.IndexToNode(index))
      p.append(0)
      p.pop(0)
      rutas.append(r)
      pesos.append(p)
      distancias.append(route_distance)
      cargas.append(route_load)
   aristas = []
   for rut in range(len(rutas)):
      for n in range(len(rutas[rut][:-1])):
         aristas.append([rutas[rut][n], rutas[rut][n+1], pesos[rut][n]])
   return aristas, distancias, cargas

def obteniendoSolucion(M, demanda, capacidad):
   """Solve the CVRP problem."""
   data = {}
   data['distance_matrix'] = M
   data['demands'] = demanda
   data['vehicle_capacities'] = capacidad
   data['num_vehicles'] = len(capacidad)
   data['depot'] = 0
   
   manager = pywrapcp.RoutingIndexManager(
      len(data['distance_matrix']),
      data['num_vehicles'],
      data['depot']
   )
   routing = pywrapcp.RoutingModel(manager)
   
   def distance_callback(from_index, to_index):
      """Returns the distance between the two nodes."""
      from_node = manager.IndexToNode(from_index)
      to_node = manager.IndexToNode(to_index)
      return data['distance_matrix'][from_node][to_node]

   transit_callback_index = routing.RegisterTransitCallback(distance_callback)
   routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

   def demand_callback(from_index):
      """Returns the demand of the node."""
      from_node = manager.IndexToNode(from_index)
      return data['demands'][from_node]

   demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
   routing.AddDimensionWithVehicleCapacity(
      demand_callback_index,
      0,                            # null capacity slack
      data['vehicle_capacities'],   # vehicle maximum capacities
      True,                         # start cumul to zero
      'Capacity'
   )

   search_parameters = pywrapcp.DefaultRoutingSearchParameters()
   search_parameters.first_solution_strategy = (
      routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
   )
   search_parameters.local_search_metaheuristic = (
      routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
   )
   search_parameters.time_limit.FromSeconds(1)
   solution = routing.SolveWithParameters(search_parameters)

   if solution:
      return data, manager, routing, solution
   return None, None, None, None

def main():
   matrices = np.load("../Instancias/matrices.npy")
   demandas = np.load("../Instancias/demandas.npy")
   capacidades = np.load("../Instancias/capacidades.npy")

   instancias = matrices.shape[0]

   laristas, ldistancias, lcargas = [], [], []

   print("Obteniendo solucion de {:,} problemas de CVRP".format(instancias))
   for i in range(instancias):
      data, manager, routing, solution = obteniendoSolucion(
         matrices[i].tolist(),
         demandas[i].tolist(),
         capacidades[i].tolist()
      )
      if(data != None):
         aristas, distancias, cargas = obteniendoGrafo(data, manager, routing, solution)
         laristas.append(aristas)
         ldistancias.append(distancias)
         lcargas.append(cargas)
      else:
         laristas.append(np.zeros(np.array(laristas[0]).shape))
         ldistancias.append(np.zeros(np.array(ldistancias[0]).shape))
         lcargas.append(np.zeros(np.array(lcargas[0]).shape))
      print("\rResolviendo...  {:.2%}".format((i+1)/instancias), end=" ")
   print("\nSe obtuvieron solucion de {:,} problemas de CVRP".format(instancias))

   laristas = np.array(laristas, dtype=int)
   ldistancias = np.array(ldistancias, dtype=int)
   lcargas = np.array(lcargas, dtype=int)

   np.save("../Targets/CVRP/aristas.npy", laristas)
   np.save("../Targets/CVRP/distancias.npy", ldistancias)
   np.save("../Targets/CVRP/cargas.npy", lcargas)

if __name__ == "__main__":
   main()