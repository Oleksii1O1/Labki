import random

def quicksort(arr, low, high):
    if low < high:

        pivot_index = random.randint(low, high)
        arr[pivot_index], arr[high] = arr[high], arr[pivot_index]
        pivot = arr[high]
        i = low - 1
        
        for j in range(low, high):
            if arr[j] >= pivot:      
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
            
        pivot_final = i + 1
        arr[pivot_final], arr[high] = arr[high], arr[pivot_final]

        left_part  = (low, pivot_final - 1)  
        right_part = (pivot_final + 1, high)           

        quicksort(arr, *left_part)
        quicksort(arr, *right_part)

    return arr


def min_cost(prices, discount):
    if not prices:
        return 0.0

    prices_copy = prices.copy()
    n = len(prices_copy)

    prices_copy = quicksort(prices_copy, 0, n - 1)

    discounted_items_count = n // 3
    total = 0.0

    for i in range(n):
        if i < discounted_items_count:
            total += prices_copy[i] * (1 - discount / 100)
        else:
            total += prices_copy[i]

    return round(total, 2)