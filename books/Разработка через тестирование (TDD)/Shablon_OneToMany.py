# написать алгоритм, который должен суммировать элементы коллекции

'''
# Шаг 1 - простая реализация алгоритма и теста для 1 элемента
def testSum():
    assert (5 == sum(5))

def sum(value: int):
    return value
'''

'''
# Шаг 2 - Используя шаблон "Изоляция изменения", вводим второй параметр
def testSum():
    assert (5 == sum(5, [5]))

def sum(value: int, values):
    return value
'''    

'''
# Шаг 3 - реализуем новый алгоритм
def testSum():
    assert (5 == sum(5, [5]))

def sum(value: int, values):
    sum = 0
    for value in values:
        sum = sum + value
    return sum
'''    
# Шаг 4 - удаляем переменную, ставшую ненужной
def testSum():
    assert (5 == sum([2, 3]))

def sum(values):
    sum = 0
    for value in values:
        sum = sum + value
    return sum

testSum()