def quick_sort_0(arr):
    # Визначаємо змінні лише якщо масив потребує сортування
    if len(arr) > 1:
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x[0] < pivot[0]]
        middle = [x for x in arr if x[0] == pivot[0]]
        right = [x for x in arr if x[0] > pivot[0]]

    return arr if len(arr) <= 1 else quick_sort_0(left) + middle + quick_sort_0(right)