# A-Path-Finding-Algorithm
The A* algorithm is a search algorithm that finds the shortest path between a start and an end node while navigating around obstacles. It’s widely used because of its efficiency, balancing path accuracy and computational cost by combining two key factors:
1. G-Score: The actual cost from the start node to the current node.
2. H-Score (Heuristic): The estimated cost from the current node to the end node.
3. The A* algorithm maintains a priority queue (open set) where nodes are prioritized based on their F-Score:<br />
   F = G + H <br />
   G represents the known path cost so far.
   H represents the heuristic estimation of remaining cost.

● The algorithm progresses as follows:
Initialize the Start Node in the priority queue with an F-Score based solely on the heuristic to the end node.
Expand Nodes with the lowest F-Score, updating neighbors' scores if a shorter path is found.
Repeat until reaching the end node, where the path can then be reconstructed.

● Heuristic Function
The heuristic function, H(p1, p2), estimates the distance from any node p1 to the target node p2. For this implementation, we use Manhattan Distance, particularly suited for grid-based movement:
𝐻(𝑝1,𝑝2) = ∣𝑥1−𝑥2∣ + ∣𝑦1−𝑦2∣ 
x1, y1 and x2, y2 represent the coordinates of the two points.
The Manhattan Distance is optimal for grids with vertical and horizontal movement (like this project), as it directly adds the differences in the x and y positions.
Using this heuristic helps the A* algorithm prioritize nodes that seem closest to the end, efficiently guiding the search while navigating around obstacles.

# How the Code Works
Setting Up the Grid:
The program creates a square grid with 50 rows and columns. Each square in this grid is called a "spot" (or "node"), which can either be a normal path, a starting point, an endpoint, or an obstacle (a wall).
You can click on spots to mark the start and end positions, or create obstacles. Obstacles are just squares that block the path.
Color System:

● Different colors help us see what’s happening:
1. Orange: Starting point
2. Turquoise: Endpoint
3. White: Open path (unvisited)
4. Black: Obstacle
5. Red: Already checked paths (closed)
6. Green: Paths that the program is considering (open)

# A* Algorithm in Action:
The A* algorithm uses the starting point (orange) and end point (turquoise) to try to find the shortest path.
It explores neighboring spots from the start point, deciding which spots to check based on two things:
How far a spot is from the start (the G-Score).
How close it seems to be to the end (the H-Score, calculated as a straight-line or "Manhattan" distance).

How the Program Chooses the Next Spot:
At each step, the program picks the spot with the smallest total distance (a combination of how far it is from the start and how close it might be to the end).
It keeps track of spots it has already checked (these turn red), spots it’s currently checking (these turn green), and spots that are part of the path it’s building (these turn purple).

Building the Path:
When the program finally reaches the endpoint, it goes back through each step it took to create a clear path from start to end.
This final path is shown in purple, and the endpoint remains turquoise.

The Heuristic Function (H-Score):
The h function estimates the distance between two spots using the "Manhattan distance" — it’s like counting how many moves it would take if you could only move straight along rows or columns.
This helps the program decide which directions seem more promising and avoid wasting time on unnecessary paths.

Playing With the Code
Start: Left-click on a spot to set the start (orange).
End: Left-click on another spot to set the end (turquoise).
Obstacles: Left-click on other spots to set obstacles (black).
Run the Algorithm: Press the space bar to start the A* algorithm. It will try to find the shortest path from the start to the end, avoiding the obstacles.
Clear the Board: Press the comma (,) key to clear the board and start over.
