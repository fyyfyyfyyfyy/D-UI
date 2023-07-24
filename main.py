<<<<<<< HEAD
from datetime import datetime
=======
>>>>>>> add-event
from dui.types import Desire, Event, Person, Religion

if __name__ == '__main__':
    desire = Desire()
    desire[0] = 1
    person = Person(desire)
<<<<<<< HEAD
    religion = Religion("吃甜舒适")

    # TODO: add event feedback
    event1 = Event(
        location="上海南路123号",
        environment="海鲜餐厅",
        time=datetime(2023, 7, 22, 19, 30),
        religion=religion
=======
    belief = Religion("吃甜舒适")

    # TODO: add event feedback
    event1 = Event("四川北路666号", "川菜馆", "8:00pm")
    event2 = Event(
        location="上海南路123号",
        environment="海鲜餐厅",
        time="7:30pm",
        belief=belief
>>>>>>> add-event
    )

    print('welcome to D-UI !')
    print(person)
    print(str(event1))
<<<<<<< HEAD
=======
    print(str(event2))
>>>>>>> add-event
