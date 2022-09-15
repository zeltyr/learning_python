from array import array

def quicksort(ar: array):
    if len(ar) < 2:
        return ar
    else:
        pivot = ar[0]
        less = [i for i in ar[1:] if i < pivot]
        greater = [i for i in ar[1:] if i > pivot]
        return quicksort(less) + [pivot] + quicksort(greater)

print(quicksort([10, 5, 2, 3]))
