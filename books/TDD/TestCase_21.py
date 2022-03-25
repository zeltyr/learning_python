
from logging import exception


class TestCase:
    def __init__(self, name):
        self.name = name
    def SetUp(self):
        pass
    def tearDown(self):
        pass
    def run(self):
        self.SetUp()
        result = TestResult()
        result.testStarted()
        method = getattr(self, self.name)
        method()
        self.tearDown()
        return result
        
class WasRun(TestCase):
    def __init__(self, name):
        TestCase.__init__(self, name)
    def SetUp(self):
        self.log = "SetUp "
    def testMethod(self):
        self.log = self.log + "testMethod "
    def testBrockenMethod(self):
        raise exception
    def tearDown(self):
        self.log = self.log + "tearDown "

class TestResult:
    def __init__(self):
        self.runCount = 0
    def testStarted(self):
        self.runCount = self.runCount + 1
    def summary(self):
        return "%d run, 0 failed" %self.runCount

class TestCaseTest(TestCase):
    def testTemplateMethod(self):
        test = WasRun("testMethod")
        test.run()
        assert("SetUp testMethod tearDown " == test.log)
    def testResult(self):
        test = WasRun("testMethod")
        result = test.run()
        assert("1 run, 0 failed" == result.summary())
    def testFailedResult(self):
        test = WasRun("testBrockenMethod")
        result = test.run()
        assert("1 run, 1 failed" == result.summary())

testTemplateMethod = TestCaseTest("testTemplateMethod").run()
print(testTemplateMethod.summary())
testResult = TestCaseTest("testResult").run()
print(testResult.summary())
testFailedResult = TestCaseTest("testFailedResult").run()
print(testFailedResult.summary())