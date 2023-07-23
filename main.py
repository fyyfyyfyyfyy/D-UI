from dui.types import Desire, Emotion, Person

if __name__ == '__main__':
    desire = Desire()
    desire[1] = 1
    desire[2] = 1.5
    desire[29] = 2
    print("第二层 [1] is ", desire.second_layer[1])
    print("第一层 [1] is ", desire.first_layer[1])
    print("第一层 [3] is ", desire.first_layer[3])
    person = Person(desire)

    # TODO: add event feedback

    print('welcome to D-UI !')
    print(person)

    # 测试加减乘除
    emotion1 = Emotion()
    print(type(emotion1._value))
    for i in range(1, 6):
        emotion1[i] = i + 1

    emotion2 = Emotion()
    for i in range(1, 6):
        emotion2[i] = i + 2
    print(emotion1._value)
    print(emotion2._value)
    print(emotion1 + emotion2)
    print(emotion2 - emotion1)
    print(emotion1 * 2.2)
