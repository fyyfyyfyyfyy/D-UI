from device.eilik import EilikCom

if __name__ == '__main__':
    opened = EilikCom.open(port='com3')
    if not opened:
        print('Failed to connect Eilik.')
        exit(-1)

    EilikCom.execute_action(3039011111)

    while True:
        status = EilikCom.read_status()
        print(status)
