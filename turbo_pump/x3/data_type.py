from enum import Enum, auto


class DataType(Enum):
    BooleanOld = auto()
    UInteger = auto()
    UReal = auto()
    String = auto()
    BooleanNew = auto()
    UShortInt = auto()
    Exponential = auto()
    String16 = auto()
    String8 = auto()


def encode_data(data_type, data):
    if data_type == DataType.BooleanOld:
        if data == True or data == "true" or data == "True":
            return "111111"
        elif data == False or data == "false" or data == "False":
            return "000000"
        else:
            return None

    elif data_type == DataType.UInteger:  # 0-999999
        try:
            data_int = int(data)
        except (ValueError, TypeError):
            return None

        if 0 <= data_int <= 999999:
            return f"{data_int:06d}"
        else:
            return None

    elif data_type == DataType.UReal:  # 0.0-9999.99
        try:
            data_float = float(data)
        except (ValueError, TypeError):
            return None

        value = round(data_float * 100)
        if 0 <= value <= 999999:
            return f"{value:06d}"
        else:
            return None

    elif data_type == DataType.String:
        if len(data) <= 6:
            return data
        else:
            return None

    elif data_type == DataType.BooleanNew:
        if data == True or data == "true" or data == "True":
            return "1"
        elif data == False or data == "false" or data == "False":
            return "0"
        else:
            return None

    elif data_type == DataType.UShortInt:  # 000-999
        try:
            data_int = int(data)
        except (ValueError, TypeError):
            return None

        if 0 <= data_int <= 999:
            return f"{data_int:03d}"
        else:
            return None

    elif data_type == DataType.Exponential:
        try:
            data_float = float(data)
        except (ValueError, TypeError):
            return None

        value = data_float
        if value < 0:
            return None
        if value == 0:
            return "000000"
        mantissa, exp = f"{value:.3e}".split("e")
        exp_code = int(exp) + 20
        if 0 <= exp_code <= 99:
            return mantissa.replace(".", "") + f"{exp_code:02d}"
        return None

    elif data_type == DataType.String16:
        if len(data) <= 16:
            return data
        else:
            return None

    elif data_type == DataType.String8:
        if len(data) <= 8:
            return data
        else:
            return None
