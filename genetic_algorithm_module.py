from utils import TotalRouteDistance
import random, math
from simulated_annealing_module import draw_solution


def initialize_population(packages, vehicles, population_size):
    pop = []  # create a list
    for _ in range(population_size):
        random.shuffle(packages)
        individual = assign_packages(packages[:], vehicles)
        pop.append(individual)
    return pop


def assign_packages(packages, vehicles):
    assignments = [[] for _ in vehicles]
    capacities = [v.capacity for v in vehicles]
    for pkg in packages:
        for i, capacity in enumerate(capacities):
            if capacity >= pkg.weight:
                assignments[i].append(pkg)
                capacities[i] -= pkg.weight
                break
    return assignments


def Cross_Over(parent1, parent2):
    child = [p1 if random.random() > 0.5 else p2 for p1, p2 in zip(parent1, parent2)]
    return child


def FitnessFunction(individual, all_packages):
    assigned_ids = {p.id for route in individual for p in route}
    unassigned = [p for p in all_packages if p.id not in assigned_ids]

    total_distance = sum(TotalRouteDistance(route) for route in individual)

    # Penalize unassigned packages, reward high-priority ones
    penalty = sum(p.weight for p in unassigned) * 10  # weight penalty
    priority_bonus = sum(p.priority for route in individual for p in route)

    return total_distance + penalty - priority_bonus


def mutation(individual, mutationRate=0.1):
    for route in individual:
        if random.random() < mutationRate and len(route) > 1:
            a, b = random.sample(range(len(route)), 2)
            route[a], route[b] = route[b], route[a]
        return individual


def repair_solution(individual, all_packages, vehicles):
    seen = set()
    for route in individual:
        route[:] = [p for p in route if p.id not in seen and not seen.add(p.id)]

    assigned_ids = {p.id for route in individual for p in route}
    unassigned = [p for p in all_packages if p.id not in assigned_ids]

    capacities = [v.capacity - sum(p.weight for p in route) for v, route in zip(vehicles, individual)]

    for pkg in sorted(unassigned, key=lambda x: -x.priority):  # prioritize higher priority
        for i, cap in enumerate(capacities):
            if cap >= pkg.weight:
                individual[i].append(pkg)
                capacities[i] -= pkg.weight
                break
    return individual


def evolve(population, packages, vehicles, generations=50, mutation_rate=0.1):
    for _ in range(generations):
        population = sorted(population, key=lambda ind: FitnessFunction(ind, packages))
        nextGen = population[:2]
        while len(nextGen) < len(population):
            parent1, parent2 = random.choices(population[:10], k=2)
            child = Cross_Over(parent1, parent2)
            child = mutation(child, mutation_rate)
            child = repair_solution(child, packages, vehicles)
            nextGen.append(child)
        population = nextGen
    return min(population, key=lambda ind: FitnessFunction(ind, packages))


class Package:
    def __init__(self, id, x, y, weight, priority):
        self.id = id
        self.x = x
        self.y = y
        self.weight = weight
        self.priority = priority


class Vehicle:
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity


def TotalRouteDistance(packages):
    # Assuming shop is at (0, 0)
    if not packages:
        return 0
    dist = 0
    prev_x, prev_y = 0, 0
    for p in packages:
        dist += math.sqrt((p.x - prev_x) ** 2 + (p.y - prev_y) ** 2)
        prev_x, prev_y = p.x, p.y
    dist += math.sqrt(prev_x ** 2 + prev_y ** 2)  # return to shop
    return dist


def convert_solution_to_vehicles(vehicle_templates, solution):
    vehicles = []
    for i, pkg_list in enumerate(solution):
        vehicle = {
            'id': vehicle_templates[i].id,
            'capacity': vehicle_templates[i].capacity,
            'current_load': 0,
            'assigned_packages': []
        }
        for p in pkg_list:
            vehicle['assigned_packages'].append({
                'id': p.id,
                'x': p.x,
                'y': p.y,
                'weight': p.weight,
                'priority': p.priority
            })
            vehicle['current_load'] += p.weight
        vehicles.append(vehicle)
    return vehicles


def run_genetic_algorithm():
    # test case 2
    # Define vehicles and packages
    vehicles = [Vehicle(1, 60), Vehicle(2, 75)]

    package_dicts = [
        {'id': 1, 'x': 5.0, 'y': 10.0, 'weight': 10.0, 'priority': 1},
        {'id': 2, 'x': 20.0, 'y': 25.0, 'weight': 15.0, 'priority': 2},
        {'id': 3, 'x': 35.0, 'y': 15.0, 'weight': 5.0, 'priority': 3},
        {'id': 4, 'x': 40.0, 'y': 30.0, 'weight': 12.0, 'priority': 1},
        {'id': 5, 'x': 55.0, 'y': 5.0, 'weight': 8.0, 'priority': 4},
        {'id': 6, 'x': 60.0, 'y': 40.0, 'weight': 18.0, 'priority': 2},
        {'id': 7, 'x': 10.0, 'y': 50.0, 'weight': 9.0, 'priority': 5}
    ]

    '''
    # Define packages
    package_dicts = [
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
    ]

     '''

    packages = [Package(**p) for p in package_dicts]
    # Genetic Algorithm Execution
    population = initialize_population(packages, vehicles, population_size=30)
    best_solution = evolve(population, packages, vehicles, generations=100, mutation_rate=0.1)
    final_vehicles = convert_solution_to_vehicles(vehicles, best_solution)

    # Display result
    for v in final_vehicles:
        print(f"Vehicle {v['id']} (Load: {v['current_load']} / {v['capacity']} kg)")
        for p in v['assigned_packages']:
            print(f"  Package {p['id']} at ({p['x']},{p['y']}) weight={p['weight']} priority={p['priority']}")
        print()

    total_distance = sum(TotalRouteDistance([Package(**p) for p in v['assigned_packages']]) for v in final_vehicles)
    total_priority = sum(p['priority'] for v in final_vehicles for p in v['assigned_packages'])

    print(f"Total Traveled Distance: {total_distance:.2f}")
    print(f"Total Priority Score: {total_priority}")

    draw_solution(final_vehicles)