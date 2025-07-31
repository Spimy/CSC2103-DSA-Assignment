class MinHeap:
    """
    A simple min-heap implementation for priority queue functionality.
    SOURCE: https://www.geeksforgeeks.org/dsa/introduction-to-min-heap-data-structure/
    SOURCE: https://youtu.be/wGSQ486Y4sc?si=fJbOueLUZk8VB78V
    """

    def __init__(self) -> None:
        self.heap: list[tuple[float, str]] = []
        self.size: int = 0

    def insert(self, item: tuple[float, str]) -> None:
        # Insert item while maintaining the heap property.
        self.heap.append(item)
        self.size += 1
        self._heapify_up(self.size - 1)

    def extract_min(self) -> tuple[float, str] | None:
        # Extract the minimum item from the heap.
        if self.size == 0:
            return None

        min_item = self.heap[0]
        self.heap[0] = self.heap[self.size - 1]
        self.size -= 1
        self.heap.pop()

        if self.size > 0:
            self._heapify_down(0)

        return min_item

    def is_empty(self) -> bool:
        # Check if the heap is empty.
        return self.size == 0

    def _heapify_up(self, index: int) -> None:
        # Maintaining the heap property by moving the item up.
        parent = (index - 1) // 2
        if index > 0 and self.heap[parent][0] > self.heap[index][0]:
            self.heap[parent], self.heap[index] = self.heap[index], self.heap[parent]
            self._heapify_up(parent)

    def _heapify_down(self, index: int) -> None:
        # Maintaining the heap property downwards.
        left = 2 * index + 1
        right = 2 * index + 2
        smallest = index

        if left < self.size and self.heap[left][0] < self.heap[smallest][0]:
            smallest = left
        if right < self.size and self.heap[right][0] < self.heap[smallest][0]:
            smallest = right
        if smallest != index:
            self.heap[index], self.heap[smallest] = (
                self.heap[smallest],
                self.heap[index],
            )
            self._heapify_down(smallest)


"""
Sources used in learning about Dijkstra's Algorithm:
SOURCE: https://www.datacamp.com/tutorial/dijkstra-algorithm-in-python
"""


class DijkstraAlgorithm:

    def solve(
        self, graph: dict[str, list[tuple[str, int]]], source: str
    ) -> dict[str, float] | None:
        # Validate the graph before solving
        if not self._is_valid_graph(graph, source):
            return None

        # To avoid mutating the original graph, we create a copy
        graph_copy: dict[str, list[tuple[str, int]]] = {}
        for vertex, edges in graph.items():
            graph_copy[vertex] = edges[:]

        distances = self._dijkstra(graph_copy, source)
        return distances if distances else None

    def solve_with_paths(
        self, graph: dict[str, list[tuple[str, int]]], source: str
    ) -> tuple[dict[str, float], dict[str, list[str]]] | None:
        # Show the complete path when solving Dijkstra's algorithm
        if not self._is_valid_graph(graph, source):
            return None
        graph_copy: dict[str, list[tuple[str, int]]] = {}
        for vertex, edges in graph.items():
            graph_copy[vertex] = edges[:]

        distances, previous = self._solve_with_path(graph_copy, source)

        # Add all the complete paths
        paths: dict[str, list[str]] = {}
        for vertex in graph_copy:
            if distances[vertex] == float("inf"):
                paths[vertex] = []
            else:
                paths[vertex] = self._reconstruct_path(previous, vertex)

        return distances, paths

    def get_user_graph(self) -> dict[str, list[tuple[str, int]]] | None:
        print("\n=== Graph Input ===")
        print("Enter edges in the format: source destination weight")
        print("Example: 'A B 4' creates edge from A to B with weight 4")
        print("Enter 'done' when finished.\n")

        graph: dict[str, list[tuple[str, int]]] = {}

        # Loop to get user input for graph edges
        while True:
            edge_input = input("Enter edge (or 'done' to finish): ").strip()

            # Use the predefined graph if user skips input
            if not edge_input:
                return None

            if edge_input.lower() == "done":
                break

            # Validate input
            partial_edge = edge_input.split()
            if len(partial_edge) != 3:
                print(
                    "Invalid input. Please enter in the format: source destination weight"
                )
                continue

            source, destination, weight_str = partial_edge

            try:
                weight = int(weight_str)
                if weight < 0:
                    print("Weight must be a non-negative integer.")
                    continue
            except ValueError:
                print("Invalid weight. Please enter a valid integer.")
                continue

            # Add vertices to graph if not already present
            if source not in graph:
                graph[source] = []
            if destination not in graph:
                graph[destination] = []

            # Add edge to graph
            edge_exists = any(dest == destination for dest, _ in graph[source])
            if edge_exists:
                print(f"Edge {source} -> {destination} already exists.")
                continue

            graph[source].append((destination, weight))
            print(f"Added edge: {source} -> {destination} (weight: {weight})")
        return graph

    def print_graph(self, graph: dict[str, list[tuple[str, int]]]) -> None:
        print("\n=== Graph Structure ===")
        for vertex in sorted(graph.keys()):
            edges = graph[vertex]
            if edges:
                edges_str = ", ".join(f"{dest}({weight})" for dest, weight in edges)
                print(f"{vertex}: {edges_str}")
            else:
                print(f"{vertex}: no outgoing edges")

    def print_distances(self, distances: dict[str, float], source: str) -> None:
        print(f"\n=== Shortest Distances from {source} ===")
        for vertex in sorted(distances.keys()):
            dist = distances[vertex]
            if dist == float("inf"):
                print(f"{vertex}: unreachable")
            else:
                print(f"{vertex}: {dist}")

    def print_paths(
        self, distances: dict[str, float], paths: dict[str, list[str]], source: str
    ) -> None:
        # Print the shortest paths from source to all other vertices in the desired format.
        print(f"\n=== Shortest Paths from {source} ===")
        for vertex in sorted(distances.keys()):
            if distances[vertex] == float("inf"):
                print(f"{vertex}: unreachable")
            else:
                path_str = "->".join(paths[vertex])
                print(f"{vertex}: {path_str}")

    def _is_valid_graph(
        self, graph: dict[str, list[tuple[str, int]]], source: str
    ) -> bool:
        # Check if graph is empty or has invalid structure
        if not graph:
            print("Graph is empty.")
            return False

        # Check if source vertex exists
        if source not in graph:
            print(f"Source vertex '{source}' does not exist in the graph.")
            return False

        # Check for negative weights
        for vertex, edges in graph.items():
            for destination, weight in edges:
                if weight < 0:
                    print(
                        f"Negative weight found: {weight} for edge {vertex} -> {destination}."
                    )
                    return False

        # Check if the graph has at least one edge
        has_edges = any(len(edges) > 0 for edges in graph.values())
        if not has_edges:
            print("Graph has no edges.")
            return False

        # When all the above checks pass, the graph is valid
        return True

    def _dijkstra(
        self, graph: dict[str, list[tuple[str, int]]], source: str
    ) -> dict[str, float]:
        # Initialize variables
        distance: dict[str, float] = {}
        for vertex in graph:
            distance[vertex] = float("inf")
        distance[source] = 0

        visited: set[str] = set()
        priority_queue = MinHeap()
        priority_queue.insert((0, source))

        print(f"\nSolving shortest path from {source}...")

        while not priority_queue.is_empty():
            current = priority_queue.extract_min()
            if current is None:
                break

            current_dist, current_vertex = current
            if current_vertex in visited:
                continue

            visited.add(current_vertex)
            print(f"Visiting {current_vertex} (distance: {current_dist})")

            # Check the neighbors of the current vertex
            for neighbour, weight in graph[current_vertex]:
                if neighbour not in visited:
                    new_distance = distance[current_vertex] + weight

                    if new_distance < distance[neighbour]:
                        distance[neighbour] = new_distance
                        priority_queue.insert((new_distance, neighbour))
                        print(f"Updating distance for {neighbour}: {new_distance}")

        return distance

    def get_path(
        self, graph: dict[str, list[tuple[str, int]]], source: str, destination: str
    ) -> list[str] | None:
        # Searching for the shortest path between the source and the destination
        if not self._is_valid_graph(graph, source) or destination not in graph:
            print("Invalid graph or destination vertex does not exist.")
            return None

        # Use Dijkstra's algorithm on the previous vertices
        distances, previous = self._solve_with_path(graph, source)

        if distances[destination] == float("inf"):
            print(f"No path found from {source} to {destination}.")
            return None

        # Restore the path from source to destination using the helper method
        path = self._reconstruct_path(previous, destination)
        return path

    def _solve_with_path(
        self, graph: dict[str, list[tuple[str, int]]], source: str
    ) -> tuple[dict[str, float], dict[str, str | None]]:
        # A modified version of Dijkstra's algorithm that also tracks the previous vertices for path reconstruction
        distance: dict[str, float] = {}
        previous: dict[str, str | None] = {}
        for vertex in graph:
            distance[vertex] = float("inf")
            previous[vertex] = None
        distance[source] = 0

        visited: set[str] = set()
        priority_queue = MinHeap()
        priority_queue.insert((0, source))

        while not priority_queue.is_empty():
            current = priority_queue.extract_min()
            if current is None:
                break

            _, current_vertex = current
            if current_vertex in visited:
                continue

            visited.add(current_vertex)

            for neighbour, weight in graph[current_vertex]:
                if neighbour not in visited:
                    new_distance = distance[current_vertex] + weight

                    if new_distance < distance[neighbour]:
                        distance[neighbour] = new_distance
                        previous[neighbour] = current_vertex
                        priority_queue.insert((new_distance, neighbour))

        return distance, previous

    def _reconstruct_path(
        self, previous: dict[str, str | None], destination: str
    ) -> list[str]:
        """
        Reconstruct the shortest path from source to destination using the previous vertices.
        This method traces back from destination to source using the previous dictionary.
        """
        path: list[str] = []
        current = destination

        # Trace back from destination to source
        while current is not None:
            path.append(current)
            current = previous[current]

        # Reverse the path to get source -> destination order
        path.reverse()
        return path


def problem_2():
    print("Problem 2: Dijkstra's Algorithm")

    solver = DijkstraAlgorithm()

    """
      Default graph representation for testing: 
      { * Made with AI: 
            Graph structure:
            A -> B(4), C(2)
            B -> C(1), D(5)
            C -> D(8), E(10)
            D -> E(2), F(6)
            E -> F(3)
            F -> (no outgoing edges)
      }
      """

    predefined_graph: dict[str, list[tuple[str, int]]] = {
        "A": [("B", 4), ("C", 2)],
        "B": [("C", 1), ("D", 5)],
        "C": [("D", 8), ("E", 10)],
        "D": [("E", 2), ("F", 6)],
        "E": [("F", 3)],
        "F": [],
    }

    # Check if user would want to use predefined graph
    choice = input("Use predefined graph? (y/n): ").strip().lower()

    if choice == "y":
        graph = predefined_graph
    else:
        user_graph = solver.get_user_graph()
        graph = user_graph if user_graph else predefined_graph

    # Display the graph structure for user
    print("\nGraph structure:")
    solver.print_graph(graph)

    # Get the source vertex from the user
    while True:
        print(f"\nAvailable vertices: {', '.join(sorted(graph.keys()))}")
        source = input("Enter the source vertex: ").strip()

        if source in graph:
            break
        else:
            print("Invalid source vertex. Please choose from the available vertices.")

    # Solve via the Dijkstra's algorithm
    result = solver.solve_with_paths(graph, source)

    if result is None:
        print("No solution found.")
        return
    distances, paths = result

    print("\nSolution:")
    solver.print_distances(distances, source)
    solver.print_paths(distances, paths, source)
