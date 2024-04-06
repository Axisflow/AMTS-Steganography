
class SpiralRectangle2D:
    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width

    def __iter__(self):
        return SpiralRectangle2D.Iterator(self)

    class Iterator:
        def __init__(self, parent: 'SpiralRectangle2D'):
            self.height = parent.height
            self.width = parent.width
            self.direction = 0 # 0: right, 1: down, 2: left, 3: up
            self.layer = 0
            self.r = 0
            self.c = 0
            self.__ep = self.__end_point()
            self.__end = False
        
        def __end_point(self):
            # Square
            # return (self.width // 2, self.height // 2)
            # Rectangle
            if self.width >= self.height:
                r = self.height // 2
                if self.height % 2:
                    c = self.width - self.height // 2 - 1
                else:
                    c = self.height // 2 - 1
            else:
                c = self.width // 2
                if self.width % 2:
                    r = self.height - self.width // 2 - 1
                else:
                    r = self.width // 2 - 1

            return SpiralRectangle2D.Point((self.height, self.width), r, c)
        
        def __next__(self):
            now = SpiralRectangle2D.Point((self.height, self.width), self.r, self.c)
            if now.r == self.__ep.r and now.c == self.__ep.c:
                if self.__end:
                    self.__end = False
                    self.r = 0
                    self.c = 0
                    raise StopIteration
                else:
                    self.__end = True
            else:
                if self.direction == 0:
                    if self.c < self.width - self.layer - 1:
                        self.c += 1
                    else:
                        self.direction = 1
                        self.r += 1
                elif self.direction == 1:
                    if self.r < self.height - self.layer - 1:
                        self.r += 1
                    else:
                        self.direction = 2
                        self.c -= 1
                elif self.direction == 2:
                    if self.c > self.layer:
                        self.c -= 1
                    else:
                        self.direction = 3
                        self.r -= 1
                else:
                    if self.r > self.layer + 1:
                        self.r -= 1
                    else:
                        self.direction = 0
                        self.c += 1
                        self.layer += 1
                
            return now
        
        def __str__(self):
            return f'({self.r}, {self.c})'
        
        def __repr__(self):
            return f'({self.r}, {self.c})'
    
    class Point:
        def __init__(self, shape: tuple[int, int], r: int, c: int):
            self.height = shape[0]
            self.width = shape[1]
            self.r = r
            self.c = c
            self.__center = (self.width // 2, self.height // 2)
            self.layer = self.__layer()
            self.strict = False

        def atRight(self) -> bool:
            return self.c >= self.__center[0]
        
        def atTop(self) -> bool:
            return self.r <= self.__center[1]
        
        def __layer(self):
            if self.atTop():
                if self.atRight():
                    return min(self.width - self.c - 1, self.r)
                else:
                    return min(self.c, self.r)
            else:
                if self.atRight():
                    return min(self.width - self.c - 1, self.height - self.r - 1)
                else:
                    return min(self.c, self.height - self.r - 1)
                
        def __lt__(self, other: 'SpiralRectangle2D.Point'):
            return self.layer < other.layer
        
        def __eq__(self, other: 'SpiralRectangle2D.Point'):
            return self.layer == other.layer
        
        def __gt__(self, other: 'SpiralRectangle2D.Point'):
            return self.layer > other.layer
        
        def __str__(self):
            return f'({self.r}, {self.c})'
        
        def __repr__(self):
            return f'({self.r}, {self.c})'