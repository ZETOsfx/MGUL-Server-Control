import json

#список названий типов сервера (как в original .json)
device = {'sev':'Сервер СЕВ', 'dbrobo':'РЎРµСЂРІРµСЂ dbrobo', 'webrobo':'Сервер webrobo', 'dokuwiki':'Сервер dokuwiki'}

# текущее состояние для вывода осредненных значений
TotalState = {'SWAP_Used':0, 'SWAP_Total':0, 'RAM_Used':0, 'RAM_Total':0,
              'Processes_Total':0, 'Processes_Stopped':0, 'Processes_Sleeping':0, 'Processes_Running':0, 'Processes_Zombie':0,
              'system_LA1':0, 'system_LA5':0, 'system_LA15':0, 'system_IDLE':0,
              'HDD_xvda1_Used':0, 'HDD_xvda1_Total':0,
              'HDD_vg-root_Used':0, 'HDD_vg-root_Total':0}


with open ("/Users/Gleb/Desktop/Python/log.json") as json_string:
    data = json.load(json_string)

    i = 0
    for key in data:
        # chek selected device (ИМЕННО НА ВЫБРАННЫЙ ДЕВАЙС)
        uName = data[str(key)]['uName']
        if (uName == 'Сервер webrobo') and (data[str(key)]['serial'] == '01'):

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
            if (uName == 'Сервер webrobo'):
                TotalState['HDD_vg-root_Used'] += int(data[str(key)]['data']['system_HDD_vg-root_Used'])
                TotalState['HDD_vg-root_Total'] += int(data[str(key)]['data']['system_HDD_vg-root_Total'])

            i += 1

            # check (проверка на диапазон времени + учесть расхождение в 1 минуту)
            #  - метод перевода времени (с разбиением на часы-минуты)
            #  - при отсутсвии записи - заглушка

            if (i == 6):
                i = 0

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
                if (uName == 'Сервер webrobo'):
                    print('HDD (xvda1) Total: ' + str(TotalState['HDD_xvda1_Total']))
                    print('HDD (root) Used: ' + str(TotalState['HDD_vg-root_Used']))
                    print('HDD (root) Total: ' + str(TotalState['HDD_vg-root_Total']) + '\n')
                else:
                    print('HDD (xvda1) Total: ' + str(TotalState['HDD_xvda1_Total']) + '\n')

                # занулить после вывода
                for strr in TotalState.keys():
                    TotalState[strr] = 0


            """
            # Место обработки json
            print(data[str(f_key)]['Date'])
            print('SWAP Used: ' + data[str(f_key)]['data']['system_SWAP_Used'])
            print('SWAP Total: ' + data[str(f_key)]['data']['system_SWAP_Total'])

            print('RAM Used: ' + data[str(f_key)]['data']['system_RAM_Used'])
            print('RAM Total: ' + data[str(f_key)]['data']['system_RAM_Total'])

            print('Proc. Total: ' + data[str(f_key)]['data']['system_Processes_Total'])
            print('Proc. Stopped: ' + data[str(f_key)]['data']['system_Processes_Stopped'])
            print('Proc. Sleeping: ' + data[str(f_key)]['data']['system_Processes_Sleeping'])
            print('Proc. Running: ' + data[str(f_key)]['data']['system_Processes_Running'])
            print('Proc. Zombie: ' + data[str(f_key)]['data']['system_Processes_Zombie'])

            print('LA1: ' + data[str(f_key)]['data']['system_LA1'])
            print('LA5: ' + data[str(f_key)]['data']['system_LA5'])
            print('LA15: ' + data[str(f_key)]['data']['system_LA15'])
            print('IDLE: ' + data[str(f_key)]['data']['system_IDLE'])

            print('HDD (xvda1) Used: ' + data[str(f_key)]['data']['system_HDD_xvda1_Used'])
            print('HDD (xvda1) Total: ' + data[str(f_key)]['data']['system_HDD_xvda1_Total'] + '\n')
                """
