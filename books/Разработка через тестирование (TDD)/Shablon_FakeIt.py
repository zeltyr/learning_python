from datetime import datetime, timedelta

# Начинаем писать тест: есть дублирование между тестом и кодом
class MyDate:
    def __init__(self, year, month, day):
        self.date = datetime(year, month, day).date()
    def yestarday():
        return datetime(2022, 3, 27).date()

dateTest = MyDate(2022, 3, 27)
assert(dateTest.date == MyDate.yestarday())

# Рефакторинг1 - пытаемся убрать дублирование, брав константу из даты
class MyDate1:
    def __init__(self, year, month, day):
        self.date = datetime(year, month, day).date()
    def yestarday():
        return datetime(2022, 3, 28).date() - timedelta(days = 1)

dateTest = MyDate1(2022, 3, 27)
assert(dateTest.date == MyDate1.yestarday())


# Рефакторинг - убираем дублирование окончательно, убирая константы из рабочего кода
class MyDate2:
    def __init__(self, year, month, day):
        self.date = datetime(year, month, day).date()
    def yestarday():
        return datetime.now() - timedelta(days = 1)

dateTest = MyDate2(2022, 3, 27)
assert(dateTest.date == MyDate2.yestarday().date())