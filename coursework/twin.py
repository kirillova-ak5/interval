from math import isnan


class twin(object):

    internal = None
    external = None

    # inside [a-,a+] external[A-,A+]
    def __init__(self, a1, a2):
        self.internal = a1
        if (isnan(float(a1.a)) or isnan(float(a1.b))) and a2.a == a2.b:
            self.internal = a2

        self.external = a2


    def internal_width(self):
        if isnan(self.internal.a):
            return -1
        return self.internal.wid

    def external_width(self):
        return self.external.wid

    def __str__(self):
        return "[ " + str(self.internal) + ", " +  str(self.external) + " ]"
