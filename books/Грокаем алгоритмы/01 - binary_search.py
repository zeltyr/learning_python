from array import array


def binary_search(list: array, item: float):
    
    low = 0
    high = len(list) - 1
    
    while low <= high:
        mid = int((low + high) / 2)
        guess = list[mid]
        if guess == item:
            return mid
        if guess < item:
            low = mid + 1
        else:
            high = mid - 1
    return None

my_list = [1, 3, 4, 7, 9]
print(binary_search(my_list, 3))
print(binary_search(my_list, 8))
