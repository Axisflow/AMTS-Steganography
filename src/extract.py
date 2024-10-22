import numpy as np
from typing import Any, Literal
from .embedable import EmbedableRGB
from .image_processor import bitget, bitset

def extract_info(stego_image: np.ndarray[tuple[Any, Any, Literal[3]], np.dtype[np.int16]]) -> tuple[int, int, int]:
    adj_mean = np.round((stego_image[1, 0] + stego_image[0, 1]) / 2)
    modified_val = stego_image[0, 0]
    N, r, T = modified_val - adj_mean
    return int(N), int(r), int(T)

def extract_endpoint(stego_image: np.ndarray[tuple[Any, Any, Literal[3]], np.dtype[np.int16]]) -> EmbedableRGB.Point:
    h, w, _ = stego_image.shape

    bits_num =  int(np.ceil(np.log2(h - 2)))
    r = 0
    for i in range(1, bits_num):
        loc = i << 1 + 2
        r = bitset(r, i, bitget(stego_image[loc, 0, 2], 0))

    bits_num =  int(np.ceil(np.log2(w - 2)))
    c = 0
    for i in range(1, bits_num):
        loc = i << 1 + 2
        c = bitset(c, i, bitget(stego_image[0, loc, 2], 0))

    e = 0
    e = bitset(e, 0, bitget(stego_image[h - 1, w - 1, 0], 0))
    e = bitset(e, 0, bitget(stego_image[h - 1, w - 1, 2], 1))

    return EmbedableRGB.Point(r + 1, c + 1, e)

def extract_data(stego_image: np.ndarray[tuple[Any, Any, Literal[3]], np.dtype[np.int16]],
                      N: int, threshold: int, end_point: EmbedableRGB.Point) -> list[int]:
    h, w, _ = stego_image.shape
    shift = 2 ** (N - 1)
    T = max(shift, threshold)
    T_mul_2 = T * 2

    data = list[int]()
    for p in iter(EmbedableRGB(h, w)).set_end_point(end_point):
        # index of height, width and channel
        r, c, e = p.r, p.c, p.ch
        modified_val = stego_image[r, c, e]

        adj_mean = int(np.round((stego_image[r + 1, c, e] + stego_image[r - 1, c, e] + stego_image[r, c + 1, e] + stego_image[r, c - 1, e]) / 4))
        if adj_mean + shift >= 256:
            adj_mean = 256 - shift
        elif adj_mean - shift < 0:
            adj_mean = 0 + shift

        while modified_val >= adj_mean + shift:
            modified_val -= T_mul_2
        
        while modified_val < adj_mean - shift:
            modified_val += T_mul_2

        data.append(modified_val - adj_mean + shift)
        
    return data
