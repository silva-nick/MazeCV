## MazeCV

_Uses OpenCV to solve mazes from pictures using graph search algorithms_

#### Basic layout:

- main: takes image input and creates a graph and prints
- graph: creates a graph from points and edges
- BFS: breadth first search code
- A\*: A-Star search algorithm
- Iterative DFS: search using iterative deepening
- skeletonize: Zhang-Suen and my skeletonize methods

\*Not a very efficient solution because to create the graph from the image I run a bfs which could pretty easily solve the maze, however the implementation allows for other path finding algorithms to be tried in the future
