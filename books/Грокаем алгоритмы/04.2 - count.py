from array import array

def count(count_array: array):
    if count_array == []:
        return 0
    else:
       return 1 + count(count_array[1:])

print(count([2, 2, 6, 8, 10, 0.0, 9]))