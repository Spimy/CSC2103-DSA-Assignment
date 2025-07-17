from tasks.problem_1 import problem_1
from tasks.problem_2 import problem_2
from tasks.problem_3 import problem_3


if __name__ == "__main__":
    print("DSA Assignment - Problem Selection")
    print("1. Run Problem 1")
    print("2. Run Problem 2")
    print("3. Run Problem 3")

    try:
        choice = int(input("Enter problem number to run (1-3): "))
        print()

        if choice == 1:
            problem_1()
        elif choice == 2:
            problem_2()
        elif choice == 3:
            problem_3()
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 3.")
