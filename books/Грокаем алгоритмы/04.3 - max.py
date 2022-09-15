from array import array

def max_array(sum_array: array):
    if len(sum_array) == 1:
        return sum_array[0]
    elif sum_array[0] > sum_array[1]:
        del sum_array[1]
        return max_array(sum_array)
    else:
        del sum_array[0]
        return max_array(sum_array)

print(max_array([2, 21, 6, 8, 3, 0.0, 9]))