def quicksort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return quicksort(left) + middle + quicksort(right)

if __name__ == "__main__":
    test_list = [3, 6, 8, 10, 1, 2, 1]
    print(f"Original list: {test_list}")
    sorted_list = quicksort(test_list)
    print(f"Sorted list: {sorted_list}")

    test_list_empty = []
    print(f"Original list: {test_list_empty}")
    sorted_list_empty = quicksort(test_list_empty)
    print(f"Sorted list: {sorted_list_empty}")

    test_list_single = [5]
    print(f"Original list: {test_list_single}")
    sorted_list_single = quicksort(test_list_single)
    print(f"Sorted list: {sorted_list_single}")

    test_list_duplicates = [4, 2, 4, 1, 3, 2]
    print(f"Original list: {test_list_duplicates}")
    sorted_list_duplicates = quicksort(test_list_duplicates)
    print(f"Sorted list: {sorted_list_duplicates}")
