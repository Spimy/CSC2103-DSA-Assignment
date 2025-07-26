# We need to merge two sorted halves of the arr into a single sorted segment
from src.tasks.problem_3 import Sudoku


def merge(arr, left, mid, right):
    print(f"\nMerging left: {arr[left:mid + 1]} and right: {arr[mid + 1:right + 1]}")
    n1 = mid - left + 1 # n1 is the size of the left subarray
    n2 = right - mid #n2 is the size of the right subarray

    # Now, we need to create temp arrays
    L = [0] * n1 # L will hold arr[left...mid]
    R = [0] * n2 # R will hold arr[mid+1...right]

    # Copy data from arr[left...mid] and arr[mid+1...right] to temp arrays L[] and R[]
    for i in range(n1):
        L[i] = arr[left + i]
    for j in range(n2):
        R[j] = arr[mid + 1 + j]

    # initiate variables to traverse L and R respectively
    i = 0
    j = 0
    # k will be the index of the original array 'arr'.
    k = left

    # Now we need a loop to compare the elements of L and R,
    # Then place the smaller one into 'arr'.
    # use the while loop to keep this running until either L or R is exhausted.
    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    # Copy the remaining elements of L[],
    # if there are any
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1

    # Copy the remaining elements of R[],
    # if there are any
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1

    print(f"→ Result after merge: {arr[left:right + 1]}")

# Now we need a recursive function to divide the array and
# call merge() to sort and combine.
def mergeSort(arr, left, right):
    if left < right: # Check whether there is more than one element
        mid = (left + right) // 2 # Find the mid of the array
        print(f"\nDividing: {arr[left:right + 1]} into")
        print(f"  Left: {arr[left:mid + 1]}")
        print(f"  Right: {arr[mid + 1:right + 1]}")

        mergeSort(arr, left, mid) # Now we recursively sort the left half.
        mergeSort(arr, mid + 1, right) # Then we recursively sort the right half
        merge(arr, left, mid, right) # Then we merge it into a sorted array


def problem_1():
    print("problem 1: Merge Sort.")
    while True:
        # Now we ask for the user input then put it into the mergeSort function
        print("Please enter some numbers \n(separate them by spaces. i.e. 9 10 71 3)")
        user_input = input()
        try:
            arr = list(map(int, user_input.strip().split()))
            break # If all the user input are integers, then break out of the while loop
        except ValueError:
            print("Invalid input, please only enter integers separated by spaces.")

    # Now we call mergeSort() to sort the user input
    print(f"\nInitial array: {arr}")
    mergeSort(arr, 0, len(arr) - 1)

    # Now we print the sorted array
    print("Final sorted array:")
    for i in arr:
        print(i, end=" ")
    print()
