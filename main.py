#1221124 Rand Saleh and 1221636 Roa Makhtoub
from simulated_annealing_module import run_simulated_annealing
from genetic_algorithm_module import run_genetic_algorithm


def main():
    print("Which algorithm do you want to run?")
    print("1 - Simulated Annealing")
    print("2 - Genetic Algorithm")

    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        run_simulated_annealing()
    if choice == '2':
        run_genetic_algorithm()


    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
