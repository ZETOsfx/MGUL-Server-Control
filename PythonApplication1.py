
import json

TotalState = {'SWAP_Used':0, 'SWAP_Total':0, 'RAM_Used':0, 'RAM_Total':0, 
              'Processes_Total':0, 'Processes_Stopped':0, 'Processes_Sleeping':0, 'Processes_Running':0, 'Processes_Zombie':0,
              'system_LA1':0, 'system_LA5':0, 'system_LA15':0, 'system_IDLE':0,
              'HDD_xvda1_Used':0, 'HDD_xvda1_Total':0,
              'HDD_vg-root_Used':0, 'HDD_vg-root_Total':0}


with open ("C:/Users/sasha/Downloads/log.json") as json_string:
    data = json.load(json_string)

    i = 0
    for key in data:
        if (data[str(key)]['uName'] == 'РЎРµСЂРІРµСЂ РЎР•Р’') and (data[str(key)]['serial'] == '01'): # Сервер CEB 01
            # Место обработки json
            print(data[str(key)]['Date']) 

            SWAP_Used.append(int(data[str(key)]['data']['system_SWAP_Used']))
            SWAP_Total.append(int(data[str(key)]['data']['system_SWAP_Total']))

            RAM_Used.append(int(data[str(key)]['data']['system_RAM_Used']))
            RAM_Total.append(int(data[str(key)]['data']['system_RAM_Total']))

            Processes_Total.append(int(data[str(key)]['data']['system_Processes_Total']))
            Processes_Stopped.append(int(data[str(key)]['data']['system_Processes_Stopped']))
            Processes_Sleeping.append(int(data[str(key)]['data']['system_Processes_Sleeping']))
            Processes_Running.append(int(data[str(key)]['data']['system_Processes_Running']))
            Processes_Zombie.append(int(data[str(key)]['data']['system_Processes_Zombie']))

            system_LA1.append(float(data[str(key)]['data']['system_LA1']))
            system_LA5.append(float(data[str(key)]['data']['system_LA5']))
            system_LA15.append(float(data[str(key)]['data']['system_LA15']))
            system_IDLE.append(float(data[str(key)]['data']['system_IDLE']))

            HDD_xvda1_Used.append(int(data[str(key)]['data']['system_HDD_xvda1_Used']))
            HDD_xvda1_Total.append(int(data[str(key)]['data']['system_HDD_xvda1_Total']))

            i += 1

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



