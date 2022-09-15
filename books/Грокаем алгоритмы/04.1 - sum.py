from array import array

def sum(sum_array: array):
    if sum_array == []:
        return 0
    else:
        return sum_array[0] + sum(sum_array[1:])

print(sum([2, 4, 6, 8, 10]))