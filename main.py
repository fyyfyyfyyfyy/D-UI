from dui.types import Desire, Person

if __name__ == '__main__':
    desire = Desire()
    desire[0] = 1
    person = Person(desire)

    # TODO: add event feedback

    print('welcome to D-UI !')
    print(person)
