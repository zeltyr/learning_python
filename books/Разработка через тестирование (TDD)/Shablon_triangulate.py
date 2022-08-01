'''
# создаём первый успешно пройденный тест на сумму двух чисел, но обобщать ещё рано, надо добавить второй тест для других аргументов
def plus(augend:int, addend:int):
    return 4

def testSum():
    assert(4 == plus(3, 1))

testSum()
'''

# пишем второй тест с другими аргрументами и видим, что тест "падает" - значит надо менять реализацию. Это и есть триангуляция
def plus(augend:int, addend:int):
    return augend + addend

def testSum():
    assert(4 == plus(3, 1))
    assert(7 == plus(4, 3))

testSum()
