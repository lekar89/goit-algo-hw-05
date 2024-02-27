def binary_search(arr, target):
    iterations = 0
    upper_bound = None

    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        iterations += 1

        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
            upper_bound = arr[mid] 

    return iterations, upper_bound