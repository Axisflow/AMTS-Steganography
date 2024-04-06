from .image_processor import rebase

def encode(data: list[int], N: int, input_bits_num: int = 8) -> tuple[list[int], int]:
    r = (N - len(data) * input_bits_num % N) % N
    return rebase(data, input_bits_num, N), r


def decode(encoded_data: list[int], N: int, r: int, output_bits_nums: int = 8) -> list[int]:
    data = rebase(encoded_data, N, output_bits_nums)
    if r > 0:
        return data[:-1]
    else:
        return data