# Solución al problema de Rutas de vehículos aplicando GNN y CNN

## About
The Vehicle Routing Problem is crucial in the Optimization field and related to various problems in real-life like getting the optimal route to serve a given number of requests. In this way, finding a solution with Neural Networks is important because the time It takes to find a solution would be lower than solving the same problem with other methods. The type of Neural Network that could give better solutions is the Graph Neural Network because it works with graphs that is the way in which this problem is represented.

## Structure / Estructura
├── Dataset                                                                                                                
│···├── Instancias / Inputs                                                                                                
│···│···├── capacidades.npy                                                                                                
│···│···├── demandas.npy                                                                                                   
│···│···└── matrices.npy                                                                                                   
│···├── Scripts                                                                                                            
│···│···├── generarInstancias.py                                                                                           
│···│···├── obtenerTargetsCVRP.py                                                                                          
│···│···└── obtenerTargetsVRP.py                                                                                           
│···└── Targets                                                                                                            
│········├── CVRP                                                                                                           
│········│···├── aristas.npy                                                                                                
│········│···├── cargas.npy                                                                                                 
│········│···└── distancias.npy                                                                                             
│········└── VRP                                                                                                            
│·············├── aristas.npy                                                                                                
│·············└── distancias.npy                                                                                             
├── Models / state_dict                                                                                                    
│···├── CVRP                                                                                                               
│···│···├── CNN.pt                                                                                                         
│···│···├── FNN.pt                                                                                                         
│···│···└── GNN.pt                                                                                                         
│···└── VRP                                                                                                                
│········├── CNN.pt                                                                                                         
│········├── FNN.pt                                                                                                         
│········└── GNN.pt                                                                                                         
├── Solucion al problema de Rutas de Vehiculos aplicando GNN y CNN.ipynb / main code                                       
└── Solucion al problema de Rutas de Vehiculos aplicando GNN y CNN.pdf / Document
