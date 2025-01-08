import heapq
import random
import matplotlib.pyplot as plt

class City:
    def __init__(self, name):
        self.name = name
        self.distances = {}  # Dictionary to store distances to other cities
        self.x = random.uniform(0, 100)  # Assigning random X coordinates
        self.y = random.uniform(0, 100)  # Assigning random Y coordinates

    def set_distance(self, other_city, distance):
        self.distances[other_city] = distance

    def __str__(self):
        return self.name


class Node:
    def __init__(self, cities_visited, current_city, g, h, path):
        self.cities_visited = cities_visited  # Set of visited cities
        self.current_city = current_city      # Current city
        self.g = g                            # Actual cost
        self.h = h                            # Heuristic (remaining estimated cost)
        self.f = g + h                        # Total cost
        self.path = path                      # Path taken

    def __lt__(self, other):
        return self.f < other.f  # Comparing total cost


def heuristic(cities, cities_visited, current_city_index):
    # Estimate the remaining distance (heuristic) using the nearest unvisited city
    remaining_cities = [city for index, city in enumerate(cities) if city not in cities_visited]
    if not remaining_cities:
        return 0

    # Use the minimum distance from the remaining cities
    min_distance = min([cities[current_city_index].distances[city] for city in remaining_cities])
    return min_distance


def a_star_tsp(cities, n, start_city):
    # Find the city specified by the user in the list of cities
    start_city_object = None
    for city in cities:
        if city.name == start_city:
            start_city_object = city
            break
    
    if not start_city_object:
        print(f"The city {start_city} is not in the list.")
        return None, None

    start_node = Node(cities_visited={start_city_object}, current_city=start_city_object, g=0, h=0, path=[start_city_object])
    open_list = []
    heapq.heappush(open_list, start_node)

    while open_list:
        current_node = heapq.heappop(open_list)

        # If all cities are visited and we return to the starting city
        if len(current_node.cities_visited) == n:
            if current_node.current_city.distances[start_city_object] != 0:  # Ensure return path exists
                current_node.path.append(start_city_object)
                return current_node.path, current_node.g + current_node.current_city.distances[start_city_object]

        # Explore the next cities that haven't been visited
        for next_city in cities:
            if next_city not in current_node.cities_visited:
                new_cities_visited = current_node.cities_visited | {next_city}
                new_g = current_node.g + current_node.current_city.distances[next_city]
                current_city_index = cities.index(current_node.current_city)
                new_h = heuristic(cities, new_cities_visited, current_city_index)
                new_path = current_node.path + [next_city]
                new_node = Node(cities_visited=new_cities_visited, current_city=next_city, g=new_g, h=new_h, path=new_path)

                heapq.heappush(open_list, new_node)

    return None, None  # If no path is found


def get_input():
    cities = []
    n = int(input("Enter the number of cities: "))

    # Enter city names only
    for i in range(n):
        city_name = input(f"Enter the name of city {i+1}: ")
        x = float(input(f"Enter the X coordinate for city {city_name}: "))
        y = float(input(f"Enter the Y coordinate for city {city_name}: "))
        city = City(city_name)
        city.x = x
        city.y = y
        cities.append(city)

    # Enter the distances between cities in kilometers
    for i in range(n):
        for j in range(i + 1, n):
            while True:
                try:
                    # Clarify that distances are in kilometers
                    distance = float(input(f"Enter the distance between {cities[i]} and {cities[j]} in kilometers: "))
                    if distance < 0:
                        raise ValueError("Distance must be a positive number.")
                    cities[i].set_distance(cities[j], distance)
                    cities[j].set_distance(cities[i], distance)
                    break
                except ValueError as e:
                    print(f"Error: {e}. Please enter a valid distance.")

    return cities


def plot_tour(cities, path):
    # Plot cities as points
    x = [city.x for city in cities]
    y = [city.y for city in cities]
    labels = [city.name for city in cities]

    plt.scatter(x, y, color='blue', marker='o')

    # Place city names next to the points
    for i, label in enumerate(labels):
        plt.text(x[i] + 1, y[i] + 1, label, fontsize=12)

    # Plot the path
    path_x = [city.x for city in path]
    path_y = [city.y for city in path]
    
    # Add line to connect cities in the path
    path_x.append(path[0].x)  # Return to the first city
    path_y.append(path[0].y)
    
    # Plot the path with blue color
    for i in range(len(path) - 1):
        plt.plot([path_x[i], path_x[i + 1]], [path_y[i], path_y[i + 1]], color='blue', linestyle='-', linewidth=2, marker='o')

        # Add arrows to indicate direction
        plt.annotate(
            '', xy=(path_x[i + 1], path_y[i + 1]), xytext=(path_x[i], path_y[i]),
            arrowprops=dict(facecolor='blue', edgecolor='blue', arrowstyle='->', lw=1.5)
        )

    plt.title('Traveling Salesman Tour')
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.show()


def main():
    # Get cities and distances
    cities = get_input()

    # Ask for the starting city
    start_city = input("Enter the starting city: ")

    # Calculate the shortest path using A*
    path, total_cost = a_star_tsp(cities, len(cities), start_city)

    if path is not None:
        # Convert the path from city objects to city names
        city_path = [city.name for city in path]
        print("\nThe optimal path that visits all cities is:")
        print(" -> ".join(city_path))
        print(f"Total cost: {total_cost} kilometers")

        # Plot the optimal path
        plot_tour(cities, path)
    else:
        print("No path found.")


if __name__ == "__main__":
    main()
