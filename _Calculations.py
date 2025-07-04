import math

from utilities import toFixed

mark = ""

def find_point(value, mark_brakepoints):
    for i, start in enumerate(range(0, 1400, 100)):
        end = start + 100
        if start <= value < end and mark == "08, 10, 3кп (1)":
            return mark_brakepoints["first_mark"][i]
        if start <= value < end and mark == "15, 25, 35 (2)":
            return mark_brakepoints["second_mark"][i]
        if start <= value < end and mark == "45, 17Г1С4 (3)":
            return mark_brakepoints["third_mark"][i]
    return None  # если не попал ни в один диапазон

def lambda_(g): # Коэффициент теплопроводности металла,Вт/(м*К)
    g = g-273
    mark_brakepoints = {
        "first_mark": [ 61,56,51,46,40,36,33,30,28,28,29,29,29],
        "second_mark": [51,50,46.5,44,40.75,37.25,33.75,28.25,28,28,28,28,28],
        "third_mark": [43.4,42.4,40.5,38.2,36.6,34.2,31.2,30.3,28.9,28.8,28.8,28.8,28.8]
    }
    result = find_point(g, mark_brakepoints)
    return -8e-7*result*result-1.477e-2*result+46.585

def c(g): # Истиная теплоёмкость металла,Дж/(кг*К)
    g = g-273
    
    mark_brakepoints = {
        "first_mark": [ 464,489,516,549,587.5,634.5,703,813,797,652,660.5,667.5,676.5],
        "second_mark": [479,496,535,550,599,683,522,723,674,649,657,678,687],
        "third_mark": [502,528,569,611,691,733,676,502,624,632,641,669,687]
    }
    result = find_point(g, mark_brakepoints)
    if result>700:
        return 1618-0.8025*result
    else:
        return (0.6938-0.002325*result+4.571e-6*result*result)*1000

def ro(g): # Плотность металла,кг/м^3)
    g = g-273
    
    
    mark_brakepoints = {
        "first_mark": [7844,7816,7783,7748,7712,7674,7635,7602,7598,7569,7521,7492,7463],
        "second_mark": [7821,7789,7755,7720,7683,7643,7604,7608,7578,7530,7491,7464,7432],
        "third_mark": [7826,7799,7769,7739,7698,7662,7625,7587,7595,7540,7508,7475,7443]
    }
    result = find_point(g, mark_brakepoints)
    return (7.824-3.355e-4*result)*1000

def Temp1(T, n, tw, dx, dtime, Epr, Tw):
    j = T[n-1][0]

    alfa = Epr * (tw**4 - j**4) / (Tw - j) + 40

    Bi = alfa * dx / lambda_(0.5 * (T[n-2][0] + T[n-1][0]))

    fmin = lambda_((T[n-1][0] + T[n-2][0]) / 2) * dtime / \
           (c(T[n-1][0]) * ro(T[n-1][0]) * dx * dx)

    if fmin > 0.5 / (1 + Bi):
        print("sx neust") 

    T[n-1][1] = 2 * fmin * T[n-2][0] + (1 - 2 * fmin * (1 + Bi)) * T[n-1][0] + 2 * fmin * Bi * tw


def Temp2(T, n, twNp, dx, dtime, Epr, dtmax, Qm_ud, Qm_ud1, Qm_ud2, time):
    for i in range(n-2, 0, -1):  # (n-1) downto 2 → range(n-2, 0, -1)
        fmin = lambda_((T[i][0] + T[i-1][0]) / 2) * dtime / (c(T[i][0]) * ro(T[i][0]) * dx * dx)
        fpl = lambda_((T[i][0] + T[i+1][0]) / 2) * dtime / (c(T[i][0]) * ro(T[i][0]) * dx * dx)
        T[i][1] = T[i][0] + fpl * (T[i+1][0] - T[i][0]) - fmin * (T[i][0] - T[i-1][0])

    fpl = lambda_((T[0][0] + T[1][0]) / 2) * dtime / (c(T[0][0]) * ro(T[0][0]) * dx * dx)

    j = T[n-1][0]
    alfa = Epr * (twNp**4 - j**4) / (twNp - j) + 40
    Bi = alfa * dx / lambda_(0.5 * (T[1][0] + T[0][0]))

    fmin = lambda_((T[0][0] + T[1][0]) / 2) * dtime / (c(T[0][0]) * ro(T[0][0]) * dx * dx)

    if fmin > 0.5 / (1 + Bi):
        print("sx neust")

    T[0][1] = 2 * fmin * T[1][0] + (1 - 2 * fmin * (1 + Bi)) * T[0][0] + 2 * fmin * Bi * twNp

    if (T[n-1][1] - T[round(n/2)-1][1]) > dtmax:
        dtmax = T[n-1][1] - T[round(n/2)-1][1]


    dQm = 0
    ccp = 0
    for i in range(n-1):
        tcp = (T[i][1] + T[i+1][1]) / 2
        dQm += c(tcp) * ((T[i][1] - T[i][0] + T[i+1][1]-T[i+1][0])/2) / (n-1) #2025
        ccp += c(tcp)

    Qm_ud += dQm

    nmin = round(n / 2)
    dQm1 = 0
    for i in range(nmin-1):
        tcp = (T[i][1] + T[i+1][1]) / 2
        dQm1 += c(tcp) * ((T[i][1] - T[i][0] + T[i+1][1]-T[i+1][0])/2) / (nmin-1) / 2 #2025

    Qm_ud1 += dQm1

    dQm2 = 0
    for i in range(nmin, n-1):
        tcp = (T[i][1] + T[i+1][1]) / 2
        dQm2 += c(tcp) * ((T[i][1] - T[i][0] + T[i+1][1]-T[i+1][0])/2) / (n-nmin) / 2 #2025

    Qm_ud2 += dQm2

    # if time % 600 == 0:
    #     print(f"time = {time}")

    for i in range(n):
        T[i][0] = T[i][1]

    return Qm_ud, Qm_ud1, Qm_ud2, dtmax

def Temp3(t, n, twNp, dx, dtime, Epr, dtmax, Qm_ud, Qm_ud1, Qm_ud2, time):

    for i in range(n-2, 0, -1):
        fmin = lambda_((t[i][0] + t[i-1][0]) / 2) * dtime / c(t[i][0]) / ro(t[i][0]) / dx / dx
        fpl = lambda_((t[i][0] + t[i+1][0]) / 2) * dtime / c(t[i][0]) / ro(t[i][0]) / dx / dx
        t[i][1] = t[i][0] + fpl * (t[i+1][0] - t[i][0]) - fmin * (t[i][0] - t[i-1][0])

    fpl = lambda_((t[0][0] + t[1][0]) / 2) * dtime / c(t[0][0]) / ro(t[0][0]) / dx / dx

    j = t[n-1][0]
    alfa = 0
    Bi = alfa * dx / lambda_(0.5 * (t[1][0] + t[0][0]))

    fmin = lambda_((t[0][0] + t[1][0]) / 2) * dtime / c(t[0][0]) / ro(t[0][0]) / dx / dx

    if fmin > 0.5 / (1 + Bi):
        print("sx neust") 

    t[0][1] = 2 * fmin * t[1][0] + (1 - 2 * fmin * (1 + Bi)) * t[0][0] + 2 * fmin * Bi * twNp

    if (t[n-1][1] - t[round(n/2)-1][1]) > dtmax:
        dtmax = t[n-1][1] - t[round(n/2)-1][1]

    # Определение энтальпии металла
    dQm = 0
    ccp = 0
    for i in range(n-1):
        tcp = (t[i][1] + t[i+1][1]) / 2
        dQm += c(tcp) * ((t[i][1] - t[i][0]+t[i+1][1]-t[i+1][0])/2) / (n-1) #2025
        ccp += c(tcp) #2025

    Qm_ud += dQm

    nmin = round(n / 2)
    dQm1 = 0
    for i in range(nmin - 1):
        tcp = (t[i][1] + t[i+1][1]) / 2
        dQm1 += c(tcp) * ((t[i][1] - t[i][0]+t[i+1][1]-t[i+1][0])/2) / (nmin - 1) / 2 #2025

    Qm_ud1 += dQm1

    dQm2 = 0
    for i in range(nmin, n-1):
        tcp = (t[i][1] + t[i+1][1]) / 2
        # dQm2 += c(tcp) * (t[i][1] - t[i][0]) / (n - nmin) / 2 #2025 в оригинальном коде не закоментирован, хотя работает над той же переменной 
        dQm2 += c(tcp) * ((t[i][1] - t[i][0] + t[i+1][1]-t[i+1][0]) / 2)/(n-nmin)/2 #2025

    Qm_ud2 += dQm2

    if time == 600 * (time // 600):
        pass  # В оригинальном коде этот блок закомментирован, поэтому его пропускаем

    for i in range(n):
        t[i][0] = t[i][1]  # Обновление температур

    return Qm_ud, Qm_ud1, Qm_ud2, dtmax


def cd(g, h2o, co2, n2, o2):
    """
    Средняя теплоёмкость дымовых газов, Дж/(м^3*К).
    
    Параметры:
    g (float): Температура газа (К).
    h2o (float): Доля H2O в дымовых газах (%).
    co2 (float): Доля CO2 в дымовых газах (%).
    n2 (float): Доля N2 в дымовых газах (%).
    o2 (float): Доля O2 в дымовых газах (%).
    
    Возвращает:
    float: Средняя теплоёмкость дымовых газов (Дж/(м^3*К)).
    """
    # Средние теплоёмкости составляющих дыма, кДж/(м^3*К)
    dh2o = -3.94e-8 * g**2 + 3.795e-4 + 1.3033
    do2 = -1.7e-8 * g**2 + 1.495e-4 + 1.3173
    dn2 = -2.48e-8 * g**2 + 1.788e-4 * g + 1.2048
    dco2 = -7.08e-8 * g**2 + 4.64e-4 * g + 1.7341

    # Средняя теплоёмкость дымовых газов, Дж/(м^3*К)
    cd_value = (dh2o * h2o + dco2 * co2 + dn2 * n2 + do2 * o2) / 100 * 1000
    return cd_value

def FuelСonsumptionCalculation(gases, heating_data, consumption, performance, result, params):
    gas_data = [] 
    zonesum = 0.0
    zonedata = heating_data["Расчет нагрева металла"]["Расход топлива по зонам:"]
    zonelist = ["в первой сварочной зоне", "в зоне нижнего подогрева 2", "во второй сварочной зоне", "в зоне нижнего подогрева 4", "в томильной зоне"]
    for i, row in enumerate(zonelist):
        zonesum += float(zonedata[f"{row}, тыс. м³/час"])

    for gas in gases:
        mixed_percentage = float(params[gas.name].get())
        m3h = float(zonesum) * float(mixed_percentage / 100)
        gas_data.append((f"Расход топлива в ч\n{gas.name}, м³/ч", toFixed(m3h, 1)))
        m3t =  float(toFixed(m3h, 1)) /float(performance) * 1000
        gas_data.append((f"Расход топлива в т\n{gas.name}, м³/т", toFixed(m3t, 1)))

        for item in result:
            key, value = item[:2]
            if gas.name == "Доменный газ" and key == "Низшая рабочая теплота\nсгорания - Доменный газ,\nккал/м³ (при 20°C)": 
                bof_prm3t = (float(m3t) / 1000)  * float(value)
                gas_data.append((f"Расход топлива в пр.т\n{gas.name}, пр.м3/т", toFixed(bof_prm3t, 1)))
            
            if gas.name == "Коксовый газ" and key == "Низшая рабочая теплота\nсгорания - Коксовый газ,\nккал/м³ (при 20°C)": 
                coke_prm3t = (float(m3t) / 4000) * float(value)
                gas_data.append((f"Расход топлива в пр.т\n{gas.name}, пр.м3/т", toFixed(coke_prm3t, 1)))

    return gas_data
        

def FuilBurnCalculation(gases, Npir, tv, tg, l, params):
    # Список газов для подсчета
    gas_list = []

    # Процентное содержание газов
    gas_percentages = {}

    # Смешанный газ
    mixed_gas = [0 for m in range(12)]

    # Стоимости газов для получения стоимости смешанного газа
    mixed_price = 0
    prices = {}

    # Теплота сгорания
    Qt = {}

    # Проход газам из базы данных
    for gas in gases:
        # Доля газов с UI
        mixed_percentage = float(params[gas.name].get())
        print(mixed_percentage)
        
        res = []
        price = 0
                
        for el in gas.components:
            # Компонент d влагосодержание
            if(el.component != "d" and el.component != "Стоимость" and el.component != "Плотность"):
                res.append(el.value)
            elif(el.component == "Плотность"):
                price = el.value
            elif(el.component == "Стоимость"):
                if(gas.name == "Сжиженный газ"):
                    price = price * el.value # Плотность на стоимость
                else:
                    price = el.value
            else:
                # Добавляем влагосодержание
                res.append(100 * el.value / (805 + el.value))
        
        # Пересчёт на влажное топливо
        for i in range(11):
            res[i] *= 1 - 0.01 * res[11]

        # Подсчет смешанного газа
        for i in range(12):
            # mixed_gas[i] += res[i] * gas.mixed_percentage
            mixed_gas[i] += res[i] * mixed_percentage

        # Низшая теплота сгорания
        Qv = (358 * res[0] + 590 * res[1] + 636 * res[2] + 913 * res[3] + 1185 * res[4] +
           1465 * res[5] + 127.7 * res[6] + 108 * res[7]) * 1000

        gas_list.append(res)

        # gas_percentages[gas.name] = gas.mixed_percentage
        gas_percentages[gas.name] = mixed_percentage
        Qt[gas.name] = Qv / 1000 / 4.19 / 293*273

        if(gas.name == "Коксовый газ" or gas.name == "Доменный газ"):
            price = (price * Qt[gas.name]) / 1000
        
        mixed_price += price * gas.mixed_percentage

        prices[gas.name] = price * gas.mixed_percentage / 100

    # Удельная теплоёмкость
    Cv = (0.21 * (6.5929e-8 * tv**2 + 1.137e-4 * tv + 1.2699) +
          0.79 * (1.2058e-7 * tv**2 - 6.0312e-5 * tv + 1.3012)) * 1000

    Cch4 = 6.497e-7 * tg**2 + 5.6125e-4 * tg + 1.3474
    Cc2h4 = -0.0000007*tg*tg + 0.0024*tg + 1.8321
    Cc2h6 = -5.755e-7 * tg**2 + 3.273e-3 * tg + 1.3594
    Cc3h8 = -2.44329e-6 * tg**2 + 6.506e-3 * tg + 1.4532
    Cc4h10 = 0.00054617 * tg + 2.637
    Cc5h12 = 0.0066452 * tg + 3.3149
    Cco = 0.000075 * tg + 1.273
    Ch2 = 0.0000608 * tg + 1.2604
    Cco2 = -5.653e-7 * tg**2 + 1.3528e-3 * tg + 1.2726
    Cn2 = 1.2058e-7 * tg**2 - 6.0312e-5 * tg + 1.3012
    Co2x = 6.5929e-8 * tg**2 + 1.137e-4 * tg + 1.2699
    Ch2o = 0.000166 * tg + 1.449

    # Цена смешанного газа
    Ts = mixed_price / 100
    # 5_933_330.752825198 / 1000 / 4.19
    # Состав смешанного газа
    bb = [mixed_gas[m] / 100 for m in range(12)]

    # Низшая рабочая теплота сгорания смеси
    Q = (358 * bb[0] + 590 * bb[1] + 636 * bb[2] + 913 * bb[3] + 1185 * bb[4] +
         1465 * bb[5] + 127.7 * bb[6] + 108 * bb[7]) * 1000
    # Плотность газа
    Rog = (0.717 * bb[0] + 1.261 * bb[1] + 1.357 * bb[2] + 2.019 * bb[3] + 2.672 * bb[4] +
           3.219 * bb[5] + 1.251 * bb[6] + 0.090 * bb[7] + 1.977 * bb[8] +
           1.251 * bb[9] + 1.429 * bb[10] + 0.804 * bb[11]) / 100

    # Удельный расход воздуха
    vo2 = 0.01 * (2 * bb[0] + 3 * bb[1] + 3.5 * bb[2] + 5 * bb[3] + 6.5 * bb[4] +
                  8 * bb[5] + 0.5 * bb[6] + 0.5 * bb[7] - bb[10])
    
    l0 = vo2 / 0.21

    # ld = l0 * 1.05
    ld = l0 * l

    # Удельный выход дыма
    vco2 = 0.01 * (bb[6] + bb[0] + 2 * bb[1] + 2 * bb[2] + 3 * bb[3] + 4 * bb[4] +
                   5 * bb[5] + 2 * bb[8])
    vh2o = 0.01 * (bb[7] + 2 * bb[0] + 2 * bb[1] + 4 * bb[3] + 5 * bb[4] + 6 * bb[5] + bb[11])
    vn2 = 0.01 * bb[9] + 0.79 * ld
    vo2i = 0.01 * bb[10] + 0.0105 * l0
    v = vco2 + vh2o + vn2 + vo2i

    v *= 0.01

    # Состав дыма
    co2 = vco2 / v
    n2 = vn2 / v
    h2o = vh2o / v
    o2 = vo2i / v

    v *= 100

    Cg = (
        Cch4 * bb[0] +
        Cc2h4 * bb[1] +
        Cc2h6 * bb[2] +
        Cc3h8 * bb[3] +
        Cc4h10 * bb[4] +
        Cc5h12 * bb[5] +
        Cco * bb[6] +
        Ch2 * bb[7] +
        Cco2 * bb[8] +
        Cn2 * bb[9] +
        Co2x * bb[10] +
        Ch2o * bb[11]
    ) / 100 * 1000

    # Физическое тепло топлива
    Qft = Cg * (tg - 273)
    # Физическое тепло воздуха
    Qfv = ld * Cv * (tv - 273)

    # Энтальпия дыма
    Hk = (Q + Qfv + Qft) / v

    # Поиск калориметрической температуры (метод половинного деления)
    t1, t2 = 500, 3500
    tk = 0
    while True:
        tk = (t1 + t2) / 2
        H = cd(tk, h2o, co2, n2, o2) * (tk - 273)
        if H < Hk:
            t1 = tk
        else:
            t2 = tk

        # Условие выхода из цикла
        if 0.999 * Hk <= H <= 1.001 * Hk:
            break

    # Действительная температура
    td = (tk - 273) * Npir

    return (
        gas_percentages, prices, Ts, Qt, (Q / 1000/ 4.19 / 293*273), 
        {"CO2": co2, "N2": n2, "H2O": h2o, "O2": o2},
        Rog, ld, v,
        cd(tk, h2o, co2, n2, o2),
        tk,
        td,
        {"Цена": Ts, "Природный газ": gas_percentages['Природный газ'], "v": v, "H2O": h2o, "CO2" : co2, "N2" : n2, "O2" : o2, "Q" : Q, "Qft" : Qft, "Qfv" : Qfv}
    )


def StCh(w):

    Em = 0.8
    Edg = 0.36

    Epr=5.67e-8*Em*Edg*((1-Edg)/w+1)/((1-Edg)*(Em+Edg*(1-Em))/w+Edg)

    return Epr

def Fettling(toc, tw, alfa_2, dst1, dst2):
    # Константы
    ef = 0.7
    edg = 0.36
    a1 = 676.162e-7  # Коэффициент температуропроводности шамота, м^2/с
    sigma = 5.67e-8  # Постоянная Стефана-Больцмана

    # Исходные параметры
    t_1 = toc
    t_2 = tw

    while True:  # Аналог label_1
        t1 = (t_1 + t_2) / 2
        t2 = (t1 + toc) / 2

        # Приведённый коэффициент излучения на футеровку
        Epr_f = sigma / (1 / ef + 1 / edg - 1)

        # Суммарный коэффициент теплоотдачи на футеровку
        alfa_1 = Epr_f * (tw**4 - t1**4) / (tw - t1) + 40

        # Тепловой поток
        Qf = alfa_1 * (tw - t1)
        t3 = Qf / alfa_2 + toc

        while True:  # Аналог label_2
            t2x = t2
            tcp2 = (t2x + t3) / 2
            lambda2 = (0.84 + 0.58e-3 * (tcp2 - 273))
            t2 = Qf * dst2 / lambda2 + t3

            if abs(t2 - t2x) / t2 <= 0.0001:
                break  # Выход из label_2

        lambda1 = (0.84 + 0.58e-3 * ((t1 + t2) / 2 - 273)) * 5
        Qf1 = lambda1 / dst1 * (t1 - t2)

        if Qf > Qf1:
            t_1 = t1
        else:
            t_2 = t1

        if abs(Qf - Qf1) / Qf <= 0.0001:
            break  # Выход из label_1

    return t1, t2, t3, Qf  # Возвращаем расчётные температуры

def SIO(p, tw, Epr, tnas, r1,r2,r3):
    # Константы
    sigma = 5.67e-8  # Постоянная Стефана-Больцмана
    Esio = 0.7
    Edg = 0.36
    # Исходные параметры        
    w = p / (math.pi * r3 * 2)

    # Вычисление эффективной теплопроводности
    Epr_s = sigma * Esio * Edg * ((1 - Edg) / w + 1) / \
        (((1 - Edg) / Edg * (Esio + Edg * (1 - Esio)) / w) + 1)

    t_1 = tnas
    t_2 = tw

    while True:
        tst = (t_1 + t_2) / 2  # Средняя температура
        j = tst

        # Коэффициент теплоотдачи
        alfa = Epr * (tw**4 - j**4) / (tw - j) + 40

        # Коэффициенты теплопроводности
        lambda3 = 30
        lambda4 = 2

        # Тепловые потоки
        Ql = 2 * math.pi * (tw - tnas) / (1 / alfa / r3 + math.log(r2 / r1) / lambda3 + math.log(r3 / r2) / lambda4)
        Ql1 = 2 * math.pi * (tst - tnas) / (math.log(r2 / r1) / lambda3 + math.log(r3 / r2) / lambda4)

        # Условие корректировки температур
        if Ql < Ql1:
            t_2 = tst
        else:
            t_1 = tst

        # Проверка критерия завершения
        if abs(Ql - Ql1) / Ql <= 0.01:
            break

    return tst, Ql


import numpy as np

def MetallBurnCalculation(
        s, bb, a, Lp, toc, tnas, tmn, twDif, twMetn, twMetNpk, twSv1n, twSv2, twNp2k, twTom, twNp2n,
        dst1, dst2, r1, r2, r3, dtdop, n, time_H, tMet_per, tSv1_per, tSv2_per, tTom_per, Fmet, Fsv1, Fsv2, Ftom,
        LsioMet, LsioSv1, LsioSv2, LsioTom, LsioPercent,
        Ts, ng, v, h2o, co2, n2, o2, Q, Qft, Qfv,
        
        mark_):
    
    global mark
    mark = mark_
    
    # dtdop = 318 # Допустимый перепад
    # n = 10      # Количество узлов # 2025-сделать нечетным (11)
    # s = 0.200   # Толщина сляба м
    # bb = 9.1    # Длина сляба м
    # a = 1.250   # Ширина сляба м

    dx = s/(n-1)
    dtime = 6   

    # toc = 20 + 273 # Т окружающей среды

    alfa_2 = 8+0.05*(toc-273) # Коэффициент конвективной теплоотдачи от футеровки в окр. ср

    # # Параметры футировки
    # dst1 = 0.464  # Толщина первой стены, м
    # dst2 = 0.115  # Толщина второй стены, м
    # tnas = 180 + 273 # температура насыщения при P=10 МПа
    # r2 = 0.146 / 2   # наружний радиус трубы
    # r1 = r2 - 0.030  # внутренний радиус трубы
    # r3 = r2 + 0.0132 # диаметр теплоизоляции

    # time_H = 240 * 60 # Время нагрева в сек

    # tMet_per = 0.1784 # время в процентах методическая зона
    # tSv1_per = 0.2826 # время в процентах первая сварочная зона
    # tSv2_per = 0.2944 # время в процентах во второй зоне
    # tTom_per = 0.2446 # время в процентах в томильной зоне

    # tmn = 20 + 273 # Начальная температура металла
    # twDif = 50 # Разница тепмператур при посаде

    # twMetn = 1050 + 273    # температура методической зоны
    # twMetNpk = 1100 + 273; # температура нижней подогрева методической зоны

    # twSv1n = 1300 + 273    # температура первой сварочной зоны

    # twSv2  = 1350 + 273    # температура второй сварочной зоны
    # twNp2k = 1250 + 273  # температура нижнего подогрева второй сварочной зоны

    # twTom  = 1280 + 273    # температура томильной зоны
    
    # twNp2n = 1250 + 273; # температура нижнего подогрева томильной зоны
    
    # Lp = 35.544 # Длина печи
    
    # # Площадь футеровки по зонам
    # Fmet = 31.05+35.99  # методическая зона
    # Fsv1 = 54.88+49.69  # первая сварочная зона
    # Fsv2 = 92.7+63.4    # во второй зоне
    # Ftom = 41.63+51.65  # в томильной зоне

    # LsioMet = 2*4*Lp*0.189+6.708*2*2 # Суммарная длина труб СИО в методической зон, м
    # LsioSv1 = 4*Lp*0.245+6.708*2*3   # Суммарная длина труб СИО в первой сварочной зоне, м
    # LsioSv2 = 4*Lp*0.312+6.708*2*4   # Суммарная длина труб СИО во второй зоне, м
    # LsioTom = 4*Lp*0.254+6.708*2*2   # Суммарная длина труб СИО в томильной зоне, м

    # lambda_(g): # Коэффициент теплопроводности металла,Вт/(м*К)
    # c(g): # Истиная теплоёмкость металла,Дж/(кг*К)
    # ro(g): # Плотность металла,кг/м^3)
    
    FmetN = 50 # 2025-1
    Fsv1N =100 # 2025-1
    Fsv2N =120 # 2025-1
    
    #--Значения по умолчанию (с почты)--
    Fmet =117.89
    Fsv1 =164.05
    Fsv2 =160.07
    Ftom = 244.94
    FmetN =130.72
    Fsv1N =160.36
    Fsv2N = 163.69
    LsioMet =67
    LsioSv1 =176.5
    LsioSv2 =156.1
    r2 = 0.168/2
    r1 = r2-0.033
    r3 = r2+0.06*LsioPercent/100 #(процент сохранности футеровки сио)(20% -> 20/100, 50% -> 50/100)
    #-----------------------------------
    
    twNp1n=twMetn-100 #2025

    m_l = 100 # Коэффициент теплопроводности металла,Вт/(м*К)
    m_c = 0  # Истиная теплоёмкость металла,Дж/(кг*К)
    m_ro = 900 # Плотность металла,кг/м^3

    G = Lp*bb*s*ro(900)/time_H

    Mslab=a*bb*s*ro(900)
    Nsteps=time_H*G/Mslab

    Qm_ud = 0
    Qm_ud1 = 0
    Qm_ud2 = 0
    
    #t = [[0.0] * 2 for _ in range(100)]
    t = np.zeros((100, 2))
    tx = np.zeros((100, 4))

    twG = np.zeros(700)
    twnG = np.zeros(700)
    tmnG = np.zeros(700)
    tmvG = np.zeros(700)
    tmcG = np.zeros(700)

    # Время нагрева по зонам
    timeMet = time_H * tMet_per # 0.1784 # методическая зона
    timeSv1 = time_H * tSv1_per # 0.2826 # первая сварочная зона
    timeSv2 = time_H * tSv2_per # 0.2944 # во второй зоне
    timeTom = time_H * tTom_per # 0.2446 # в томильной зоне
    
    # Начало расчета

    for i in range(n):  
        t[i][0] = tmn

    time = 0
    dtmax = 0
    nn = 0
    ss = 5

    # Нагрев металла в методической зоне

    w = 1.86

    epr = StCh(w) # Коэффициент излучения на металл

    tw = (twMetn + twSv1n) / 2

    t1, t2, t3, Qf = Fettling(toc, tw, alfa_2, dst1, dst2) # расчет футировки
    
    QfMet=Qf*Fmet # 2025-1
    tw=(twNp1n+twMetNpk)/2 # 2025-1
    
    t1, t2, t3, Qf = Fettling(toc, tw, alfa_2, dst1, dst2) # 2025-1
    QfMetN=Qf*FmetN # 2025-1
    
    # Qr=QmNpMet+QsioMet+QfMetN # 2025-1
    
    p = (1.680+6.708) * 2

    tst, Ql = SIO(p, tw, epr, tnas, r1, r2, r3) # расчет теплопотери от охлаждения

    QsioMet = Ql*LsioMet
    # QfMet = Qf*Fmet #2025-1

    tw = twMetn
    twNp = twMetn-twDif

    while(time <= timeMet):
        tw = twMetn+(twSv1n-twMetn)*time/timeMet
        twNp = (twMetn-twDif)+(twMetNpk-(twMetn-twDif))*time/timeMet

        Temp1(t, n, tw, dx, dtime, epr, tw)
        Qm_ud, Qm_ud1, Qm_ud2, dtmax = Temp2(t, n, twNp, dx, dtime, epr, dtmax, Qm_ud, Qm_ud1, Qm_ud2, time)

        # if time == ss * round(time / ss):   # 2025-2
        #     nn += 1
        #     twG[nn] = tw - 273
        #     twnG[nn] = twNp - 273
        #     tmnG[nn] = t[0, 1] - 273
        #     tmvG[nn] = t[n-1, 1] - 273
        #     tmcG[nn] = t[round(n/2)-1, 1] - 273
        
        time += dtime

    NNmet = nn
    QmMet = Qm_ud2*G
    QmNpMet= Qm_ud1*G

    for i in range(n):
        tx[i][0] = t[i][0]

    # Нагрев металла в первой сварочной зоне

    w = 2.1
    epr = StCh(w)
    tw = (twSv1n+twSv2)/2

    t1, t2, t3, Qf = Fettling(toc, tw, alfa_2, dst1, dst2)

    tst, Ql = SIO(p, tw, epr, tnas, r1, r2, r3)

    QfSv1 = Qf*Fsv1 # 2025-1

    tw = (twMetNpk+twNp2n)/2 # 2025-1
    
    t1, t2, t3, Qf = Fettling(toc, tw, alfa_2, dst1, dst2) # 2025-1
    
    QfSv1N = Qf * Fsv1N
    
    tst, Ql = SIO(p, tw, epr, tnas, r1, r2, r3)
    
    QsioSv1 = Ql*LsioSv1
    
    tw=twSv1n
    twNp = twMetNpk 

    while time<(timeMet+timeSv1):
        tw = twSv1n+(twSv2-twSv1n)*(time-timeMet)/timeSv1
        twNp = twMetNpk+(twNp2n-twMetNpk)*(time-timeMet)/timeSv1

        Temp1(t, n, tw, dx, dtime, epr, tw)
        Qm_ud, Qm_ud1, Qm_ud2, dtmax = Temp2(t, n, twNp, dx, dtime, epr, dtmax, Qm_ud, Qm_ud1, Qm_ud2, time)

        # if time == ss * round(time / ss):  # 2025-2
        #     nn += 1
        #     twG[nn] = round(tw - 273)
        #     twnG[nn] = twNp - 273
        #     tmnG[nn] = t[0, 1] - 273
        #     tmvG[nn] = t[n-1, 1] - 273
        #     tmcG[nn] = t[round(n/2), 1] - 273

        time += dtime

    NNsv1 = nn
    QmSv1 = Qm_ud2*G-QmMet
    # QmNp1 = Qm_ud1*G # 2025
    QmNpSv1 = Qm_ud1*G-QmNpMet # 2025

    for i in range(n):
        tx[i][1] = t[i][0]

    
    # Нагрев металла во второй сварочной зоне
    w = 2.5
    epr = StCh(w)
    tw = twSv2

    t1, t2, t3, Qf = Fettling(toc, tw, alfa_2, dst1, dst2)

    Qfsv2 = Qf*Fsv2 # 2025-1
    tw=twNp2n
    t1, t2, t3, Qf = Fettling(toc, tw, alfa_2, dst1, dst2)
    QfSv2N = Qf*Fsv2N # 2025-1
    p = (1.960+6.708)*2

    tst, Ql = SIO(p, tw, epr, tnas, r1, r2, r3)

    QsioSv2 = Ql*LsioSv2
    # Qfsv2 = Qf*Fsv2 # 2025-1
    # k4 = (twNp2k-twNp2n)/(timeSv2+timeTom) # 2025-1
    twNp = twNp2n

    while(time<(timeMet + timeSv1 + timeSv2)):
        Temp1(t, n, tw, dx, dtime, epr, tw)
        Qm_ud, Qm_ud1, Qm_ud2, dtmax = Temp2(t, n, twNp, dx, dtime, epr, dtmax, Qm_ud, Qm_ud1, Qm_ud2, time)

        # if time == ss * round(time / ss): # 2025-2
        #     nn += 1
        #     twG[nn] = round(tw - 273)
        #     twnG[nn] = twNp - 273
        #     tmnG[nn] = t[0, 1] - 273
        #     tmvG[nn] = t[n-1, 1] - 273
        #     tmcG[nn] = t[round(n/2), 1] - 273

        time += dtime
    
    nnSv2 = nn
    QmSv2 = Qm_ud2*G-QmMet-QmSv1
    QmNp2=Qm_ud1*G-QmNpSv1-QmNpMet # 2025

    for i in range(n):
        tx[i][2] = t[i][0]


    # Нагрев металла в томильной зоне
    w = 1.8
    epr = StCh(w)
    tw = twTom

    t1, t2, t3, Qf = Fettling(toc, tw, alfa_2, dst1, dst2)

    tst, Ql = SIO(p, tw, epr, tnas, r1, r2, r3)

    QsioTom = Ql*LsioTom
    Qftom = Qf*Ftom
    twNp = twNp2n # 2025

    while(time < time_H):
        Temp1(t, n, tw, dx, dtime, epr, tw)
        Qm_ud, Qm_ud1, Qm_ud2, dtmax = Temp3(t, n, twNp, dx, dtime, epr, dtmax, Qm_ud, Qm_ud1, Qm_ud2, time)

        # if time == ss * round(time / ss): # 2025-2
        #     nn += 1
        #     twG[nn] = round(tw - 273)
        #     twnG[nn] = twNp - 273
        #     tmnG[nn] = t[0, 1] - 273
        #     tmvG[nn] = t[n-1, 1] - 273
        #     tmcG[nn] = t[round(n/2), 1] - 273

        time += dtime

    # QmTom = Qm_ud2*G-QmMet-QmSv1-QmSv2 # 2025
    QmTom = (Qm_ud1+Qm_ud2)*G-QmMet-QmSv1-QmSv2-QmNpSv1-QmNp2-QmNpMet # 2025
    # QmNp2 = Qm_ud1*G-QmNp1 # 2025
    tcpm = 0

    for i in range(n):
        tx[i][3] = t[i][0]
        tcpm += tx[i][3] / n

    results = {
        "Расчет нагрева металла": {},
        "Тепловой баланс": {},
        "График": {},
        "data" : {},
        "t_data" : {}
    } 

    results["data"]["Время нагрева (time_H)"] = time_H
    results["data"]["Время в методической зоне"] = timeMet
    results["data"]["Время в первой сварочной зоне"] = timeSv1
    results["data"]["Время во второй сварочной зоне"] = timeSv2
    results["data"]["Время в томильной зоне"] = timeTom
    results["t_data"]["Температура сляба при посаде"] = tmn
    results["t_data"]["Температура верха печи при посаде"] = twMetn
    results["t_data"]["Температура низа печи при посаде"] = twMetn - twDif

    results["Расчет нагрева металла"]["Методическая зона"] = {
        "tпечи, °C" : f"{twMetn - 273} - {twSv1n - 273}",
        "tпов1, °C" : tx[n-1][0]-273,
        "tпов2, °C" : tx[0][0]-273,
        "Tц, °C" : tx[round(n/2)-1][0]-273,
        "tниз, °C" : f"{twNp1n-273} - {twMetNpk-273}" # 2025
    }

    results["Расчет нагрева металла"]["Первая сварочная зона"] = {
        "tпечи, °C" : f"{twSv1n - 273} - {twSv2 - 273}",
        "tпов1, °C" : tx[n-1][1]-273,
        "tпов2, °C" : tx[0][1]-273,
        "Tц, °C" : tx[round(n/2)-1][1]-273,
        "tниз, °C" : f"{twMetNpk-273-twDif} - {twNp2n-273}"
    }

    results["Расчет нагрева металла"]["Вторая сварочная зона"] = {
        "tпечи, °C" : twSv2-273,
        "tпов1, °C" : tx[n-1][2]-273,
        "tпов2, °C" : tx[0][2]-273,
        "Tц, °C" : tx[round(n/2)-1][2]-273,
        "tниз, °C" : twNp2n-273
    }

    results["Расчет нагрева металла"]["Томильная зона"] = {
        "tпечи, °C" : twTom-273,
        "tпов1, °C" : tx[n-1][3]-273,
        "tпов2, °C" : tx[0][3]-273,
        "Tц, °C" : tx[round(n/2)-1][3]-273,
        # "tниз, °C" : twNp2k-273 # 2025
    }

    # Вычисление времени нагрева
    heating_hours = int(time_H // 3600)
    heating_minutes = (time_H / 3600 - heating_hours) * 60

    # n_cage = 2.2939 * tcpm - 1688
    n_cage = 2.11 * (tcpm-273) - 1461.4 

    if(n_cage > 1150):
        n_cage = 1150
 
    results["Расчет нагрева металла"]["Время нагрева, ч:м"] = f"{heating_hours} :{heating_minutes:2.0f}"
    results["Расчет нагрева металла"]["Масса сляба, т"] = f"{Mslab / 1000:2.3f}"
    results["Расчет нагрева металла"]["Производительность печи, т/час"] = f"{G / 1000 * 3600:2.2f}"
    results["Расчет нагрева металла"]["Среднемассовая температура металла, °C"] = f"{tcpm-273:4.0f}"
    results["Расчет нагрева металла"]["Температура раската за пятой клетью (T5), °C"] = f"{n_cage:4.0f}"
    results["Расчет нагрева металла"]["Конечный перепад температур, °C"] = f"{t[n-1][0] - t[round(n/2)-1][0]:0.1f}"
    results["Расчет нагрева металла"]["Максимальный перепад температур, °C"] = f"{dtmax:0.0f}"
    results["Расчет нагрева металла"]["Кол-во теплоты получаемое металлом, кДж/кг"] = f"{Qm_ud / 1000:0.0f}"

    Qd_Tom_ud = v * cd(twTom, h2o, co2, n2, o2) * (twTom - 273)
    Qd_Sv2_ud = v * cd(twSv2, h2o, co2, n2, o2) * (twSv2 - 273)
    Qd_Sv1_ud = v * cd(twSv1n, h2o, co2, n2, o2) * (twSv1n - 273)
    Qd_Np2_ud = v * cd(twNp2n, h2o, co2, n2, o2) * (twNp2n - 273)
    Qd_Np1_ud = v * cd(twMetNpk, h2o, co2, n2, o2) * (twMetNpk-273) # 2025 

    QwindowTom = 2.89 * 6.7 * (twTom / 100) ** 4
    QwindowMet = 3.34 * 6.7 * (twMetn / 100) ** 4

    B_Tom = (QmTom + Qftom + QwindowTom) / (Q + Qft + Qfv - Qd_Tom_ud)
    Qtr_Sv2 = B_Tom * v * ((twTom - 273) * cd(twTom, h2o, co2, n2, o2) - (twSv2 - 273) * cd(twSv2, h2o, co2, n2, o2))

    B_Sv2 = (QmSv2 + Qfsv2 - Qtr_Sv2) / (Q + Qft + Qfv - Qd_Sv2_ud)
    Qtr_Sv1 = (B_Tom + B_Sv2) * v * ((twSv2 - 273) * cd(twSv2, h2o, co2, n2, o2) - (twSv1n - 273) * cd(twSv1n, h2o, co2, n2, o2))

    kSv1 = 0.15

    B_Sv1 = (QmSv1 + QfSv1 + kSv1 * (QmNpSv1 + QsioSv1) - Qtr_Sv1) / (Q + Qft + Qfv - Qd_Sv1_ud)
    B_Np = (QsioSv2 + QsioTom + QmNp2) / (Q + Qft + Qfv - Qd_Np2_ud)
    
    B_Np4 = (QsioSv2+QsioTom+QmNp2+QfSv2N)/(Q+Qft+Qfv-Qd_Np2_ud) # 2025  {Расход газа в зоне нижнего подогрева 4,м^3/сек}
    Qtr_Np1=B_Np4*v*((twNp2n-273)*cd(twNp2n, h2o, co2, n2, o2)-(twMetNpk-273)*cd(twMetNpk, h2o, co2, n2, o2)) # 2025
    B_Np2=(QsioSv1+QmNpSv1+QfSv1N-Qtr_Np1)/(Q+Qft+Qfv-Qd_Np1_ud) # 2025  {Расход газа в зоне нижнего подогрева 2,м^3/сек}

    B = B_Tom + B_Sv1 + B_Sv2 + B_Np4 + B_Np2 # 2025
    
    twMetn_ = twMetn # 2025
    twMetn = (((twSv1n-273)*cd(twSv1n, h2o, co2, n2, o2)-(QmMet+QfMet+QwindowMet)/(B_Tom+B_Sv1+B_Sv2)/v)/cd(twMetn, h2o, co2, n2, o2)+273+twMetn)/2 # 2025

    twNpn_ = twNp1n
    twNp1n = (((twNp2n-273)*cd(twNp2n, h2o, co2, n2, o2)-(QmNpMet+QsioMet+QfMetN)/(B_Np2+B_Np4)/v)/cd(twNp1n, h2o, co2, n2, o2)+273+twNp1n)/2
    
    # if (abs(twNp1n-twNpn_)>1) or (abs(twMetn-twMetn_)>1): #2025 (решить)
        # break
    
    Qtr_Met_V=(B_Tom+B_Sv1+B_Sv2)*v*((twSv1n-273)*cd(twSv1n, h2o, co2, n2, o2)-(twMetn-273)*cd(twMetn, h2o, co2, n2, o2)) # 2025
    Qtr_Met_N=(B_Np2+B_Np4)*v*((twNp2n-273)*cd(twNp2n, h2o, co2, n2, o2)-(twNp1n-273)*cd(twNp1n, h2o, co2, n2, o2)) # 2025
    
    QfSv1N = Qf * Fsv1N # 2025-1
    Qd_Np1_ud = v * cd(twMetNpk, h2o, co2, n2, o2) * (twMetNpk-273) # 2025

    QfSv2N = Qf*Fsv2N # 2025-1
    

    Qd_Tom = Qd_Tom_ud*B_Tom
    Qd_Sv2 = Qd_Sv2_ud*B_Sv2
    Qd_Sv1 = Qd_Sv1_ud*B_Sv1
    Qd_Np2 = Qd_Np2_ud*B_Np4 # 2025
    Qd_Np1 = Qd_Np1_ud*B_Np2 # 2025

    B_ud = B/G*1000

    results["Расчет нагрева металла"]["Расход топлива на печь, тыс. м³/час"] = f"{B / 1000 * 3600:.2f}"

    results["Расчет нагрева металла"]["Расход топлива по зонам:"] = {
        "в первой сварочной зоне, тыс. м³/час" : f"{B_Sv1 / 1000 * 3600:.3f}",
        "в первой сварочной зоне, %" : f"{B_Sv1 / B * 100:.1f}",
        "во второй сварочной зоне, тыс. м³/час" : f"{B_Sv2 / 1000 * 3600:.3f}",
        "во второй сварочной зоне, %" : f"{B_Sv2 / B * 100:.1f}",
        "в томильной зоне, тыс. м³/час" : f"{B_Tom / 1000 * 3600:.3f}",
        "в томильной зоне, %" : f"{B_Tom / B * 100:.1f}",
        "в зоне нижнего подогрева, тыс. м³/час" : f"{B_Np / 1000 * 3600:.3f}",
        "в зоне нижнего подогрева, %" : f"{B_Np / B * 100:.1f}",
        "в зоне нижнего подогрева 2, тыс. м³/час" : f"{B_Np2 / 1000 * 3600:.3f}", # 2025
        "в зоне нижнего подогрева 2, %" : f"{B_Np2 / B * 100:.1f}", # 2025
        "в зоне нижнего подогрева 4, тыс. м³/час" : f"{B_Np4 / 1000 * 3600:.3f}", # 2025
        "в зоне нижнего подогрева 4, %" : f"{B_Np4 / B * 100:.1f}", # 2025
    }
    results["Расчет нагрева металла"]["Удельный расход топлива, м³/т"] = f"{B_ud:.0f}"
    results["Расчет нагрева металла"]["Удельный расход природного газа, м³/т"] = f"{B_ud * (ng / 100):.0f}"
    results["Расчет нагрева металла"]["Себестоимость нагрева, тг/т"] = f"{B_ud * Ts / 1000:.2f}"

    Qpr = B * (Q + Qfv + Qft)
    Qm = Qm_ud * G
    Qm_ = Qm / Qpr * 100

    results["Расчет нагрева металла"]["КПД нагрева, %"] = f"{Qm_:5.1f}"
    results["Расчет нагрева металла"]["Удельный расход условного топлива, кг у.т. /т"] = f"{B_ud*Q/1_000_000/29.33:0.1f}"
    # print(f"КПД нагрева                          {Qm_:5.1f} %")
        
    Qr = QmMet+QfMet+QsioMet+QwindowMet
    Qpr = Qtr_Met_V
    Qm_ = QmMet/Qr*100
    Qf_ = QfMet/Qr*100
    Qsio_ = QsioMet/Qr*100
    Qwindow_ = QwindowMet/Qr*100 

    results["Тепловой баланс"]["Методическая зона верх"] = {
        "Приход тепла": {
            "Тепло транзитных газов, MВт" : f"{Qtr_Met_V / 1_000_000:5.2f}",
            "Тепло транзитных газов, %" : f"{Qtr_Met_V / Qpr * 100:5.1f}",
            "Итого приход, MВт" : f"{Qpr / 1_000_000:5.2f}",
            "Итого приход, %" : f"{Qtr_Met_V / Qpr * 100:5.1f}"
        },
        "Расход тепла": {
            "Тепло на нагрев металла, MВт": f"{QmMet / 1_000_000:5.2f}",
            "Тепло на нагрев металла, %": f"{Qm_:5.1f}",
            "Потери через кладку, MВт": f"{QfMet / 1_000_000:5.2f}",
            "Потери через кладку, %": f"{Qf_:5.1f}",
            "Потери через СИО, MВт": f"{QsioMet / 1_000_000:5.2f}",
            "Потери через СИО, %": f"{Qsio_:5.1f}",
            "Потери через окно посада, MВт": f"{QwindowMet / 1_000_000:5.2f}",
            "Потери через окно посада, %": f"{Qwindow_:5.1f}",
            "Итого расход, MВт": f"{Qr / 1_000_000:5.2f}",
            "Итого расход, %": f"{(Qm_ + Qf_ + Qwindow_):5.1f}"
        }
    }
    
    
    Qpr=Qtr_Met_N
    
    results["Тепловой баланс"]["Методическая зона низ"] = {
        "Приход тепла": {
            "Тепло транзитных газов, MВт" : f"{Qtr_Met_N / 1_000_000:5.2f}",
            "Тепло транзитных газов, %" : f"{Qtr_Met_N / Qpr * 100:5.1f}",
            "Итого приход, MВт" : f"{Qpr / 1_000_000:5.2f}",
            "Итого приход, %" : f"{Qtr_Met_N / Qpr * 100:5.1f}"
        },
        "Расход тепла": {
            "Тепло на нагрев металла, MВт": f"{QmMet / 1_000_000:5.2f}",
            "Тепло на нагрев металла, %": f"{Qm_:5.1f}",
            "Потери через кладку, MВт": f"{QfMet / 1_000_000:5.2f}",
            "Потери через кладку, %": f"{Qf_:5.1f}",
            "Потери через СИО, MВт": f"{QsioMet / 1_000_000:5.2f}",
            "Потери через СИО, %": f"{Qsio_:5.1f}",
            "Потери через окно посада, MВт": f"{QwindowMet / 1_000_000:5.2f}",
            "Потери через окно посада, %": f"{Qwindow_:5.1f}",
            "Итого расход, MВт": f"{Qr / 1_000_000:5.2f}",
            "Итого расход, %": f"{(Qm_ + Qf_ + Qwindow_):5.1f}"
        }
    }


    Qtr_Met = Qr
    
    results["Тепловой баланс"]["Методическая зона"] = {
        "Приход тепла": {
            "Тепло транзитных газов, MВт" : f"{Qtr_Met / 1_000_000:5.2f}",
            "Тепло транзитных газов, %" : f"{Qtr_Met / Qpr * 100:5.1f}",
            "Итого приход, MВт" : f"{Qpr / 1_000_000:5.2f}",
            "Итого приход, %" : f"{Qtr_Met / Qpr * 100:5.1f}"
        },
        "Расход тепла": {
            "Тепло на нагрев металла, MВт": f"{QmMet / 1_000_000:5.2f}",
            "Тепло на нагрев металла, %": f"{Qm_:5.1f}",
            "Потери через кладку, MВт": f"{QfMet / 1_000_000:5.2f}",
            "Потери через кладку, %": f"{Qf_:5.1f}",
            "Потери через СИО, MВт": f"{QsioMet / 1_000_000:5.2f}",
            "Потери через СИО, %": f"{Qsio_:5.1f}",
            "Потери через окно посада, MВт": f"{QwindowMet / 1_000_000:5.2f}",
            "Потери через окно посада, %": f"{Qwindow_:5.1f}",
            "Итого расход, MВт": f"{Qr / 1_000_000:5.2f}",
            "Итого расход, %": f"{(Qm_ + Qf_ + Qsio_ + Qwindow_):5.1f}"
        }
    }
    
    Qpr = (Q+Qfv+Qft)*B_Sv1+Qtr_Sv1
    Qr = QmSv1+QfSv1+Qd_Sv1 #+kSv1*(QsioSv1+QmNpSv1)   # 2025
    Q_ = Q*B_Sv1/Qpr*100
    Qfv_ = Qfv*B_Sv1/Qpr*100
    Qft_ = Qft*B_Sv1/Qpr*100
    Qtr_ = Qtr_Sv1/Qpr*100
    Qm_ = (QmSv1+QmNpSv1*kSv1)/Qr*100
    Qf_ = QfSv1/Qr*100
    Qsio_ = kSv1*QsioSv1/Qr*100
    Qd_ = Qd_Sv1/Qr*100

    results["Тепловой баланс"]["Первая сварочная зона"] = {
        "Приход тепла": {
            "Химическое тепло топлива, MВт": f"{Q * B_Sv1 / 1_000_000:5.2f}",
            "Химическое тепло топлива, %": f"{Q_:5.1f}",
            "Физическое тепло воздуха, MВт": f"{Qfv * B_Sv1 / 1_000_000:5.2f}",
            "Физическое тепло воздуха, %": f"{Qfv_:5.1f}",
            "Физическое тепло газа, MВт": f"{Qft * B_Sv1 / 1_000_000:5.2f}",
            "Физическое тепло газа, %": f"{Qft_:5.1f}",
            "Тепло транзитных газов, MВт": f"{Qtr_Sv1 / 1_000_000:5.2f}",
            "Тепло транзитных газов, %": f"{Qtr_:5.1f}",
            "Итого приход, MВт": f"{Qpr / 1_000_000:5.2f}",
            "Итого приход, %": f"{(Q_ + Qfv_ + Qft_ + Qtr_):5.1f}"
        },
        "Расход тепла": {
            "Тепло на нагрев металла, MВт": f"{QmSv1 / 1_000_000:5.2f}",
            "Тепло на нагрев металла, %": f"{Qm_:5.1f}",
            "Потери через кладку, MВт": f"{QfSv1 / 1_000_000:5.2f}",
            "Потери через кладку, %": f"{Qf_:5.1f}",
            "Тепло уходящее с дымом, MВт": f"{Qd_Sv1 / 1_000_000:5.2f}",
            "Тепло уходящее с дымом, %": f"{Qd_:5.1f}",
            "Потери через СИО, MВт": f"{kSv1 * QsioSv1 / 1_000_000:5.2f}",
            "Потери через СИО, %": f"{Qsio_:5.1f}",
            "Итого расход, MВт": f"{Qr / 1_000_000:5.2f}",
            "Итого расход, %": f"{(Qm_ + Qf_ + Qd_ + Qsio_):5.1f}"
        },

        "Расход топлива, тыс. м³/час": f"{B_Sv1 / 1_000 * 3600:0.3f}"
    }

    Qpr = (Q+Qfv+Qft)*B_Sv2+Qtr_Sv2
    Qr = QmSv2+Qfsv2+Qd_Sv2
    Q_ = Q*B_Sv2/Qpr*100
    Qfv_ = Qfv*B_Sv2/Qpr*100
    Qft_ = Qft*B_Sv2/Qpr*100
    Qtr_ = Qtr_Sv2/Qpr*100
    Qm_ = QmSv2/Qr*100
    Qf_ = Qfsv2/Qr*100
    Qd_ = Qd_Sv2/Qr*100

    results["Тепловой баланс"]["Вторая сварочная зона"] = {
        "Приход тепла": {
            "Химическое тепло топлива, MВт": f"{Q * B_Sv2 / 1_000_000:5.2f}",
            "Химическое тепло топлива, %": f"{Q_:5.1f}",
            "Физическое тепло воздуха, MВт": f"{Qfv * B_Sv2 / 1_000_000:5.2f}",
            "Физическое тепло воздуха, %": f"{Qfv_:5.1f}",
            "Физическое тепло газа, MВт": f"{Qft * B_Sv2 / 1_000_000:5.2f}",
            "Физическое тепло газа, %": f"{Qft_:5.1f}",
            "Тепло транзитных газов, MВт": f"{Qtr_Sv2 / 1_000_000:5.2f}",
            "Тепло транзитных газов, %": f"{Qtr_:5.1f}",
            "Итого приход, MВт": f"{Qpr / 1_000_000:5.2f}",
            "Итого приход, %": f"{(Q_ + Qfv_ + Qft_ + Qtr_):5.1f}"
        },
        "Расход тепла": {
            "Тепло на нагрев металла, MВт": f"{QmSv2 / 1_000_000:5.2f}",
            "Тепло на нагрев металла, %": f"{Qm_:5.1f}",
            "Потери через кладку, MВт": f"{Qfsv2 / 1_000_000:5.2f}",
            "Потери через кладку, %": f"{Qf_:5.1f}",
            "Тепло уходящее с дымом, MВт": f"{Qd_Sv2 / 1_000_000:5.2f}",
            "Тепло уходящее с дымом, %": f"{Qd_:5.1f}",
            "Итого расход, MВт": f"{Qr / 1_000_000:5.2f}",
            "Итого расход, %": f"{(Qm_ + Qf_ + Qd_):5.1f}"
        },
        "Расход топлива, тыс. м³/час": f"{B_Sv2 / 1_000 * 3600:0.3f}"
    }

    Qpr = (Q+Qfv+Qft)*B_Tom
    Qr = QmTom+Qftom+Qd_Tom+QwindowTom
    Q_ = Q*B_Tom/Qpr*100
    Qfv_ = Qfv*B_Tom/Qpr*100
    Qft_ = Qft*B_Tom/Qpr*100
    Qm_ = QmTom/Qr*100
    Qf_ = Qftom/Qr*100
    Qwindow_ = QwindowTom/Qr*100
    Qd_ = Qd_Tom/Qr*100

    results["Тепловой баланс"]["Томильная зона"] = {
        "Приход тепла": {
            "Химическое тепло топлива, MВт": f"{Q * B_Tom / 1_000_000:5.2f}",
            "Химическое тепло топлива, %": f"{Q_:5.1f}",
            "Физическое тепло воздуха, MВт": f"{Qfv * B_Tom / 1_000_000:5.2f}",
            "Физическое тепло воздуха, %": f"{Qfv_:5.1f}",
            "Физическое тепло газа, MВт": f"{Qft * B_Tom / 1_000_000:5.2f}",
            "Физическое тепло газа, %": f"{Qft_:5.1f}",
            "Итого приход, MВт": f"{Qpr / 1_000_000:5.2f}",
            "Итого приход, %": f"{(Q_ + Qfv_ + Qft_):5.1f}"
        },
        "Расход тепла": {
            "Тепло на нагрев металла, MВт": f"{QmTom / 1_000_000:5.2f}",
            "Тепло на нагрев металла, %": f"{Qm_:5.1f}",
            "Потери через кладку, MВт": f"{Qftom / 1_000_000:5.2f}",
            "Потери через кладку, %": f"{Qf_:5.1f}",
            "Тепло уходящее с дымом, MВт": f"{Qd_Tom / 1_000_000:5.2f}",
            "Тепло уходящее с дымом, %": f"{Qd_:5.1f}",
            "Потери через окно выдачи, MВт": f"{QwindowTom / 1_000_000:5.2f}",
            "Потери через окно выдачи, %": f"{Qwindow_:5.1f}",
            "Итого расход, MВт": f"{Qr / 1_000_000:5.2f}",
            "Итого расход, %": f"{(Qm_ + Qf_ + Qd_ + Qwindow_):5.1f}"
        },
        "Расход топлива, тыс. м³/час": f"{B_Tom / 1_000 * 3600:0.3f}"
    }

    Qpr = (Q+Qfv+Qft)*B_Np
    Qr = QmNp2+Qd_Np2+QsioTom+QsioSv2
    Q_ = Q*B_Np/Qpr*100
    Qfv_ = Qfv*B_Np/Qpr*100
    Qft_ = Qft*B_Np/Qpr*100
    Qm_ = QmNp2/Qr*100
    Qsio_ = (QsioTom+QsioSv2)/Qr*100
    Qd_ = Qd_Np2/Qr*100

    results["Тепловой баланс"]["Зона нижнего подогрева"] = {
        "Приход тепла": {
            "Химическое тепло топлива, MВт": f"{Q * B_Np / 1_000_000:5.2f}",
            "Химическое тепло топлива, %": f"{Q_:5.1f}",
            "Физическое тепло воздуха, MВт": f"{Qfv * B_Np / 1_000_000:5.2f}",
            "Физическое тепло воздуха, %": f"{Qfv_:5.1f}",
            "Физическое тепло газа, MВт": f"{Qft * B_Np / 1_000_000:5.2f}",
            "Физическое тепло газа, %": f"{Qft_:5.1f}",
            "Итого приход, MВт": f"{Qpr / 1_000_000:5.2f}",
            "Итого приход, %": f"{(Q_ + Qfv_ + Qft_):5.1f}"
        },
        "Расход тепла": {
            "Тепло на нагрев металла, MВт": f"{QmNp2 / 1_000_000:5.2f}",
            "Тепло на нагрев металла, %": f"{Qm_:5.1f}",
            "Тепло уходящее с дымом, MВт": f"{Qd_Np2 / 1_000_000:5.2f}",
            "Тепло уходящее с дымом, %": f"{Qd_:5.1f}",
            "Потери через СИО, MВт": f"{(QsioTom + QsioSv2) / 1_000_000:5.2f}",
            "Потери через СИО, %": f"{Qsio_:5.1f}",
            "Итого расход, MВт": f"{Qr / 1_000_000:5.2f}",
            "Итого расход, %": f"{(Qm_ + Qd_ + Qsio_):5.1f}"
        },
        "Расход топлива, тыс. м³/час": f"{B_Np / 1_000 * 3600:0.3f}"
    }
    
    
    # Зона нижнего подогрева 2 #2025
    Qpr=(Q+Qfv+Qft)*B_Np2+Qtr_Np1
    Qr=QmNpSv1+Qd_Np1+QsioSv1+QfSv1N
    Q_=Q*B_Np2/Qpr*100
    Qfv_=Qfv*B_Np2/Qpr*100
    Qft_=Qft*B_Np2/Qpr*100
    Qtr_=Qtr_Np1/Qpr*100
    Qm_=QmNpSv1/Qr*100
    Qf_=QfSv1N/Qr*100 #2025-1
    Qsio_=QsioSv1/Qr*100
    Qd_=Qd_Np1/Qr*100
    
    results["Тепловой баланс"]["Зона нижнего подогрева 2"] = {
        "Приход тепла": {
            "Химическое тепло топлива, MВт": f"{Q * B_Np2 / 1_000_000:5.2f}",
            "Химическое тепло топлива, %": f"{Q_:5.1f}",
            "Физическое тепло воздуха, MВт": f"{Qfv * B_Np2 / 1_000_000:5.2f}",
            "Физическое тепло воздуха, %": f"{Qfv_:5.1f}",
            "Физическое тепло газа, MВт": f"{Qft * B_Np2 / 1_000_000:5.2f}",
            "Физическое тепло газа, %": f"{Qft_:5.1f}",
            "Тепло транзитных газов, MВт": f"{Qtr_Np1 / 1_000_000:5.2f}",
            "Тепло транзитных газов, %": f"{Qtr_:5.1f}",
            "Итого приход, MВт": f"{Qpr / 1_000_000:5.2f}",
            "Итого приход, %": f"{(Q_ + Qfv_ + Qft_ + Qtr_):5.1f}"
        },
        "Расход тепла": {
            "Тепло на нагрев металла, MВт": f"{QmNpSv1 / 1_000_000:5.2f}",
            "Тепло на нагрев металла, %": f"{Qm_:5.1f}",
            "Потери через кладку, MВт": f"{QfSv1N / 1_000_000:5.2f}",
            "Потери через кладку, %": f"{Qf_:5.1f}",
            "Тепло уходящее с дымом, MВт": f"{Qd_Np1 / 1_000_000:5.2f}",
            "Тепло уходящее с дымом, %": f"{Qd_:5.1f}",
            "Потери через СИО, MВт": f"{(QsioSv1) / 1_000_000:5.2f}",
            "Потери через СИО, %": f"{Qsio_:5.1f}",
            "Итого расход, MВт": f"{Qr / 1_000_000:5.2f}",
            "Итого расход, %": f"{(Qm_ + Qf_ + Qd_ + Qsio_):5.1f}"
        },
        "Расход топлива, тыс. м³/час": f"{B_Np2 / 1_000 * 3600:0.3f}"
    }
    
    
    Qpr=(Q+Qfv+Qft)*B_Np4 # 2025
    Qr=QmNp2+Qd_Np2+QsioSv2+QfSv2N # 2025-1
    Q_=Q*B_Np4/Qpr*100 # 2025
    Qfv_=Qfv*B_Np4/Qpr*100 # 2025
    Qft_=Qft*B_Np4/Qpr*100 # 2025
    Qm_=QmNp2/Qr*100
    Qf_=QfSv2N/Qr*100
    Qsio_=QsioSv2/Qr*100
    Qd_=Qd_Np2/Qr*100
    
    results["Тепловой баланс"]["Зона нижнего подогрева 4"] = {
        "Приход тепла": {
            "Химическое тепло топлива, MВт": f"{Q * B_Np4 / 1_000_000:5.2f}", #2025
            "Химическое тепло топлива, %": f"{Q_:5.1f}",
            "Физическое тепло воздуха, MВт": f"{Qfv * B_Np4 / 1_000_000:5.2f}", #2025
            "Физическое тепло воздуха, %": f"{Qfv_:5.1f}",
            "Физическое тепло газа, MВт": f"{Qft * B_Np4 / 1_000_000:5.2f}", #2025
            "Физическое тепло газа, %": f"{Qft_:5.1f}",
            "Итого приход, MВт": f"{Qpr / 1_000_000:5.2f}",
            "Итого приход, %": f"{(Q_ + Qfv_ + Qft_):5.1f}"
        },
        "Расход тепла": {
            "Тепло на нагрев металла, MВт": f"{QmNp2 / 1_000_000:5.2f}",
            "Тепло на нагрев металла, %": f"{Qm_:5.1f}",
            "Потери через кладку, MВт": f"{QfSv2N / 1_000_000:5.2f}",
            "Потери через кладку, %": f"{Qf_:5.1f}",
            "Тепло уходящее с дымом, MВт": f"{Qd_Np2 / 1_000_000:5.2f}",
            "Тепло уходящее с дымом, %": f"{Qd_:5.1f}",
            "Потери через СИО, MВт": f"{(QsioTom + QsioSv2) / 1_000_000:5.2f}",
            "Потери через СИО, %": f"{Qsio_:5.1f}",
            "Итого расход, MВт": f"{Qr / 1_000_000:5.2f}",
            "Итого расход, %": f"{(Qm_ + Qf_ + Qd_ + Qsio_):5.1f}"
        },
        "Расход топлива, тыс. м³/час": f"{B_Np4 / 1_000 * 3600:0.3f}"
    }
    
    QfSv2=Qf*Fsv2 # 2025-1
    QfSv2N=Qf*Fsv2N # 2025-1

    B=B_Tom+B_Sv1+B_Sv2+B_Np2+B_Np4 # 2025
    B_ud = B/G*1000
    Qm = Qm_ud*G
    Qd=((B_Tom+B_Sv2+B_Sv1))*v*cd(twMetn, h2o, co2, n2, o2)*(twMetn-273)+(B_Np2+B_Np4)*v*cd(twNp1n, h2o, co2, n2, o2)*(twNp1n-273) # 2025
    Qpr = B*(Q+Qfv+Qft)
    Qr = Qm+(QfMet+QfSv1+Qfsv2+Qftom)+Qd+(QsioMet+QsioSv1+QsioSv2+QsioTom)+QwindowTom+QwindowMet
    Q_ = B*Q/Qpr*100 # 2025-1
    Qfv_ = B*Qfv/Qpr*100 # 2025-1
    Qft_ = B*Qft/Qpr*100 # 2025-1
    Qm_ = Qm/Qpr*100 # 2025-1
    Qsio_ = (QsioMet+QsioSv1+QsioSv2+QsioTom)/Qpr*100 # 2025-1
    Qf_=(QfMet+QfSv1+QfSv2+Qftom+QfMetN+QfSv1N+QfSv2N)/Qpr*100 # 2025-1
    Qd_ = Qd/Qpr*100 # 2025-1
    Qwindow_=(QwindowTom+QwindowMet)/Qpr*100 # 2025-1

    results["Тепловой баланс"]["Тепловой баланс печи"] = {
        "Приход тепла": {
            "Химическое тепло топлива, MВт": f"{B * Q / 1_000_000:5.2f}",
            "Химическое тепло топлива, %": f"{Q_:5.1f}",
            "Физическое тепло воздуха, MВт": f"{B * Qfv / 1_000_000:5.2f}",
            "Физическое тепло воздуха, %": f"{Qfv_:5.1f}",
            "Физическое тепло газа, MВт": f"{B * Qft / 1_000_000:5.2f}",
            "Физическое тепло газа, %": f"{Qft_:5.1f}",
            "Итого приход, MВт": f"{Qpr / 1_000_000:5.2f}",
            "Итого приход, %": f"{(Q_ + Qfv_ + Qft_):5.1f}"
        },
        "Расход тепла": {
            "Тепло на нагрев металла, MВт": f"{Qm / 1_000_000:5.2f}",
            "Тепло на нагрев металла, %": f"{Qm_:5.1f}",
            "Потери через кладку, MВт": f"{(QfMet+QfSv1+QfSv2+Qftom+QfMetN+QfSv1N+QfSv2N) / 1_000_000:5.2f}",
            "Потери через кладку, %": f"{Qf_:5.1f}",
            "Тепло уходящее с дымом, MВт": f"{Qd / 1_000_000:5.2f}",
            "Тепло уходящее с дымом, %": f"{Qd_:5.1f}",
            "Потери через СИО, MВт": f"{(QsioMet + QsioSv1 + QsioSv2 + QsioTom) / 1_000_000:5.2f}",
            "Потери через СИО, %": f"{Qsio_:5.1f}",
            "Потери излучением ч/з окна, MВт": f"{QwindowTom / 1_000_000:5.2f}",
            "Потери излучением ч/з окна, %": f"{Qwindow_:5.1f}",
            "Итого расход, MВт": f"{Qr / 1_000_000:5.2f}",
            "Итого расход, %": f"{(Qm_ + Qf_ + Qd_ + Qsio_ + Qwindow_):5.1f}"
        },
        "Расход топлива, тыс. м³/час": f"{B / 1_000 * 3600:0.2f}"
    }

    # import matplotlib.pyplot as plt

    # 🔹 Данные (заполни своими значениями)
    #t = np.linspace(0, time_H / 60, 700)  # Время от 0 до 240 минут

    t = np.arange(0, nn * ss * dtime, ss * dtime) / 60  

    results["График"]["t"] = t

    results["График"]["время"] = time_H / 60

    results["График"]["Печь (верх)"] = twG[:nn]
    results["График"]["Печь (низ)"] = twnG[:nn]
    results["График"]["Металл (верх)"] = tmvG[:nn]
    results["График"]["Металл (центр)"] = tmcG[:nn]
    results["График"]["Металл (низ)"] = tmnG[:nn]


    # # 🔹 Построение графика
    # plt.figure(figsize=(12, 6))
    # plt.plot(t, twG[:nn], label="Печь (верх)", color="red")
    # plt.plot(t, twnG[:nn], label="Печь (низ)", color="orange")
    # plt.plot(t, tmvG[:nn], label="Металл (верх)", color="green")
    # plt.plot(t, tmcG[:nn], label="Металл (центр)", color="purple")
    # plt.plot(t, tmnG[:nn], label="Металл (низ)", color="blue")

    # # 🔹 Настройки осей
    # plt.xlabel("Время нагрева (мин)", fontsize=12)
    # plt.ylabel("Температура (°C)", fontsize=12)
    # plt.title("Температурный режим нагрева", fontsize=14)
    # plt.legend()
    # plt.grid(True, linestyle="--", alpha=0.5)

    # # 🔹 Подписи осей
    # plt.xticks(np.arange(0, time_H / 60, 10))  # Шаг 10 минут
    # plt.yticks(np.arange(0, 1500, 100))  # Шаг 100 градусов

    # # 🔹 Отображение графика
    # plt.show()

    #print(results)

    return results

def Balance():
    pass