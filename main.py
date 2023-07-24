from datetime import datetime
from dui.types import Desire, Event, Person, Religion

if __name__ == '__main__':
    desire = Desire()
    desire[0] = 1
    person = Person(desire)
    religion = Religion("吃甜舒适")

    # TODO: add event feedback
    event1 = Event(
        location="上海南路123号",
        environment="海鲜餐厅",
        time=datetime(2023, 7, 22, 19, 30),
        religion=religion
    )

    print('welcome to D-UI !')
    print(person)
    print(str(event1))
