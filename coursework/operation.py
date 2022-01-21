from twin import twin
from Interval import Interval, intersection
from math import isnan

def p (T1:twin,T2:twin):
    if T1.internal_width() == -1 and T2.internal_width() == -1:
        return None
    if T1.internal_width() == -1:
        return T2.internal.a + T1.external.b
    if T2.internal_width() == -1:
        return T1.internal.a + T2.external.b
    return min(T1.internal.a + T2.external.b, T2.internal.a + T1.external.b)

def q(T1:twin , T2:twin):
    if T1.internal_width() == -1 and T2.internal_width() == -1:
        return None
    if T1.internal_width() == -1:
        return T2.internal.b + T1.external.a
    if T2.internal_width() == -1:
        return T1.internal.b + T2.external.a
    return max(T1.internal.b + T2.external.a, T2.internal.b + T1.external.a)

def plus(T1:twin,T2:twin):
    if T1.external_width() <= T2.internal_width() or T2.external_width() <= T1.internal_width():
        return twin( Interval(p(T1, T2), q(T1, T2)),Interval(T1.external.a + T2.external.a, T1.external.b + T2.external.b))
    else:
        return twin(
            Interval(None, None),
            Interval(T1.external.a + T2.external.a, T1.external.b + T2.external.b)
        )


def phi2(I1, I2):
    Z = intersection(I1, I2)
    if isnan(float(Z.a)) or isnan(float(Z.b)):
        return Interval(None, None)
    min = abs(I1.a - I2.a)
    min_a = I1.a
    min_b = I2.a

    if abs(I1.b - I2.b) < min:
        min = abs(I1.b - I2.b)
        min_a = I1.b
        min_b = I2.b

    if abs(I1.a - I2.b) < min:
        min = abs(I1.a - I2.b)
        min_a = I1.a
        min_b = I2.b

    if abs(I1.b - I2.a) < min:
        min = abs(I1.b - I2.a)
        min_a = I1.b
        min_b = I2.a

    return Interval(min_a, min_b)

  #  return Z


def phi(I1, I2):
    Z = intersection(I1, I2)
    if not (isnan(float(Z.a)) or isnan(float(Z.b))):
        return Interval(None, None)
    elif not isnan(float(Z.a)) and (not isnan(float(Z.b))) and Z.a != Z.b:
        return Interval(None, None)
    else:
        min = abs(I1.a - I2.a)
        min_a = I1.a
        min_b = I2.a

        if abs(I1.b - I2.b) < min:
            min = abs(I1.b - I2.b)
            min_a = I1.b
            min_b = I2.b

        if abs(I1.a - I2.b) < min:
            min = abs(I1.a - I2.b)
            min_a = I1.a
            min_b = I2.b

        if abs(I1.b - I2.a) < min:
            min = abs(I1.b - I2.a)
            min_a = I1.b
            min_b = I2.a
        if min_b < min_a:
            return Interval(min_b, min_a)
        return Interval(min_a, min_b)


def psi(I1, I2):
    return Interval(
        min(I1.a, I1.b, I2.a, I2.b),
        max(I1.a, I1.b, I2.a, I2.b)
    )


def multiply_num(n, T2: twin):
    return twin(n * T2.internal, n * T2.external)
def plus_num(n, T2: twin):
    return twin(Interval(T2.internal.a + n, T2.internal.b + n), Interval(T2.external.a + n, T2.external.b + n))

def multiply(T1: twin, T2: twin):
    if T1.internal_width() == -1 and T2.internal_width() == -1:
        return twin(
            Interval(None, None),
            Interval(T1.external.a, T1.external.b) * Interval(T2.external.a, T2.external.b)
        )

    if T1.internal_width() == -1:
        return twin(
            phi2(
                T2.internal.a * Interval(T1.external.a, T1.external.b),
                T2.internal.b * Interval(T1.external.a, T1.external.b)
            ),
            Interval(T1.external.a, T1.external.b) * Interval(T2.external.a, T2.external.b)
        )

    if T2.internal_width() == -1:
        return twin(
            phi2(
                T1.internal.a * Interval(T2.external.a, T2.external.b),
                T1.internal.b * Interval(T2.external.a, T2.external.b)
            ),
            Interval(T1.external.a, T1.external.b) * Interval(T2.external.a, T2.external.b)
        )

    return twin(
        psi(
            phi2(
                (T1.internal.a) * Interval(T2.external.a, T2.external.b),
                (T1.internal.b) * Interval(T2.external.a, T2.external.b)
            ),
            phi2(
                T2.internal.a * Interval(T1.external.a, T1.external.b),
                T2.internal.b * Interval(T1.external.a, T1.external.b)
            )
        ),
        Interval(T1.external.a, T1.external.b) * Interval(T2.external.a, T2.external.b)
    )

def unary_minus_twin(T: twin):
    return twin(-T.internal, -T.external)

def inverse_twin(T: twin):
    if 0 in T.internal or 0 in T.external:
        print("Cannot be divided into intervals containing 0.")
        exit()
    return twin(1 / T.internal, 1 / T.external)
