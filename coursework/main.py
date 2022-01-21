from Interval import *
from twin import *
from operation import *
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio

def table_const_interpolated(t, temps, vals):
    if t <= temps[0] + 273.15:
        return vals[0]
    if t >= temps[-1] + 273.15:
        return vals[-1]
    for i in range(len(temps) - 1):
        if t >= temps[i] + 273.15 and t <= temps[i + 1] + 273.15:
            k = (temps[i + 1] + 273.15 - t) / (temps[i + 1] - temps[i])
            return float(vals[i]) * k + float(vals[i + 1]) * (1.0 - k)


def table_const_interpolated_twi(t: twin, temps, vals):
    a1 = table_const_interpolated(t.internal.a, temps, vals)
    b1 = table_const_interpolated(t.internal.b, temps, vals)
    a2 = table_const_interpolated(t.external.a, temps, vals)
    b2 = table_const_interpolated(t.external.b, temps, vals)
    return twin(Interval(a1, b1), Interval(a2, b2))

a_temps = [0, 100, 200, 300]

table_const = {
    'ag': {
        'rho': 10500,
        'hi':  430,
        'cp_temps': [27, 127, 327, 527, 727, 962, 1127],
        'cp': [235, 239, 250, 256, 277, 310, 310],
        'alpha': [19.5 * 0.000001, 19.62 * 0.000001, 19.79 * 0.000001, 20.0 * 0.000001]
    },
    'cu': {
        'rho': 8960,
        'hi':  401,
        'cp_temps': [27, 127, 327, 527],
        'cp': [385, 398, 417, 433],
        'alpha': [16.70 * 0.000001, 17.06 * 0.000001, 17.42 * 0.000001, 17.78 * 0.000001]
    },
    'au': {
        'rho': 19320,
        'hi':  320,
        'cp_temps': [27, 127, 327, 527],
        'cp': [129, 131, 135, 140],
        'alpha': [14.15 * 0.000001, 14.32 * 0.000001, 14.51 * 0.000001, 14.735 * 0.000001]
    },
    'al': {
        'rho': 2688.9,
        'hi':  219,
        'cp_temps': [27, 127, 327, 527],
        'cp': [904, 951, 1037, 1154],
        'alpha': [22.8 * 0.000001, 23.7 * 0.000001, 24.5 * 0.000001, 25.4 * 0.000001]
    },
    'cr': {
        'rho': 7180,
        'hi':  107,
        'cp_temps': [27, 127, 327, 527],
        'cp': [453, 482, 517, 558],
        'alpha': [5.88 * 0.000001, 6.61 * 0.000001, 7.28 * 0.000001, 7.84 * 0.000001]
    },
    'fe': {
        'rho': 7874,
        'hi':  92,
        'cp_temps': [27, 127, 327, 527],
        'cp': [450, 490, 572, 678],
        'alpha': [11.30 * 0.000001, 12.15 * 0.000001, 12.70 * 0.000001, 13.25 * 0.000001]
    },
    'pt': {
        'rho': 21450,
        'hi':  70,
        'cp_temps': [27, 127, 327, 527],
        'cp': [133, 136, 141, 147],
        'alpha': [8.95 * 0.000001, 9.10 * 0.000001, 9.20 * 0.000001, 9.325 * 0.000001]
    },
    'sn': {
        'rho': 7290,
        'hi':  67,
        'cp_temps': [27, 127, 232, 327, 527],
        'cp': [229, 244, 248, 242, 236],
        'alpha': [21.0 * 0.000001, 26.2 * 0.000001, 31.6 * 0.000001, 33.7 * 0.000001]
    },
    'pb': {
        'rho': 11336,
        'hi':  35.3,
        'cp_temps': [27, 127, 227, 328, 527],
        'cp': [128, 133, 138, 146, 143],
        'alpha': [28.3 * 0.000001, 29.2 * 0.000001, 30.3 * 0.000001, 31.3 * 0.000001]
    },
    'ti': {
        'rho': 4505,
        'hi':  21.9,
        'cp_temps': [27, 127, 327, 527],
        'cp': [531, 556, 605, 637],
        'alpha': [7.7 * 0.000001, 8.1 * 0.000001, 8.5 * 0.000001, 8.85 * 0.000001]
    }
}

if __name__ == '__main__':
    temp_mat = sio.loadmat('Temp20200601.mat')
    temp = temp_mat['therm']

    first = [Interval(temp[6][i] - 0.35, temp[6][i] + 0.35) for i in range(temp[6].size)]
    second = [Interval(temp[7][i] - 0.35, temp[7][i] + 0.35) for i in range(temp[7].size)]

    intr = []

    for i in range(len(first)):
        intersect = intersection(first[i], second[i])
        if intersect.a <= intersect.b:
            intr.append(i)

    intr_deltas = [intr[i+1] - intr[i] for i in range(len(intr) - 1)]
#    print(intr[141:828])
#    print(intersection(first[3771], second[3771]))

    twins = []
#    twins_fu = []
    for i in range(141, 828):
        twi = twin(intersection(first[intr[i]], second[intr[i]]), union(first[intr[i]], second[intr[i]]))
        twi.internal.a += 273.15
        twi.internal.b += 273.15
        twi.external.a += 273.15
        twi.external.b += 273.15
#        twii = twin(Interval(twi.external.a, twi.internal.a), Interval(twi.internal.b, twi.external.b))
        twins.append(twi)
#        twins_fu.append(twii)

    rwid = []
    zeros = []
    for i in range(3000, 4000):
        int = intersection(first[i], second[i])
        uni = union(first[i], second[i])
        rwid.append(int.wid / uni.wid)
        zeros.append(0.0)

#    rwid = [twins[i].internal.wid / twins[i].external.wid for i in range(len(twins))]
    plt.plot(rwid)
    plt.plot(zeros, linewidth = 0.5)
    plt.figure()

    k1 = 100.0 / 273.15
#    resist = [multiply(twin(Interval(k1-0.000005, k1+0.000005), Interval(k1-0.00005, k1+0.00005)), twins[i]) for i in range(len(twins))]
#    resist = [multiply(twin(Interval(k1-0.00001, k1+0.00000), Interval(k1+0.00001, k1+0.00002)), twins_fu[i]) for i in range(len(twins))]
    resist = [multiply_num(k1, twins[i]) for i in range(len(twins))]

    res_plt_1 = [resist[i].external.a for i in range(len(twins))]
    res_plt_2 = [resist[i].external.b for i in range(len(twins))]
    res_plt_3 = [resist[i].internal.a for i in range(len(twins))]
    res_plt_4 = [resist[i].internal.b for i in range(len(twins))]
    plt.plot(res_plt_1, linestyle = ':')
    plt.plot(res_plt_2, linestyle = ':')
    plt.plot(res_plt_3)
    plt.plot(res_plt_4)

    plt.figure()

    metal = 'pt'

    cp = [table_const_interpolated_twi(twins[i], table_const[metal]['cp_temps'], table_const[metal]['cp']) for i in range(len(twins))]
#    multiply(table_const_interpolated_twi(twins[i], a_temps, table_const[metal]['alpha']), plus_num(- 20.0 + 273.15, twins[i]))
    rho_helper = [plus_num(1.0, multiply(
        table_const_interpolated_twi(twins[i], a_temps, table_const[metal]['alpha']),
        plus_num(- 20.0 + 273.15, twins[i]))) for i in range(len(twins))]
    rho = [multiply_num(table_const[metal]['rho'], inverse_twin(
        multiply(rho_helper[i], multiply(rho_helper[i], rho_helper[i])))) for i in range(len(twins))]

    lambd = [multiply_num(table_const[metal]['hi'], inverse_twin(multiply(cp[i], rho[i]))) for i in range(len(twins))]

#    lambd = [multiply(twins[i], twins[i]) for i in range(len(twins))]
    res_plt_1 = [lambd[i].external.a for i in range(len(twins))]
    res_plt_2 = [lambd[i].external.b for i in range(len(twins))]
    res_plt_3 = [lambd[i].internal.a for i in range(len(twins))]
    res_plt_4 = [lambd[i].internal.b for i in range(len(twins))]
    plt.plot(res_plt_1, linestyle = ':')
    plt.plot(res_plt_2, linestyle = ':')
    plt.plot(res_plt_3)
    plt.plot(res_plt_4)

    plt.show()
