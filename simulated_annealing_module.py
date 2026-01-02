import math
import random
import copy
import matplotlib.pyplot as plt

# Input vehicles and packages
def input_vehicles():
    vehicles = []
    n = int(input("Enter number of vehicles: "))
    for i in range(n):
        cap = float(input(f"Enter capacity for Vehicle {i+1} (in kg): "))
        vehicles.append({'id': i+1, 'capacity': cap, 'assigned_packages': [], 'current_load': 0})
    return vehicles

def input_packages():
    packages = []
    m = int(input("Enter number of packages: "))
    for i in range(m):
        print(f"\nPackage {i+1}:")
        x = float(input("  Enter x coordinate (0-100 km): "))
        y = float(input("  Enter y coordinate (0-100 km): "))
        weight = float(input("  Enter weight (kg): "))
        priority = int(input("  Enter priority (1=highest, 5=lowest): "))
        packages.append({'id': i+1, 'x': x, 'y': y, 'weight': weight, 'priority': priority})
    return packages

# Random assignment
def assign_packages_randomly(vehicles, packages):
    for v in vehicles:
        v['assigned_packages'] = []
        v['current_load'] = 0

    unassigned_packages = []
    for package in packages:
        random.shuffle(vehicles)
        assigned = False
        for vehicle in vehicles:
            if vehicle['current_load'] + package['weight'] <= vehicle['capacity']:
                vehicle['assigned_packages'].append(package)
                vehicle['current_load'] += package['weight']
                assigned = True
                break
        if not assigned:
            unassigned_packages.append(package)
    return vehicles, unassigned_packages

# Total distance
def calculate_total_distance(vehicles):
    total_distance = 0
    for vehicle in vehicles:
        if not vehicle['assigned_packages']:
            continue
        current_x, current_y = 0, 0
        for package in vehicle['assigned_packages']:
            next_x, next_y = package['x'], package['y']
            distance = math.sqrt((next_x - current_x)**2 + (next_y - current_y)**2)
            total_distance += distance
            current_x, current_y = next_x, next_y
        distance_back = math.sqrt(current_x**2 + current_y**2)
        total_distance += distance_back
    return total_distance

# Priority score
def calculate_priority_score(vehicles):
    score = 0
    for vehicle in vehicles:
        for idx, package in enumerate(vehicle['assigned_packages']):
            score += (idx + 1) * package['priority']
    return score

# Neighbor generation
def generate_neighbor(vehicles):
    new_vehicles = copy.deepcopy(vehicles)
    move_type = random.choice(['move', 'swap_between', 'reorder'])

    if move_type == 'move':
        source = None
        while True:
            candidate = random.choice(new_vehicles)
            if candidate['assigned_packages']:
                source = candidate
                break

        package = random.choice(source['assigned_packages'])

        for target in new_vehicles:
            if target['id'] != source['id'] and target['current_load'] + package['weight'] <= target['capacity']:
                source['assigned_packages'].remove(package)
                source['current_load'] -= package['weight']
                target['assigned_packages'].append(package)
                target['current_load'] += package['weight']
                break

    elif move_type == 'swap_between':
        v1 = v2 = None
        attempts = 0
        while attempts < 10:
            v1 = random.choice(new_vehicles)
            v2 = random.choice(new_vehicles)
            if v1 != v2 and v1['assigned_packages'] and v2['assigned_packages']:
                break
            attempts += 1

        if v1 and v2 and v1['assigned_packages'] and v2['assigned_packages']:
            p1 = random.choice(v1['assigned_packages'])
            p2 = random.choice(v2['assigned_packages'])

            new_load_v1 = v1['current_load'] - p1['weight'] + p2['weight']
            new_load_v2 = v2['current_load'] - p2['weight'] + p1['weight']

            if new_load_v1 <= v1['capacity'] and new_load_v2 <= v2['capacity']:
                v1['assigned_packages'] = [pkg for pkg in v1['assigned_packages'] if pkg['id'] != p1['id']]
                v2['assigned_packages'] = [pkg for pkg in v2['assigned_packages'] if pkg['id'] != p2['id']]
                v1['assigned_packages'].append(p2)
                v2['assigned_packages'].append(p1)
                v1['current_load'] = new_load_v1
                v2['current_load'] = new_load_v2

    elif move_type == 'reorder':
        vehicle = random.choice(new_vehicles)
        if len(vehicle['assigned_packages']) >= 2:
            i, j = random.sample(range(len(vehicle['assigned_packages'])), 2)
            vehicle['assigned_packages'][i], vehicle['assigned_packages'][j] = vehicle['assigned_packages'][j], vehicle['assigned_packages'][i]

    return new_vehicles

# Simulated Annealing
def simulated_annealing(vehicles, packages, initial_temperature=1000, cooling_rate=0.95, stopping_temperature=1):
    current_solution = copy.deepcopy(vehicles)
    current_cost = calculate_total_distance(current_solution)
    current_priority_score = calculate_priority_score(current_solution)

    best_solution = copy.deepcopy(current_solution)
    best_cost = current_cost
    best_priority_score = current_priority_score

    T = initial_temperature

    while T > stopping_temperature:
        for _ in range(100):
            neighbor_solution = generate_neighbor(current_solution)
            neighbor_cost = calculate_total_distance(neighbor_solution)
            neighbor_priority_score = calculate_priority_score(neighbor_solution)

            delta_distance = current_cost - neighbor_cost
            delta_priority = current_priority_score - neighbor_priority_score

            if delta_distance > 0:
                current_solution = neighbor_solution
                current_cost = neighbor_cost
                current_priority_score = neighbor_priority_score

                if current_cost < best_cost or (current_cost == best_cost and current_priority_score < best_priority_score):
                    best_solution = copy.deepcopy(current_solution)
                    best_cost = current_cost
                    best_priority_score = current_priority_score

            elif delta_priority > 0:
                current_solution = neighbor_solution
                current_cost = neighbor_cost
                current_priority_score = neighbor_priority_score

            else:
                acceptance_probability = math.exp(delta_distance / T)
                if random.uniform(0, 1) < acceptance_probability:
                    current_solution = neighbor_solution
                    current_cost = neighbor_cost
                    current_priority_score = neighbor_priority_score

        T *= cooling_rate

    return best_solution, best_cost, best_priority_score

# Drawing
def draw_solution(vehicles, filename='vehicle_routes.png'):
    fig, ax = plt.subplots(figsize=(12, 10))
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    colors = ['red', 'cyan', 'lime', 'yellow', 'orange', 'magenta', 'white', 'pink']
    color_idx = 0

    plt.scatter(0, 0, c='white', marker='s', s=150, label='Shop (0,0)')
    plt.text(2, 2, 'Shop', fontsize=10, color='white')

    for vehicle in vehicles:
        if not vehicle['assigned_packages']:
            continue

        path_x = [0]
        path_y = [0]

        for package in vehicle['assigned_packages']:
            path_x.append(package['x'])
            path_y.append(package['y'])

        path_x.append(0)
        path_y.append(0)

        for i in range(len(path_x) - 1):
            plt.arrow(
                path_x[i], path_y[i],
                path_x[i+1] - path_x[i],
                path_y[i+1] - path_y[i],
                color=colors[color_idx % len(colors)],
                length_includes_head=True,
                head_width=2, head_length=3, alpha=0.8
            )

        for package in vehicle['assigned_packages']:
            plt.scatter(package['x'], package['y'], color=colors[color_idx % len(colors)], s=70)
            plt.text(package['x'] + 1, package['y'] + 1, f"Pkg {package['id']}", fontsize=8, color='white')

        color_idx += 1

    plt.title('Vehicle Delivery Routes', fontsize=16, color='white')
    plt.xlabel('X Coordinate (km)', fontsize=14, color='white')
    plt.ylabel('Y Coordinate (km)', fontsize=14, color='white')
    plt.legend(facecolor='black', edgecolor='white', labelcolor='white')
    plt.grid(True, color='gray', linestyle='--', alpha=0.3)
    plt.xlim(-5, 105)
    plt.ylim(-5, 105)
    plt.savefig(filename, facecolor='black')
    print(f"Plot saved as '{filename}' successfully ")
    plt.show()

# Main
def run_simulated_annealing():
    # vehicles = input_vehicles()
    # packages = input_packages()
    # test case1
    """
    vehicles = [
        {'id': 1, 'capacity': 70, 'assigned_packages': [], 'current_load': 0},
        {'id': 2, 'capacity': 80, 'assigned_packages': [], 'current_load': 0},
        {'id': 3, 'capacity': 60, 'assigned_packages': [], 'current_load': 0}
    ]
    packages = [
        {'id': 1, 'x': 10.0, 'y': 20.0, 'weight': 10.0, 'priority': 2},
        {'id': 2, 'x': 30.0, 'y': 40.0, 'weight': 20.0, 'priority': 1},
        {'id': 3, 'x': 70.0, 'y': 80.0, 'weight': 15.0, 'priority': 3},
        {'id': 4, 'x': 15.0, 'y': 60.0, 'weight': 25.0, 'priority': 2},
        {'id': 5, 'x': 50.0, 'y': 10.0, 'weight': 5.0, 'priority': 4},
        {'id': 6, 'x': 60.0, 'y': 30.0, 'weight': 20.0, 'priority': 2},
        {'id': 7, 'x': 5.0, 'y': 90.0, 'weight': 10.0, 'priority': 5},
        {'id': 8, 'x': 85.0, 'y': 25.0, 'weight': 12.0, 'priority': 3},
        {'id': 9, 'x': 25.0, 'y': 5.0, 'weight': 8.0, 'priority': 1},
        {'id': 10, 'x': 95.0, 'y': 90.0, 'weight': 18.0, 'priority': 2}
    ]"""

    #test case 2
    vehicles = [
        {'id': 1, 'capacity': 60, 'assigned_packages': [], 'current_load': 0},
        {'id': 2, 'capacity': 75, 'assigned_packages': [], 'current_load': 0}
    ]
    packages = [
        {'id': 1, 'x': 5.0, 'y': 10.0, 'weight': 10.0, 'priority': 1},
        {'id': 2, 'x': 20.0, 'y': 25.0, 'weight': 15.0, 'priority': 2},
        {'id': 3, 'x': 35.0, 'y': 15.0, 'weight': 5.0, 'priority': 3},
        {'id': 4, 'x': 40.0, 'y': 30.0, 'weight': 12.0, 'priority': 1},
        {'id': 5, 'x': 55.0, 'y': 5.0, 'weight': 8.0, 'priority': 4},
        {'id': 6, 'x': 60.0, 'y': 40.0, 'weight': 18.0, 'priority': 2},
        {'id': 7, 'x': 10.0, 'y': 50.0, 'weight': 9.0, 'priority': 5}
    ]

    vehicles, _ = assign_packages_randomly(vehicles, packages)
    for v in vehicles:
        print(f"Vehicle {v['id']} (Load: {v['current_load']} / {v['capacity']} kg)")
        for p in v['assigned_packages']:
            print(f"  Package {p['id']} at ({p['x']},{p['y']}) weight={p['weight']} priority={p['priority']}")
        print()
    initial_cost = calculate_total_distance(vehicles)
    initial_priority_score = calculate_priority_score(vehicles)
    print(f"\nInitial total traveled distance: {initial_cost:.2f} km")
    print(f"Initial total priority score: {initial_priority_score}")

    best_solution, best_cost, best_priority_score = simulated_annealing(vehicles, packages)

    print("\nFinal Best Solution After Simulated Annealing:")
    for v in best_solution:
        print(f"Vehicle {v['id']} (Load: {v['current_load']} / {v['capacity']} kg)")
        for p in v['assigned_packages']:
            print(f"  Package {p['id']} at ({p['x']},{p['y']}) weight={p['weight']} priority={p['priority']}")
        print()

    print(f"Best total traveled distance: {best_cost:.2f} km")
    print(f"Best total priority score: {best_priority_score}")

    draw_solution(best_solution)
