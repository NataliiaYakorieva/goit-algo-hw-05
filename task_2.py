from typing import List, Optional, Tuple


def binary_search_upper_bound(
        array: List[float], target: float) -> Tuple[int, Optional[float]]:
    left: int = 0
    right: int = len(array) - 1
    iterations: int = 0
    upper_bound: Optional[float] = None

    while left <= right:
        iterations += 1
        mid: int = (left + right) // 2
        if array[mid] < target:
            left = mid + 1
        else:
            upper_bound = array[mid]
            right = mid - 1

    return iterations, upper_bound


# Example usage:
test_array = [1.1, 2.5, 3.3, 4.4, 5.5, 6.6]
result = binary_search_upper_bound(test_array, 3.0)
print(result)  # Output: (3, 3.3)
