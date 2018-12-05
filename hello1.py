"""Person."""


class Person:
    """."""

    def __init__(self, name, age):
        """."""
        self.name = name
        self.age = age

    def sayhello(self, has_sayhello=True):
        """."""
        self.has_sayhello = has_sayhello
        print('My name1 is:', self.name)
        print('My age1 is:', self.age)

    def sayhello2(self):
        """."""
        # try:self.has_sayhello
        # except:pass
        # else:
        if hasattr(self, "has_sayhello"):
            if self.has_sayhello:
                print(self.name, "has said hello")
            else:
                print(self.name, "has not said hello")


p = Person('Bill', 10)
p.sayhello()
# p.sayhello(False)
p.sayhello2()
