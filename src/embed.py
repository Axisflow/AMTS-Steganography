import numpy as np
from typing import Any, Literal
from .embedable import EmbedableRGB
from .image_processor import bitget, bitset

def embed_info(image: np.ndarray[tuple[Any, Any, Literal[3]], np.dtype[np.int16]], N: int, r: int,
               T: int) -> np.ndarray[tuple[Any, Any, Literal[3]], np.dtype[np.int16]]:
    result = image.copy()
    adj_mean = np.round((image[1, 0] + image[0, 1]) / 2)
    result[0, 0, 0] = adj_mean[0] + N
    result[0, 0, 1] = adj_mean[1] + r
    result[0, 0, 2] = adj_mean[2] + T

    return result

def embed_endpoint(image: np.ndarray[tuple[Any, Any, Literal[3]], np.dtype[np.int16]],
                   end_point: EmbedableRGB.Point) -> np.ndarray[tuple[Any, Any, Literal[3]], np.dtype[np.int16]]:
    result = image.copy()
    h, w, _ = image.shape
    r, c, e = end_point.r - 1, end_point.c - 1, end_point.ch

    bits_num =  int(np.ceil(np.log2(h - 2)))
    for i in range(1, bits_num):
        loc = i << 1 + 2
        result[loc, 0, 1] = bitset(image[loc, 0, 1], 0, bitget(c, i))

    bits_num =  int(np.ceil(np.log2(w - 2)))
    for i in range(1, bits_num):
        loc = i << 1 + 2
        result[0, loc, 1] = bitset(image[0, loc, 1], 0, bitget(r, i))

    result[h - 1, w - 1, 1] = bitset(image[h - 1, w - 1, 1], 0, bitget(e, 0))
    result[h - 1, w - 1, 1] = bitset(result[h - 1, w - 1, 1], 1, bitget(e, 1))
    return result

def embed_data(image: np.ndarray[tuple[Any, Any, Literal[3]], np.dtype[np.int16]], decimal_data: list[int], N: int,
                    threshold: int) -> tuple[np.ndarray[tuple[Any, Any, Literal[3]], np.dtype[np.int16]], EmbedableRGB.Point]:
    result = image.copy()
    h, w, _ = image.shape
    shift = 2 ** (N - 1)
    T = max(shift, threshold)
    T_mul_2 = T * 2
    limit = None
    adj_mean = None

    # index of height, width, channel and data
    r, c, e, d = None, None, None, 0
    end_point = EmbedableRGB.Point(1, 1, 0)
    for p in EmbedableRGB(h, w):
        if d < len(decimal_data):
            datum = decimal_data[d]
            d = d + 1
        else:
            break

        end_point = p
        r, c, e = p.r, p.c, p.ch
        modified_val = original_val = image[r, c, e]

        adj_mean = int(np.round((image[r + 1, c, e] + image[r - 1, c, e] + image[r, c + 1, e] + image[r, c - 1, e]) / 4))
        if adj_mean + shift >= 256:
            adj_mean = 256 - shift
        elif adj_mean - shift < 0:
            adj_mean = 0 + shift

        modified_val = adj_mean - shift + datum
        if modified_val > original_val + T:
            limit = max(0, original_val - T)
            diff_min = 256
            while modified_val >= limit and abs(modified_val - original_val) < diff_min:
                diff_min = abs(modified_val - original_val)
                modified_val -= T_mul_2
            modified_val += T_mul_2
        elif modified_val < original_val - T:
            limit = min(255, original_val + T)
            diff_min = 256
            while modified_val <= limit and abs(modified_val - original_val) < diff_min:
                diff_min = abs(modified_val - original_val)
                modified_val += T_mul_2
            modified_val -= T_mul_2

        result[r, c, e] = modified_val

    return result, end_point