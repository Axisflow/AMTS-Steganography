""" class Embedable:
    def __init__(self, height: int, width: int):
        self.shape = (height, width)

    def __iter__(self):
        return self.Iterator(self)
    
    def __repr__(self):
        return f'{self.shape}'

    class Point:
        def __init__(self, r: int, c: int):
            self.r = r
            self.c = c

        def __add__(self, other: 'Embedable.Point'):
            return Embedable.Point(self.r + other.r, self.c + other.c)
        
        def __eq__(self, other: 'Embedable.Point'):
            return self.r == other.r and self.c == other.c
        
        def __repr__(self):
            return f'({self.r}, {self.c})'

    class Iterator:
        def __init__(self, parent: 'Embedable'):
            self.shape = parent.shape[0] - 2, parent.shape[1] - 2
            self.r = 0
            self.c = 0
            self.__end = False
            self.__ep = self.end_point()

        def isEven(self, num: int):
            return num % 2 == 0
        
        def matchRequirement(self):
            return self.shape[0] > 0 and self.shape[1] > 0

        def end_point(self):
            r = self.shape[0] - 1
            c = self.shape[1] - 1 if self.isEven(self.shape[0] + self.shape[1]) else self.shape[1] - 2
            return Embedable.Point(r, c)

        def __repr__(self):
            return f'({self.r}, {self.c})'

        def __next__(self):
            if self.matchRequirement():
                now = Embedable.Point(self.r, self.c)
                if now == self.__ep:
                    if self.__end:
                        self.__end = False
                        self.r = 0
                        self.c = 0
                        raise StopIteration
                    else:
                        self.__end = True
                else:
                    if self.c < self.shape[1] - 2:
                        self.c += 2
                    else:
                        self.r += 1
                        self.c = 0 if self.isEven(self.r) else 1

                return now + Embedable.Point(1, 1)
            else:
                raise StopIteration """
            
class EmbedableRGB:
    def __init__(self, height: int, width: int):
        self.shape = (height, width)

    def __iter__(self):
        return self.Iterator(self)
    
    def __repr__(self):
        return f'{self.shape}'

    class Point:
        def __init__(self, r: int, c: int, ch: int):
            self.r = r
            self.c = c
            self.ch = ch

        def __add__(self, other: 'EmbedableRGB.Point'):
            return EmbedableRGB.Point(self.r + other.r, self.c + other.c, self.ch + other.ch)
        
        def __eq__(self, other: 'EmbedableRGB.Point'):
            return self.r == other.r and self.c == other.c and self.ch == other.ch
        
        def __repr__(self):
            return f'({self.r}, {self.c}, {self.ch})'

    class Iterator:
        def __init__(self, parent: 'EmbedableRGB'):
            self.shape = parent.shape[0] - 2, parent.shape[1] - 2
            self.r = 0
            self.c = 0
            self.ch = 0
            self.__end = False
            self.__ep = self.end_point()

        def __iter__(self):
            return self

        def isEven(self, num: int):
            return num % 2 == 0
        
        def matchRequirement(self):
            return self.shape[0] > 0 and self.shape[1] > 0
        
        def set_end_point(self, ep: 'EmbedableRGB.Point'):
            self.__ep = ep + EmbedableRGB.Point(-1, -1, 0)
            return self

        def end_point(self):
            r = self.shape[0] - 1
            c = self.shape[1] - 1 if self.isEven(self.shape[0] + self.shape[1]) else self.shape[1] - 2
            return EmbedableRGB.Point(r, c, 2)

        def __repr__(self):
            return f'({self.r}, {self.c}, {self.ch})'

        def __next__(self):
            if self.matchRequirement():
                now = EmbedableRGB.Point(self.r, self.c, self.ch)
                if now == self.__ep:
                    if self.__end:
                        self.__end = False
                        self.r = 0
                        self.c = 0
                        self.ch = 0
                        raise StopIteration
                    else:
                        self.__end = True
                else:
                    if self.ch < 2:
                        self.ch += 1
                    else:
                        self.ch = 0
                        if self.c < self.shape[1] - 2:
                            self.c += 2
                        else:
                            self.r += 1
                            self.c = 0 if self.isEven(self.r) else 1

                return now + EmbedableRGB.Point(1, 1, 0)
            else:
                raise StopIteration