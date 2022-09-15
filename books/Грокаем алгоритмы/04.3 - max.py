from array import array

def max(max_array: array):
    if len(max_array) == 2:
        return max_array[1] if max_array[1] > max_array[0] else max_array[0]
    else:
        sub_max = max(max_array[1:])
        return sub_max if sub_max > max_array[0] else max_array[0]

print(max([2, 21, 63, 8, 3, 0.0, 9]))