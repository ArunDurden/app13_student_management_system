class Test:

    def __init__(self, name, number):
        self.name = name
        self.number = number


class Dummy(Test):

    def __init__(self, name, number):
        super().__init__(name, number)
        self.word = self.name


test = Test("Arun", 4)
print(test.name)
print(test.number)


dummy = Dummy("Arun Pandian", 16)
print(dummy.word)


