
class TestCase:
    def __init__(self, name):
        self.name = name
    def SetUp(self):
        pass
    def tearDown(self):
        pass
    def run(self):
        self.SetUp()
        method = getattr(self, self.name)
        method()
        self.tearDown()
        
class WasRun(TestCase):
    def __init__(self, name):
        TestCase.__init__(self, name)
    def SetUp(self):
        self.log = "SetUp "
    def testMethod(self):
        self.log = self.log + "testMethod "
    def tearDown(self):
        self.log = self.log + "tearDown "

class TestCaseTest(TestCase):
    def testTemplateMethod(self):
        test = WasRun("testMethod")
        test.run()
        assert("SetUp testMethod tearDown " == test.log)
        
print(TestCaseTest("testTemplateMethod").run())
