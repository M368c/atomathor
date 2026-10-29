from turbo_pump.x3.data_type import encode_data

# a2 | a1 | a0 | * | 0 | n2 | n1 | n0 | l1 | l0 | dn | ... | d0 | c2 | c1 | c0 | Cr |

MIN_LENGTH = 15


def encode(address, parameter, data, action):
    if action == "write":
        function = "1"

        data = encode_data(parameter.data_type, data)
        if data == None:
            return
    elif action == "read":
        function = "0"
    else:
        return None

    if len(data) > 99:
        print("Data too long!")
        return None

    data_length = f"{len(data):02d}"

    msg = f"{address}{function}0{parameter.value}{data_length}{data}"
    checksum_value = sum(msg.encode("ascii")) % 256
    checksum = f"{checksum_value:03d}"
    frame = f"{msg}{checksum}\r\n".encode("ascii")
    return frame


def decode(line):
    try:
        line = line.decode("ascii").strip()
    except:
        print(f"Could not decode line: {line}")
        return None

    if len(line) < MIN_LENGTH:
        print("X3 telegram is not correct")
        return None

    address = line[0:3]
    function = line[3:4]
    parameter = line[5:8]

    try:
        data_length = int(line[8:10])
    except ValueError:
        print("Invalid data length!")
        return None

    data_end = line[10 : 10 + data_length]
    data = line[10:data_end]

    try:
        checksum = int(line[data_end:-1])
    except ValueError:
        print("Invalid checksum!")

    calculated_checksum = sum(line[:data_end].encode("ascii")) % 256

    if calculated_checksum != checksum:
        print("Checksum is not correct!")
        return None

    return address, parameter, data
