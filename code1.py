import json

# список ошибок (временные промежутки аномалий на сервере)
ErrorList = ['Time codes of anomaly: ']

#список названий типов сервера (как в original .json)
device = {'sev':'Сервер СЕВ', 'dbrobo':'Сервер dbrobo', 'webrobo':'Сервер webrobo', 'dokuwiki':'Сервер dokuwiki'}

# текущее состояние для вывода осредненных значений
TotalState = {'SWAP_Used':0, 'SWAP_Total':0, 'RAM_Used':0, 'RAM_Total':0,
              'Processes_Total':0, 'Processes_Stopped':0, 'Processes_Sleeping':0, 'Processes_Running':0, 'Processes_Zombie':0,
              'system_LA1':0, 'system_LA5':0, 'system_LA15':0, 'system_IDLE':0,
              'HDD_xvda1_Used':0, 'HDD_xvda1_Total':0,
              'HDD_vg-root_Used':0, 'HDD_vg-root_Total':0}

# метод добавления ошибок с соответствующим сообщением
def _addError(s_hour, s_min, str_Err):
    if (s_min >= 25 and s_min <= 30):
        ErrorList.append(str(s_hour) + ':00 - ' + str(s_hour) + ':30 : ' + str_Err)
    elif (s_min >= 55 and s_min <= 59):
        ErrorList.append(str(s_hour) + ':30 - ' + str(s_hour + 1) + ':00 : ' + str_Err)
    return

# вся обработка по открытии файла (.json)
with open ("/Users/Gleb/Desktop/Python/fall.json") as json_string:
    data = json.load(json_string)

    i5 = 0  # записи во время, где число минут кратно 5
    ir = 0  # все остальные записи с рандомным временем
    last_min = 0
    twice_5 = False     # проверка на избыточные граничные записи
    twice = False       # проверка на дублирование записей в целом
    extra = False       # флаг допуска к условию пересчета и печати
    skip = False        # флаг обхода дополнительной проверки
    GO_IN = False       # флаг последнего вхождения для печати оставшейся информации
    am_pm = False
    for key in data:
        # chek selected device (ИМЕННО НА ВЫБРАННЫЙ ДЕВАЙС)
        uName = data[str(key)]['uName']
        key_copy = int(key) + 1

        # проверка наличия след. записи (конец файла .json)
        try:
            data[str(key_copy)]['uName']
        except:
            # флаги всех обходов для последнего вхождения и печати
            GO_IN = True
            twice_5 = False
            extra = True
            skip = True

        # определение записей необходимого девайса
        if (uName == device['dbrobo'] and data[str(key)]['serial'] == '01') or GO_IN:
            # время записи (не для последнего вхождения)
            if not GO_IN:
                hour = int(data[str(key)]['Date'][11] + data[str(key)]['Date'][12])
                min = int(data[str(key)]['Date'][14] + data[str(key)]['Date'][15])

            # срочная печать данных за интервал, который уже прошел
            if (min >= 30 and am_pm == False) or (min <= 30 and am_pm == True):
                am_pm = not am_pm
                extra = True
                skip = True

            # дублирование записей в промежутке времени
            twice = not last_min == min
            last_min = min

            # повторное вхождение
            if twice_5 and ((min >= 25 and min < 30) or (min >= 55 and min <= 59)):
                extra = True
                # ... дополнение к повтору записей (перехватить лишние записи на границе)
                skip = False
            elif twice_5:
                # дублирование на границе завершено (пора печатать значения)
                twice_5 = False
                extra = True
                skip = True

            # подсчет только "правильных" записей
            if (not GO_IN):
                if (min % 5 == 0):
                    i5 += 1
                else:
                    ir += 1

            if (not skip):
                print(data[str(key)]['Date'])

            if not extra:
                # Место обработки json (сложение для осреднения)
                TotalState['SWAP_Used'] += int(data[str(key)]['data']['system_SWAP_Used'])
                TotalState['SWAP_Total'] += int(data[str(key)]['data']['system_SWAP_Total'])

                TotalState['RAM_Used'] += int(data[str(key)]['data']['system_RAM_Used'])
                TotalState['RAM_Total'] += int(data[str(key)]['data']['system_RAM_Total'])

                try:
                    TotalState['Processes_Total'] += int(data[str(key)]['data']['system_Processes_Total'])
                    TotalState['Processes_Stopped'] += int(data[str(key)]['data']['system_Processes_Stopped'])
                    TotalState['Processes_Sleeping'] += int(data[str(key)]['data']['system_Processes_Sleeping'])
                    TotalState['Processes_Running'] += int(data[str(key)]['data']['system_Processes_Running'])
                    TotalState['Processes_Zombie'] += int(data[str(key)]['data']['system_Processes_Zombie'])
                except:
                    TotalState['Processes_Total'] += 0
                    TotalState['Processes_Stopped'] += 0
                    TotalState['Processes_Sleeping'] += 0
                    TotalState['Processes_Running'] += 0
                    TotalState['Processes_Zombie'] += 0

                TotalState['system_LA1'] += float(data[str(key)]['data']['system_LA1'])
                TotalState['system_LA5'] += float(data[str(key)]['data']['system_LA5'])
                TotalState['system_LA15'] += float(data[str(key)]['data']['system_LA15'])

                try:
                    TotalState['system_IDLE'] += float(data[str(key)]['data']['system_IDLE'])
                except:
                    TotalState['system_IDLE'] += 100.0

                TotalState['HDD_xvda1_Used'] += int(data[str(key)]['data']['system_HDD_xvda1_Used'])
                TotalState['HDD_xvda1_Total'] += int(data[str(key)]['data']['system_HDD_xvda1_Total'])

                # только для webrobo (дополнительные поля root)
                if (uName == device['webrobo']):
                    TotalState['HDD_vg-root_Used'] += int(data[str(key)]['data']['system_HDD_vg-root_Used'])
                    TotalState['HDD_vg-root_Total'] += int(data[str(key)]['data']['system_HDD_vg-root_Total'])

            #---------------------------------------------------------------------
            if ((min == 25) or (min == 55)) or extra:  # вывод среднего за 30 минут
                extra = False
                twice_5 = True

                # flag
                if (not skip):
                    continue
                skip = False

                twice_5 = False
                if not GO_IN:
                    if (i5 == 6) and (ir == 0):
                        strErr = "Все в порядке."
                    elif (i5 + ir == 6):
                        strErr = "Ненормальная работа: остановка или сбои в работе. Записи в нужном числе."
                        _addError(hour, min, strErr)
                    elif (i5 + ir < 6 and i5 + ir > 0):
                        strErr = "Остановка работы на продолжительное время. Записи частично утеряны."
                        _addError(hour, min, strErr)
                    elif i5 + ir == 0:
                        strErr = "Сервер не работал."
                        _addError(hour, min, strErr)

                    if twice:
                        _addError(hour, min, 'Дублирование записей.')
                    elif (i5 + ir > 6):
                        strErr = "Присутствуют лишние записи: возможно, сервер был перезагружен."
                        _addError(hour, min, strErr)
                    twice = False


                # осреднение за 30 минут
                for key in TotalState.keys():
                    TotalState[key] /= (i5 + ir)

                i5 = 0
                ir = 0

                # ----------------------------------------------------------------
                print('SWAP Used: ' + str(TotalState['SWAP_Used']))
                print('SWAP Total: ' + str(TotalState['SWAP_Total']))

                print('RAM Used: ' + str(TotalState['RAM_Used']))
                print('RAM Total: ' + str(TotalState['RAM_Total']))

                print('Proc. Total: ' + str(TotalState['Processes_Total']))
                print('Proc. Stopped: ' + str(TotalState['Processes_Stopped']))
                print('Proc. Sleeping: ' + str(TotalState['Processes_Sleeping']))
                print('Proc. Running: ' + str(TotalState['Processes_Running']))
                print('Proc. Zombie: ' + str(TotalState['Processes_Zombie']))

                print('LA1: ' + str(TotalState['system_LA1']))
                print('LA5: ' + str(TotalState['system_LA5']))
                print('LA15: ' + str(TotalState['system_LA15']))
                print('IDLE: ' + str(TotalState['system_IDLE']))

                print('HDD (xvda1) Used: ' + str(TotalState['HDD_xvda1_Used']))

                # если есть дополнительные поля
                if (uName == device['webrobo']):
                    print('HDD (xvda1) Total: ' + str(TotalState['HDD_xvda1_Total']))
                    print('HDD (root) Used: ' + str(TotalState['HDD_vg-root_Used']))
                    print('HDD (root) Total: ' + str(TotalState['HDD_vg-root_Total']) + '\n')
                else:
                    print('HDD (xvda1) Total: ' + str(TotalState['HDD_xvda1_Total']) + '\n')

                # занулить после вывода
                for strr in TotalState.keys():
                    TotalState[strr] = 0

        GO_IN = False

    # оформление и вывод списка ошибок
    if (len(ErrorList) > 1):
        ErrorList.append('Конец списка ошибок.')
    else:
        ErrorList.append('Ошибок в работе не выявлено.')

    for list in ErrorList:
        print(list)
