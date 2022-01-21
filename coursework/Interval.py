from math import isnan


class IntervalIterator:
    def __init__(self, interval):
        self._interval = interval
        self._index = 0

    def __next__(self):
        if self._index >= 2:
            raise StopIteration

        if self._index == 0:
            self._index += 1
            return self._interval.a
        else:
            self._index += 1
            return self._interval.b

class Interval:
    a = float('nan')
    b = float('nan')
    wid = float('nan')

    def __init__(self, a, b):
        if a is None:
            a = float('nan')

        if b is None:
            b = float('nan')
        self.a = a
        self.b = b
        if not isnan(self.a) and not isnan(self.b):
            self.wid = float(b - a)

    def __mul__(self, other):
        if type(other) != type(self):
            raise TypeError
        return Interval(min(self.a * other.a, self.a * other.b, self.b * other.a, self.b * other.b),
                        max(self.a * other.a, self.a * other.b, self.b * other.a, self.b * other.b))

    def __neg__(self):
        r = None
        l = None
        if not isnan(self.a):
            r = -self.a
        if not isnan(self.b):
            l = -self.b

        return Interval(l, r)

    def __rtruediv__(self, other):
        r = None
        l = None
        if not isnan(self.a):
            r = 1 / self.a
        if not isnan(self.b):
            l = 1 / self.b
        return other * Interval(l, r)

    def __rmul__(self, other):
        r = None
        l = None
        if not isnan(self.b):
            r = other * self.b
        if not isnan(self.a):
            l = other * self.a
        return Interval(l, r)

    def __str__(self):
        return "[" + str(self.a) + ", " + str(self.b) + "]"

    def __iter__(self):
        return IntervalIterator(self)


def intersection(a: Interval, b: Interval):
    return Interval(max(a.a, b.a), min(a.b, b.b))


def union(a: Interval, b: Interval):
    return Interval(min(a.a, b.a), max(a.b, b.b))
