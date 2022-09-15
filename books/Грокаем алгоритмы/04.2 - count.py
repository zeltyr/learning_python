from array import array

def count(sum_array: array):
    if len(sum_array) == 0:
        return 0
    else:
       del sum_array[0]
       return 1 + count(sum_array)

print(count([2, 2, 6, 8, 10, 0.0, 9]))