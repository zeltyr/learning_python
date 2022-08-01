
class TestCase:
    def __init__(self, name):
        self.name = name
    def SetUp(self):
        pass
    def run(self):
        self.SetUp()
        method = getattr(self, self.name)
        method()
    
class WasRun(TestCase):
    def __init__(self, name):
        TestCase.__init__(self, name)
    def testMethod(self):
        self.wasRun = 1
    def SetUp(self):
        self.wasRun = None
        self.wasSetUp = 1

class TestCaseTest(TestCase):
    def SetUp(self):
        self.test = WasRun("testMethod")
    def testRunning(self):
        self.test.run()
        assert(self.test.wasRun)
    def testSetUp(self):
        self.test.run()
        assert(self.test.wasSetUp)

        
TestCaseTest("testRunning").run()
TestCaseTest("testSetUp").run()