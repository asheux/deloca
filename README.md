# DeLoca

![deloca](data/deloca.png?raw=true)

A system that use a heuristic algorithm to solve the travelling salesman problem (TSP)
which is a popular problem that is categorised as a combinatorial optimization. The system applies heuristic
techniques to try and optimise a route delivery that will allow meeting all delivery deadlines
while travelling the least number of miles.

For this project uses a heuristic algorithm called 2-opt to develop an effective and efficient
solution. The whole idea behind 2-opt is to take an initial route that crosses over itself and gradually
improve it using local search until it reaches a local optimum and no more improvements can be made
(improvement is done through reordering or swapping).

### Run

```
$ python run.py
```
