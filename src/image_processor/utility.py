import cv2 as cv
import numpy as np
from typing import Union
import matplotlib.pyplot as plt
from matplotlib.colors import Colormap

def isOdd(x: int) -> bool:
    return bool(x & 1)

def bitget(x, loc: int) -> int:
    return (x >> loc) & 1

def bitset(x, loc: int, bit: int) -> int:
    if bit != 0:
        return x | (1 << loc)
    else:
        return x & ~(1 << loc)

def rebase(input_array, input_bit_num: int, output_bit_num: int) -> list[int]:
    if input_bit_num == output_bit_num:
        return input_array
    else:
        return rebase_1N(rebase_N1(input_array, input_bit_num), output_bit_num)

def rebase_N1(input_array, input_bit_num: int) -> list[int]:
    tmp = np.array(input_array).astype(np.uint)
    output_array = np.zeros((len(input_array), input_bit_num)).astype(np.uint)

    for i in range(input_bit_num):
        output_array[:, input_bit_num - i - 1] = bitget(tmp, i)

    return list(output_array.reshape(-1))

def rebase_1N(input_array, output_bit_num: int) -> list[int]:
    more = (output_bit_num - len(input_array) % output_bit_num) % output_bit_num
    tmp = np.concatenate((input_array, np.zeros(more).astype(np.uint)), axis = 0).reshape(-1, output_bit_num).astype(np.uint)
    output_array = np.zeros((len(tmp))).astype(np.uint)
    for i in range(output_bit_num):
        output_array = output_array << 1 | tmp[:, i]

    return list(output_array)

def crop(arr: np.ndarray, location: list[int], length: list[int]) -> np.ndarray:
    # crop a multi-dimensional array
    # arr: the array to be cropped
    # location: the location of the first element to be cropped
    # length: the length of the cropped array
    # return: the cropped array
    return arr[tuple([slice(location[i], location[i]+length[i]) for i in range(len(location))])]

def crop2D(img: np.ndarray, x: int, y: int, w: int, h: int) -> np.ndarray:
    return crop(img, [y, x], [h, w])

def load_image_path(path: str, color: int = cv.IMREAD_COLOR, covert_code: Union[None, int] = cv.COLOR_BGR2RGB) -> np.ndarray:
    if covert_code is None:
        return np.array(cv.imread(path, color))
    else:
        return np.array(cv.cvtColor(cv.imread(path, color), covert_code))
    
def save_image_path(path: str, img: np.ndarray, covert_code: Union[None, int] = cv.COLOR_RGB2BGR):
    if covert_code is None:
        cv.imwrite(path, img)
    else:
        cv.imwrite(path, cv.cvtColor(img, covert_code))

def show_image(img: np.ndarray, title = "", cmp: Union[None, str , Colormap] = None):
    if cmp is None:
        plt.imshow(img)
    else:
        plt.imshow(img, cmp)

    plt.title(title)
    plt.show()

def diff_sum(img1: np.ndarray, img2: np.ndarray) -> int:
    return np.sum(np.abs(img1 - img2))

def mse(img1: np.ndarray, img2: np.ndarray) -> float:
    return np.mean((img1.astype(np.float64) - img2.astype(np.float64)) ** 2)

def PSNR(img1: np.ndarray, img2: np.ndarray, max_value = 255) -> float:
    MSE = mse(img1, img2)
    
    if MSE == 0:
        return np.inf
    else:
        return 10 * np.log10(max_value ** 2 / MSE)
