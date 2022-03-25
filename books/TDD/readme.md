# Пример разработки через тестирование

Повторение учебного примера из книги "Экстремальное программирование"
Мне удобнее, когда решения в разных файлах для анализа изменений, поэтому у меня несколько версий исходных файлов решений...

## Шаги разработки примера

1. Пишем первый тест

    ```py
    test = WasRun("testMethod")
    print(test.wasRun)
    test.testMethod()
    print(test.wasRun)
    ```

2. Начинаем исправлять ошибки
  
    * Определяем класс WasRun

        ```py
        class WasRun:
            pass
        ```

    * Определяем конструктор класса ```__init__```

        ```py
        class WasRun:
            def __init__(self, name):
                self.wasRun = None
        ```

    * Добавление метода ```testMethod```

        ```py
        class WasRun:
            def __init__(self, name):
                self.wasRun = None
            def testMethod(self):
                pass
        ```

    * Меняем значение флага ```wasRun``` на 1

        ```py
        class WasRun:
            def __init__(self, name):
                self.wasRun = None
            def testMethod(self):
                self.wasRun = 1
        ```

3. Меняем интерфейс вызова тестового метода на реальный интерфейс

    ```py
    class WasRun:
        def __init__(self, name):
            self.wasRun = None
        def testMethod(self):
            self.wasRun = 1
        def run(self):
            self.testMethod()

    test = WasRun("testMethod")
    print(test.wasRun)
    test.run()
    print(test.wasRun)
    ```

4. Проводим рефакторинг

    Выдержка из книги:
    "Одной из отличительных особенностей языка python являет возможность использования имен классов и методов в качестве функций...
    ... Получив такой атрибут, мы можем обратиться к нему как к функции..."

    ```py
    class WasRun:
        def __init__(self, name):
            self.wasRun = None
            self.name = name
        def testMethod(self):
            self.wasRun = 1
        def run(self):
            method = getattr(self, self.name)
            method()

    test = WasRun("testMethod")
    print(test.wasRun)
    test.run()
    print(test.wasRun)
    ```

5. Развиваем программу и вводим суперкласс ```TestCase```, а класс ```WasRun``` делаем производным классом

    ```py
    class TestCase:
        def __init__(self, name):
            self.name = name
        
    class WasRun(TestCase):
        def __init__(self, name):
            self.wasRun = None
            TestCase.__init__(self, name)
        def testMethod(self):
            self.wasRun = 1
        def run(self):
            method = getattr(self, self.name)
            method()
    ```

6. Проводим рефакторинг: видно, что метод run использует атрибуты суперкласса и не использует атрибуты производного класса, а значит метод можно перенести

    ```py
    class TestCase:
        def __init__(self, name):
            self.name = name
        def run(self):
            method = getattr(self, self.name)
            method()
    ```

7. Продолжаем рефакторинг - создаём отдельный производный класс для запуска нашего первого теста и заменяем ```print``` на ```assert```

    ```py
    class TestCase:
        def __init__(self, name):
            self.name = name
        def run(self):
            method = getattr(self, self.name)
            method()
        
    class WasRun(TestCase):
        def __init__(self, name):
            self.wasRun = None
            TestCase.__init__(self, name)
        def testMethod(self):
            self.wasRun = 1

    class TestCaseTest(TestCase):
        def testRunning(self):
            test = WasRun("testMethod")
            assert(not test.wasRun)
            test.run()
            assert(test.wasRun)
            
    TestCaseTest("testRunning").run()
    ```

8. Добавляем функцию setUp

    * Вставляем инициализацию метода ```setUp``` и флага ```wasSetUp``` в наши алгоритмы

        ```py

            # TestCase
            def SetUp(self):
                pass
            def run(self):
                self.SetUp()
                method = getattr(self, self.name)
                method()
                
            # WasRun
            def SetUp(self):
                self.wasSetUp = 1

            # TestCaseTest
            def testSetUp(self):
                test = WasRun("testMethod")
                test.run()
                assert(not test.wasSetUp)
            
            # Команды запуска тестов
            TestCaseTest("testRunning").run()
            TestCaseTest("testSetUp").run()

        ```

    * Оптимизируем алгоритмы

        ```py
            # WasRun - изменили место инициализации флага wasRun
            def __init__(self, name):
                TestCase.__init__(self, name)
            def testMethod(self):
                self.wasRun = 1
            def SetUp(self):
                self.wasRun = None
                self.wasSetUp = 1

            # TestCaseTest - 2 разных теста не могут быть взаимозависимы, 
            # поэтому можно вынести инициализацию объекта WasRun в функцию SetUp
            def SetUp(self):
                self.test = WasRun("testMethod")
            def testRunning(self):
                self.test.run()
                assert(self.test.wasRun)
            def testSetUp(self):
                self.test.run()
                assert(not self.test.wasSetUp)
        ```

9. Готовимся к внедрению функции ```tearDown``` (высвобождение ресурсов)  (глава 20 - убираем со стола...)

    * Меням флаги на строку лога (ибо флагов становится слишком много)

         ```py
            # WasRun
            def testMethod(self):
                self.wasRun = 1
                self.log = self.log + "testMethod "
            def SetUp(self):
                self.wasRun = None
                self.log = "SetUp "

            # TestCaseTest(TestCase):
            def testSetUp(self):
                self.test.run()
                assert("SetUp testMethod " == self.test.log)
            
            ```

    * Оптимизируем код под использование журнала и добавляем тесты для функции ```tearDown```
      * в моей версии книги под это был старый пример кода, пришлось дописывать так, как считаю нужным

         ```py
            # TestCase:
            def tearDown(self):
                pass
            def run(self):
                self.SetUp()
                method = getattr(self, self.name)
                method()
                self.tearDown()
                
            # WasRun:
            def SetUp(self):
                self.log = "SetUp "
            def testMethod(self):
                self.log = self.log + "testMethod "
            def tearDown(self):
                self.log = self.log + "tearDown "

            # TestCaseTest
            # Тут убрали методы, которые по сути дублировали друг друга и заменили всё одним универсальным
            def testTemplateMethod(self):
                test = WasRun("testMethod")
                test.run()
                assert("SetUp testMethod tearDown " == test.log)
                
            TestCaseTest("testTemplateMethod").run()            
        ```

10. Вывод результата работы тестов (глава 21 - учет и контроль)

    * Вводим новый класс ```TestResult```, который будет аккумулировать состояния тестов

        ```py
        # TestCase:
        def run(self):
            self.SetUp()
            method = getattr(self, self.name)
            method()
            self.tearDown()
            return TestResult()
        
        # TestResult
        class TestResult:
            def summary(self):
                return "1 run, 0 failed"
        
        # TestCaseTest(TestCase):
        def testResult(self):
            test = WasRun("testMethod")
            result = test.run()
            assert("1 run, 0 failed" == result.summary())
        
        # вызов
        testResult = TestCaseTest("testResult").run()
        print(testResult.summary())
        ```

    * Настраиваем счетчик успешных тестов

        ```py
        # TestCase:
            def run(self):
                self.SetUp()
                result = TestResult()
                result.testStarted()
                method = getattr(self, self.name)
                method()
                self.tearDown()
                return result
                
        # TestResult:
            def __init__(self):
                self.runCount = 0
            def testStarted(self):
                self.runCount = self.runCount + 1
            def summary(self):
                return "%d run, 0 failed" %self.runCount
        ```

    * Подготавливаемся к перехвату проваленных тестов

        ```py
        # WasRun(TestCase):
            def testBrockenMethod(self):
                raise exception

        # TestCaseTest(TestCase):
            def testFailedResult(self):
                test = WasRun("testBrockenMethod")
                result = test.run()
                assert("1 run, 1 failed" == result.summary())

        testFailedResult = TestCaseTest("testFailedResult").run()
        print(testFailedResult.summary())
        ```

11. Учет проваленных тестов

    * Ввод новых методов testStarted() и testFailed() для генерации правильного результата тестирования

        ```py
        # TestResult:
            def __init__(self):
                self.runCount = 0
                self.errorCount = 0
            def testStarted(self):
                self.runCount = self.runCount + 1
            def testFailed(self):
                self.errorCount = self.errorCount + 1
            def summary(self):
                return "%d run, %d failed" %(self.runCount, self.errorCount) 

        # TestCaseTest(TestCase):
            def testFailedResultFormatting(self):
                result = testResult()
                result.testStarted()
                result.testFailed()
                assert("1 run, 1 failed" == result.summary())

        testFailedResultFormatting = TestCaseTest("testFailedResultFormatting").run()
        print(testFailedResultFormatting.summary())
        ```

    * Вызов добавленных обработчиков

        ```py
        # TestCase
            def run(self):
                
                self.SetUp()
                result = TestResult()
                result.testStarted()
                
                try:
                    method = getattr(self, self.name)
                    method()
                except:
                    result.testFailed()
                self.tearDown()
                return result

        testFailedResultFormatting = TestCaseTest("testFailedResultFormatting").run()
        print(testFailedResultFormatting.summary())
        ```

12. Создаём набор тестов

    * Подготавливаем новый класс для запуска набора тестов ```TestSuite```

        ```py
        # TestSuite
        class TestSuite:
            def __init__(self):
                self.tests = []
            def add(self, test):
                self.tests.append(test)
            def run(self):
                result = testResult()
                for test in self.tests:
                    test.run(result)
                return result

        # TestCaseTest(TestCase):
            def testSuite(self):
                suite = TestSuite()
                suite.add(WasRun("testMethod"))
                suite.add(WasRun("testBrockenMethod"))
                result = suite.run()
                assert("2 run, 1 failed" == result.summary())
        ```

    * Оптимизируем вызов ```TestSuite``` в классе  ```TestCaseTest```

        ```py
        # TestCaseTest(TestCase):
            def testTemplateMethod(self):
                test = WasRun("testMethod")
                result = TestResult()
                test.run(result)
                assert("SetUp testMethod tearDown " == test.log)
            def testResult(self):
                test = WasRun("testMethod")
                result = TestResult()
                test.run(result)
                assert("1 run, 0 failed" == result.summary())
            def testFailedResult(self):
                test = WasRun("testBrockenMethod")
                result = TestResult()
                test.run(result)
                assert("1 run, 1 failed" == result.summary())
            def testFailedResultFormatting(self):
                result = TestResult()
                result.testStarted()
                result.testFailed()
                assert("1 run, 1 failed" == result.summary())
            def testSuite(self):
                suite = TestSuite()
                suite.add(WasRun("testMethod"))
                suite.add(WasRun("testBrockenMethod"))
                result = TestResult()
                suite.run(result)
                assert("2 run, 1 failed" == result.summary())

        suite = TestSuite()
        suite.add(TestCaseTest("testTemplateMethod"))
        suite.add(TestCaseTest("testResult"))
        suite.add(TestCaseTest("testFailedResultFormatting"))
        suite.add(TestCaseTest("testFailedResult"))
        suite.add(TestCaseTest("testSuite"))

        result = TestResult()
        suite.run(result)

        print(result.summary())
        ```

    * Переносим инициализацию предварительных настроек в метод ```SetUp``` класса ```TestSuite```

        ```py
        # TestCaseTest(TestCase):
            def SetUp(self):
                self.result = TestResult()
            def testTemplateMethod(self):
                test = WasRun("testMethod")
                test.run(self.result)
                assert("SetUp testMethod tearDown " == test.log)
            def testResult(self):
                test = WasRun("testMethod")
                test.run(self.result)
                assert("1 run, 0 failed" == self.result.summary())
            def testFailedResult(self):
                test = WasRun("testBrockenMethod")
                test.run(self.result)
                assert("1 run, 1 failed" == self.result.summary())
            def testFailedResultFormatting(self):
                self.result.testStarted()
                self.result.testFailed()
                assert("1 run, 1 failed" == self.result.summary())
            def testSuite(self):
                suite = TestSuite()
                suite.add(WasRun("testMethod"))
                suite.add(WasRun("testBrockenMethod"))
                suite.run(self.result)
                assert("2 run, 1 failed" == self.result.summary())
        ```
