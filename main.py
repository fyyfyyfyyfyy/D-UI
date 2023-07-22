from dui.types import Desire, Event, Person, Religion

if __name__ == '__main__':
    desire = Desire()
    desire[0] = 1
    person = Person(desire)
    belief = Religion("吃甜舒适")

    # TODO: add event feedback
    event1 = Event("四川北路666号", "川菜馆", "8:00pm")
    event2 = Event(
        location="上海南路123号",
        environment="海鲜餐厅",
        time="7:30pm",
        belief=belief
    )

    print('welcome to D-UI !')
    print(person)
    print(str(event1))
    print(str(event2))
