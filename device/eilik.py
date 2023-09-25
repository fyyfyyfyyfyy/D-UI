import datetime
import platform
import struct
import time
from typing import TypedDict

import serial  # type: ignore


def get_default_serial_name() -> str:
    system = platform.system()

    if system == "Windows":
        return "com3"
    elif system == "Darwin":
        return "/dev/tty.usbmodem101"
    else:
        raise ValueError('not prepare for other os system.')
        return "com3"


class EilikMachine:
    _CHECK_TIME: datetime.datetime = datetime.datetime.now()
    _CHECK_DATA: bytearray = bytearray()
    _FRAME_LENGTH: int = 0

    @staticmethod
    def _update_time():
        now = datetime.datetime.now()
        if len(EilikMachine._CHECK_DATA) == 0:
            EilikMachine._CHECK_TIME = now
        elif now - EilikMachine._CHECK_TIME > datetime.timedelta(milliseconds=20):
            EilikMachine._clear_data()

    @staticmethod
    def _clear_data():
        EilikMachine._CHECK_DATA.clear()

    @staticmethod
    def decode_data(data: bytes) -> bytes | None:
        list_data = None
        EilikMachine._update_time()
        for d in data:
            EilikMachine._CHECK_DATA.append(d)
            length = len(EilikMachine._CHECK_DATA)
            if length < 5:
                if length < 3:
                    if d != 0xaa:
                        EilikMachine._clear_data()
            elif length == 5:
                EilikMachine._FRAME_LENGTH = struct.unpack('<H',
                                                           EilikMachine._CHECK_DATA[-2:])[0]
            elif length == EilikMachine._FRAME_LENGTH + 3:
                list_data = bytearray()
                list_data.extend(EilikMachine._CHECK_DATA)
                EilikMachine._clear_data()
            elif length > EilikMachine._FRAME_LENGTH + 3:
                EilikMachine._clear_data()
        return list_data

    @staticmethod
    def _get_checksum(data: bytes) -> int:
        return (~sum(data)) & 0xff

    @staticmethod
    def _encode_data(data: list[int]) -> bytes:
        list_byte: bytearray = bytearray()
        length = len(data) + 4
        list_byte.extend([0xaa, 0xaa, 0xaa])
        list_byte.extend(struct.pack('<H', length))
        list_byte.append(0x60)
        list_byte.extend(data)
        list_byte.append(EilikMachine._get_checksum(list_byte[3:len(list_byte)]))
        return list_byte

    @staticmethod
    def encode_instruction(
        inst1: int | None = None,
        inst2: int | None = None,
        number: int | None = None
    ) -> bytes:

        data = []
        if inst1 is not None:
            data.append(inst1)
        if inst2 is not None:
            data.append(inst2)
        if number is not None:
            data.extend(struct.pack('<I', number))
        return EilikMachine._encode_data(data)


class EilikPressStatus(TypedDict):
    head: bool
    front: bool
    back: bool


DEFAULT_EILIK_PRESS_STATUS: EilikPressStatus = {
    'head': False,
    'front': False,
    'back': False,
}


class EilikCom:
    serial_connection: serial.Serial | None = None

    @staticmethod
    def open(port: str, baudrate: int = 1000000) -> bool:
        EilikCom.serial_connection = serial.Serial(port=port, baudrate=baudrate)
        return EilikCom.serial_connection.is_open

    @staticmethod
    def send_data(data: bytes) -> None:
        if EilikCom.serial_connection and EilikCom.serial_connection.is_open:
            EilikCom.serial_connection.write(data)
        else:
            print('>>> Eilik.serial is closed.')

    @staticmethod
    def read_data() -> bytes | None:
        if EilikCom.serial_connection and EilikCom.serial_connection.is_open:
            data = EilikCom.serial_connection.read_all()
            return EilikMachine.decode_data(data)
        else:
            print('>>> Eilik.serial is closed.')
            return None

    @staticmethod
    def execute_action(action_id: int) -> None:
        data = EilikMachine.encode_instruction(0x02, 0x03, action_id)
        EilikCom.send_data(data)

    @staticmethod
    def read_status(delay_s: float = 0.05) -> EilikPressStatus:
        data_send = EilikMachine.encode_instruction(0x01, 0x01)
        EilikCom.send_data(data_send)
        time.sleep(delay_s)
        data_recv = EilikCom.read_data()
        if data_recv is None:
            return DEFAULT_EILIK_PRESS_STATUS
        else:
            status = EilikCom.data_recv_to_press_status(data_recv[-4:-1])
            return status

    @staticmethod
    def data_recv_to_press_status(data: bytes | None) -> EilikPressStatus:
        if data is None or len(data) < 3:
            print('转换失败')
            return DEFAULT_EILIK_PRESS_STATUS
        # print(list(data))
        status_data: list[bool] = [int(v) >= 2 for v in data[:3]]
        status: EilikPressStatus = {
            'head': status_data[0],
            'front': status_data[1],
            'back': status_data[2],
        }
        return status
