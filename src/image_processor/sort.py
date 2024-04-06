from typing import Any

class Sorter:
    def __init__(self, compare_func: Any=None, args=None):
        self.compare_func = compare_func
        self.args = args
    
    def qsort(self, arr):
        def qsort_compare_func_args(arr) -> list:
            if len(arr) <= 1:
                return arr
            pivot = arr[len(arr) // 2]
            left = [x for x in arr if self.compare_func(x, pivot, self.args) < 0]
            middle = [x for x in arr if self.compare_func(x, pivot, self.args) == 0]
            right = [x for x in arr if self.compare_func(x, pivot, self.args) > 0]
            return qsort_compare_func_args(left) + middle + qsort_compare_func_args(right)
        
        def qsort_compare_func(arr) -> list:
            if len(arr) <= 1:
                return arr
            pivot = arr[len(arr) // 2]
            left = [x for x in arr if self.compare_func(x, pivot) < 0]
            middle = [x for x in arr if self.compare_func(x, pivot) == 0]
            right = [x for x in arr if self.compare_func(x, pivot) > 0]
            return qsort_compare_func(left) + middle + qsort_compare_func(right)
        
        def qsort(arr) -> list:
            if len(arr) <= 1:
                return arr
            pivot = arr[len(arr) // 2]
            left = [x for x in arr if x < pivot]
            middle = [x for x in arr if x == pivot]
            right = [x for x in arr if x > pivot]
            return qsort(left) + middle + qsort(right)
        
        if self.compare_func is None:
            return qsort(arr)
        elif self.args is None:
            return qsort_compare_func(arr)
        else:
            return qsort_compare_func_args(arr)