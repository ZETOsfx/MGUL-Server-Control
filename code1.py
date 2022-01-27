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

def _addError(s_hour, s_min, str_Err):
    if (s_min == 25):
        ErrorList.append(str(s_hour) + ':00 - ' + str(s_hour) + ':30 : ' + str_Err)
    elif (s_min == 55):
        ErrorList.append(str(s_hour) + ':30 - ' + str(s_hour + 1) + ':00 : ' + str_Err)
    return

with open ("/Users/Gleb/Desktop/Python/log.json") as json_string:
    data = json.load(json_string)

    i5 = 0  # записи во время, где число минут кратно 5
    ir = 0  # все остальные записи с рандомным временем
    for key in data:
        # chek selected device (ИМЕННО НА ВЫБРАННЫЙ ДЕВАЙС)
        uName = data[str(key)]['uName']
        if (uName == device['webrobo']) and (data[str(key)]['serial'] == '01'):

            # Место обработки json (сложение для осреднения)
            print(data[str(key)]['Date'])

            TotalState['SWAP_Used'] += int(data[str(key)]['data']['system_SWAP_Used'])
            TotalState['SWAP_Total'] += int(data[str(key)]['data']['system_SWAP_Total'])

            TotalState['RAM_Used'] += int(data[str(key)]['data']['system_RAM_Used'])
            TotalState['RAM_Total'] += int(data[str(key)]['data']['system_RAM_Total'])

            TotalState['Processes_Total'] += int(data[str(key)]['data']['system_Processes_Total'])
            TotalState['Processes_Stopped'] += int(data[str(key)]['data']['system_Processes_Stopped'])
            TotalState['Processes_Sleeping'] += int(data[str(key)]['data']['system_Processes_Sleeping'])
            TotalState['Processes_Running'] += int(data[str(key)]['data']['system_Processes_Running'])
            TotalState['Processes_Zombie'] += int(data[str(key)]['data']['system_Processes_Zombie'])

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

            # check (проверка на диапазон времени)
            #  - метод перевода времени (с разбиением на часы-минуты)
            #  - при отсутсвии записи - заглушка


            hour = int(data[str(key)]['Date'][11] + data[str(key)]['Date'][12])
            min = int(data[str(key)]['Date'][14] + data[str(key)]['Date'][15])

            # подсчет только "правильных записей"
            if (min % 5 == 0):
                i5 += 1
            else:
                ir += 1
            #---------------------------------------------------------------------
            if (min == 25) or (min == 55):  # вывод среднего за 30 минут

                if (i5 == 6) and (ir == 0):
                    strErr = "Все в порядке."
                elif (i5 + ir == 6):
                    strErr = "Ненормальная работа: остановка или сбои в работе. Записи в нужном числе."
                    _addError(hour, min, strErr)
                elif (i5 + ir > 6):
                    strErr = "Присутствуют лишние записи: возможно, сервер был перезагружен."
                    _addError(hour, min, strErr)
                elif (i5 + i6 < 6):
                    strErr = "Остановка работы на продолжительное время. Записи частично утеряны."
                    _addError(hour, min, strErr)

                print(strErr)

                i5 = 0
                ir = 0

                # осреднение за 30 минут
                for key in TotalState.keys():
                    TotalState[key] /= 6

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

    # оформление и вывод списка ошибок
    if (len(ErrorList) > 1):
        ErrorList.append('Конец списка ошибок.')
    else:
        ErrorList.append('Ошибок в работе не выявлено.')

    for list in ErrorList:
        print(list)
