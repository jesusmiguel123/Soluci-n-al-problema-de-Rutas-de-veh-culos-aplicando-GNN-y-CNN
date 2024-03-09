import numpy as np
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def obteniendoGrafo(data, manager, routing, solution):
   rutas, distancias = [], []
   total_distance = 0
   for vehicle_id in range(data['num_vehicles']):
      r = []
      index = routing.Start(vehicle_id)
      route_distance = 0
      while not routing.IsEnd(index):
         node_index = manager.IndexToNode(index)
         r.append(node_index)
         previous_index = index
         index = solution.Value(routing.NextVar(index))
         route_distance += routing.GetArcCostForVehicle(
            previous_index, index, vehicle_id
         )
      r.append(manager.IndexToNode(index))
      rutas.append(r)
      distancias.append(route_distance)
   aristas = []
   for rut in range(len(rutas)):
      for n in range(len(rutas[rut][:-1])):
         aristas.append([rutas[rut][n], rutas[rut][n+1]])
   return aristas, distancias

def obteniendoSolucion(M, capacidad):
   """Solve the VRP problem."""
   data = {}
   data['distance_matrix'] = M
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

   dimension_name = 'Distance'
   routing.AddDimension(
      transit_callback_index,
      0,                      # no slack
      6000,                   # vehicle maximum travel distance
      True,                   # start cumul to zero
      dimension_name
   )
   distance_dimension = routing.GetDimensionOrDie(dimension_name)
   distance_dimension.SetGlobalSpanCostCoefficient(100)

   search_parameters = pywrapcp.DefaultRoutingSearchParameters()
   search_parameters.first_solution_strategy = (
      routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
   )
   search_parameters.time_limit.FromSeconds(2)
   solution = routing.SolveWithParameters(search_parameters)

   if solution:
      return data, manager, routing, solution
   return None, None, None, None

def main():
   matrices = np.load("../Instancias/matrices.npy")
   capacidades = np.load("../Instancias/capacidades.npy")

   instancias = matrices.shape[0]

   laristas, ldistancias = [], []

   print("Obteniendo solucion de {:,} problemas de VRP".format(instancias))
   for i in range(instancias):
      data, manager, routing, solution = obteniendoSolucion(
         matrices[i].tolist(),
         capacidades[i].tolist()
      )
      if(data != None):
         aristas, distancias = obteniendoGrafo(data, manager, routing, solution)
         laristas.append(aristas)
         ldistancias.append(distancias)
      else:
         laristas.append(np.zeros(np.array(laristas[0]).shape))
         ldistancias.append(np.zeros(np.array(ldistancias[0]).shape))
      print("\rResolviendo...  {:.2%}".format((i+1)/instancias), end=" ")
   print("\nSe obtuvieron solucion de {:,} problemas de VRP".format(instancias))

   laristas = np.array(laristas, dtype=int)
   ldistancias = np.array(ldistancias, dtype=int)

   np.save("../Targets/VRP/aristas.npy", laristas)
   np.save("../Targets/VRP/distancias.npy", ldistancias)

if __name__ == "__main__":
   main()