from array import array

def sum(sum_array: array):
    if len(sum_array) == 0:
        return 0
    else:
        return sum_array.pop(0) + sum(sum_array)

print(sum([2, 4, 6, 8, 10]))