
import json

TotalState = {'SWAP_Used':0, 'SWAP_Total':0, 'RAM_Used':0, 'RAM_Total':0,
              'Processes_Total':0, 'Processes_Stopped':0, 'Processes_Sleeping':0, 'Processes_Running':0, 'Processes_Zombie':0,
              'system_LA1':0, 'system_LA5':0, 'system_LA15':0, 'system_IDLE':0,
              'HDD_xvda1_Used':0, 'HDD_xvda1_Total':0,
              'HDD_vg-root_Used':0, 'HDD_vg-root_Total':0}


with open ("/Users/Gleb/Desktop/log.json") as json_string:
    data = json.load(json_string)

    i = 0
    for key in data:
        if (data[str(key)]['uName'] == 'РЎРµСЂРІРµСЂ РЎР•Р’') and (data[str(key)]['serial'] == '01'): # Сервер CEB 01
            # Место обработки json
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
            TotalState['system_IDLE'] += float(data[str(key)]['data']['system_IDLE'])

            TotalState['HDD_xvda1_Used'] += int(data[str(key)]['data']['system_HDD_xvda1_Used'])
            TotalState['HDD_xvda1_Total'] += int(data[str(key)]['data']['system_HDD_xvda1_Total'])

            i += 1

            # check (проверка на диапазон времени + учесть расхождение в 1 минуту)
            #  - метод перевода времени (с разбиением на часы-минуты)
            #  - при отсутсвии записи - заглушка

            if (i == 6):
                i = 0

                #for key in TotalState.keys():
                #    TotalState[key] /= 6

                TotalState['SWAP_Used'] /= 6
                TotalState['SWAP_Total'] /= 6

                TotalState['RAM_Used'] /= 6
                TotalState['RAM_Total'] /= 6

                TotalState['Processes_Total'] /= 6
                TotalState['Processes_Stopped'] /= 6
                TotalState['Processes_Sleeping'] /= 6
                TotalState['Processes_Running'] /= 6
                TotalState['Processes_Zombie'] /= 6

                TotalState['system_LA1'] /= 6
                TotalState['system_LA5'] /= 6
                TotalState['system_LA15'] /= 6
                TotalState['system_IDLE'] /= 6

                TotalState['HDD_xvda1_Used'] /= 6
                TotalState['HDD_xvda1_Total'] /= 6

                # ----------------------------------------------------------------

                print('SWAP Used: ' + TotalState['SWAP_Used'])
                print('SWAP Total: ' + TotalState['SWAP_Total'])

                print('RAM Used: ' + TotalState['RAM_Used'])
                print('RAM Total: ' + TotalState['RAM_Total'])

                print('Proc. Total: ' + TotalState['Processes_Total'])
                print('Proc. Stopped: ' + TotalState['Processes_Stopped'])
                print('Proc. Sleeping: ' + TotalState['Processes_Sleeping'])
                print('Proc. Running: ' + TotalState['Processes_Running'])
                print('Proc. Zombie: ' + TotalState['Processes_Zombie'])

                print('LA1: ' + TotalState['system_LA1'])
                print('LA5: ' + TotalState['system_LA5'])
                print('LA15: ' + TotalState['system_LA15'])
                print('IDLE: ' + TotalState['system_IDLE'])

                print('HDD (xvda1) Used: ' + TotalState['HDD_xvda1_Used'])
                print('HDD (xvda1) Total: ' + TotalState['HDD_xvda1_Total'] + '\n')

                    # занулить после вывода
                for str in TotalState.keys():
                    TotalState[str] = 0



            #print(data[str(key)]['data']['system_HDD_vg-root_Used'])
            #print(data[str(key)]['data']['system_HDD_vg-root_Total'] + '\n')

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
