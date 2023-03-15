from Generator import Generator

gnrt = Generator(12345)


def encode_file(filename_read: str, filename_write: str, keys: str, encode: bool):
    if encode:
        save_keys(gnrt)
    if not encode:
        load_keys(gnrt)
    with open(filename_read, 'rb') as fr:
        bytes_array = []
        while True:
            byte = fr.read(1)
            if not byte:
                break
            info_bits = int.from_bytes(byte, byteorder='big')
            random_number = gnrt.generate_number() % 256
            encoded_bits = info_bits ^ random_number
            bytes_array.append(encoded_bits)
    with open(filename_write, 'wb') as fw:
        bytes_seq = bytes(bytearray(bytes_array))
        fw.write(bytes_seq)


def save_keys(gnrt: Generator):
    with open('keys.txt', 'w') as f:
        f.write(str(gnrt.a) + '\n' + str(gnrt.b) + '\n' + str(gnrt.current_number))


def load_keys(gnrt: Generator):
    with open('keys.txt', 'r') as f:
        gnrt.a = int(f.readline())
        gnrt.b = int(f.readline())
        gnrt.current_number = int(f.readline())


encode_file('s1.jpeg', 'newjpg', True)
encode_file('newjpg', 'encoded.jpeg', False)
