#!/usr/bin/env python3

from lib import rpclib, tuilib
import os
import time

oracles = {}
oracles['name'] = 'Oracles'
oracles['header'] = "\
                 _                       ____                 _               __  __           _       _       \n\
     /\         | |                     / __ \               | |             |  \/  |         | |     | |      \n\
    /  \   _ __ | |_ __ _ _ __ __ _    | |  | |_ __ __ _  ___| | ___  ___    | \  / | ___   __| |_   _| | ___  \n\
   / /\ \ | '_ \| __/ _` | '__/ _` |   | |  | | '__/ _` |/ __| |/ _ \/ __|   | |\/| |/ _ \ / _` | | | | |/ _ \ \n\
  / ____ \| | | | || (_| | | | (_| |   | |__| | | | (_| | (__| |  __/\__ \   | |  | | (_) | (_| | |_| | |  __/ \n\
 /_/    \_\_| |_|\__\__,_|_|  \__,_|    \____/|_|  \__,_|\___|_|\___||___/   |_|  |_|\___/ \__,_|\__,_|_|\___| \n"
                                                                                                              
oracles['menu'] = [
    # TODO: Have to implement here native oracle file uploader / reader, should be dope
    # TODO: data publisher / converter for different types
    {"Check mempool": tuilib.print_mempool},
    {"View oracle info": tuilib.oracles_info},
    {"Create oracle": tuilib.oracle_create_tui},
    {"Register as publisher for oracle": tuilib.oracle_register_tui},
    {"Subscribe on oracle (+UTXO generator)": tuilib.oracle_subscription_utxogen},
    {"Upload file to oracle": tuilib.convert_file_oracle_D},
    {"Display list of files uploaded to this AC": tuilib.display_files_list},
    {"Download files from oracle": tuilib.files_downloader},
    {"Migrate oracles and data from one chain to another": tuilib.migrate_oracles}
]
oracles['author'] = 'Welcome to the OraclesCC TUI!\nCLI version 0.2 by Anton Lysakov & Thorn Mennet\n'

pegs_usage = {}
pegs_usage['name'] = 'Pegs usage'
pegs_usage['header'] = "\
                 _                      _____                   __  __           _       _      \n\
     /\         | |                    |  __ \                 |  \/  |         | |     | |     \n\
    /  \   _ __ | |_ __ _ _ __ __ _    | |__) |__  __ _ ___    | \  / | ___   __| |_   _| | ___ \n\
   / /\ \ | '_ \| __/ _` | '__/ _` |   |  ___/ _ \/ _` / __|   | |\/| |/ _ \ / _` | | | | |/ _ \ \n\
  / ____ \| | | | || (_| | | | (_| |   | |  |  __/ (_| \__ \   | |  | | (_) | (_| | |_| | |  __/ \n\
 /_/    \_\_| |_|\__\__,_|_|  \__,_|   |_|   \___|\__, |___/   |_|  |_|\___/ \__,_|\__,_|_|\___| \n\
                                                   __/ |                                        \n\
                                                  |___/                                         \n"

pegs_usage['menu'] = [
    {"Pegs Module Readme": tuilib.readme_tui},
    {"Check assetchain mempool": tuilib.print_mempool},
    {"View assetchain Gateway Info": tuilib.gateway_info_tui},
    {"Deposit KMD in Gateway and claim Tokens": tuilib.gateways_deposit_claim_tokens},
    {"Execute Pegs funding": tuilib.pegs_fund_tui},
    {"Execute Pegs get": tuilib.pegs_get_tui},
    {"Check Pegs info": tuilib.pegsinfo_tui},
    {"Check Pegs account history": tuilib.pegs_accounthistory_tui},
    {"Check Pegs account info": tuilib.pegs_accountinfo_tui},
    {"Check Pegs addresses": tuilib.pegs_addresses_tui},
    {"Check Pegs worst accounts": tuilib.pegs_worstaccounts_tui}
]
pegs_usage['author'] = 'Welcome to the Pegs Usage TUI!\nCLI version 0.2 by Thorn Mennet\n'

pegs_create = {}
pegs_create['name'] = 'Pegs create'
pegs_create['header'] = "\
                 _                      _____                   __  __           _       _      \n\
     /\         | |                    |  __ \                 |  \/  |         | |     | |     \n\
    /  \   _ __ | |_ __ _ _ __ __ _    | |__) |__  __ _ ___    | \  / | ___   __| |_   _| | ___ \n\
   / /\ \ | '_ \| __/ _` | '__/ _` |   |  ___/ _ \/ _` / __|   | |\/| |/ _ \ / _` | | | | |/ _ \ \n\
  / ____ \| | | | || (_| | | | (_| |   | |  |  __/ (_| \__ \   | |  | | (_) | (_| | |_| | |  __/ \n\
 /_/    \_\_| |_|\__\__,_|_|  \__,_|   |_|   \___|\__, |___/   |_|  |_|\___/ \__,_|\__,_|_|\___| \n\
                                                   __/ |                                        \n\
                                                  |___/                                         \n"

pegs_create['menu'] = [
    {"Pegs Module Readme": tuilib.readme_tui},
    {"Create a Pegs assetchain": tuilib.pegs_create_tui},
    {"Run oraclefeed": tuilib.oraclefeed_tui}
]
pegs_create['author'] = 'Welcome to the Pegs Creation TUI!\nCLI version 0.2 by Thorn Mennet\n'



gw_create = {}
gw_create['name'] = 'GW create'
gw_create['header'] = "\
                  _                       _____       _                                   __  __           _       _      \n\
      /\         | |                     / ____|     | |                                 |  \/  |         | |     | |      \n \
    /  \   _ __ | |_ __ _ _ __ __ _    | |  __  __ _| |_ _____      ____ _ _   _ ___    | \  / | ___   __| |_   _| | ___  \n \
   / /\ \ | '_ \| __/ _` | '__/ _` |   | | |_ |/ _` | __/ _ \ \ /\ / / _` | | | / __|   | |\/| |/ _ \ / _` | | | | |/ _ \ \n \
  / ____ \| | | | || (_| | | | (_| |   | |__| | (_| | ||  __/\ V  V / (_| | |_| \__ \   | |  | | (_) | (_| | |_| | |  __/ \n \
 /_/    \_\_| |_|\__\__,_|_|  \__,_|    \_____|\__,_|\__\___| \_/\_/ \__,_|\__, |___/   |_|  |_|\___/ \__,_|\__,_|_|\___| \n \
                                                                            __/ |                                        \n \
                                                                           |___/                                         \n "


gw_create['menu'] = [
    {"Check mempool": tuilib.print_mempool},
    {"Create token": tuilib.token_create_tui},
    {"Create oracle": tuilib.oracle_create_tui},
    {"Register as publisher for oracle": tuilib.oracle_register_tui},
    {"Subscribe on oracle (+UTXO generator)": tuilib.oracle_subscription_utxogen},
    {"Bind Gateway": tuilib.gateways_bind_tui},
]
gw_create['author'] = 'Welcome to the Gateways Creation TUI!\nCLI version 0.2 by Anton Lysakov & Thorn Mennet\n'


gw_use = {}
gw_use['name'] = 'GW usage'
gw_use['header'] = "\
                  _                       _____       _                                   __  __           _       _      \n\
      /\         | |                     / ____|     | |                                 |  \/  |         | |     | |      \n \
    /  \   _ __ | |_ __ _ _ __ __ _    | |  __  __ _| |_ _____      ____ _ _   _ ___    | \  / | ___   __| |_   _| | ___  \n \
   / /\ \ | '_ \| __/ _` | '__/ _` |   | | |_ |/ _` | __/ _ \ \ /\ / / _` | | | / __|   | |\/| |/ _ \ / _` | | | | |/ _ \ \n \
  / ____ \| | | | || (_| | | | (_| |   | |__| | (_| | ||  __/\ V  V / (_| | |_| \__ \   | |  | | (_) | (_| | |_| | |  __/ \n \
 /_/    \_\_| |_|\__\__,_|_|  \__,_|    \_____|\__,_|\__\___| \_/\_/ \__,_|\__, |___/   |_|  |_|\___/ \__,_|\__,_|_|\___| \n \
                                                                            __/ |                                        \n \
                                                                           |___/                                         \n "

gw_use['menu'] = [
    {"Check assetchain mempool": tuilib.print_mempool},
    {"View assetchain Gateway Info": tuilib.gateway_info_tui},
    {"Send KMD gateway deposit transaction": tuilib.gateways_send_kmd},
    {"Execute gateways deposit": tuilib.gateways_deposit_tui},
    {"Execute gateways claim": tuilib.gateways_claim_tui},
    {"Execute gateways withdrawal": tuilib.gateways_withdrawal_tui}
]
gw_use['author'] = 'Welcome to the Gateways Usage TUI!\nCLI version 0.2 by Anton Lysakov & Thorn Mennet\n'

payments = {}
payments['name'] = 'Payments'
payments['header'] = "\
                 _                      _____                                 _           __  __           _       _      \n\
     /\         | |                    |  __ \                               | |         |  \/  |         | |     | |     \n\
    /  \   _ __ | |_ __ _ _ __ __ _    | |__) |_ _ _   _ _ __ ___   ___ _ __ | |_ ___    | \  / | ___   __| |_   _| | ___  \n\
   / /\ \ | '_ \| __/ _` | '__/ _` |   |  ___/ _` | | | | '_ ` _ \ / _ \ '_ \| __/ __|   | |\/| |/ _ \ / _` | | | | |/ _ \ \n\
  / ____ \| | | | || (_| | | | (_| |   | |  | (_| | |_| | | | | | |  __/ | | | |_\__ \   | |  | | (_) | (_| | |_| | |  __/ \n\
 /_/    \_\_| |_|\__\__,_|_|  \__,_|   |_|   \__,_|\__, |_| |_| |_|\___|_| |_|\__|___/   |_|  |_|\___/ \__,_|\__,_|_|\___| \n\
                                                    __/ |                                                                 \n\
                                                   |___/                                                                  \n"

payments['menu'] = [
    {"Check mempool": tuilib.print_mempool},
    {"View Payments contracts": tuilib.payments_info},
    {"Create Payments contract": tuilib.payments_create},
    {"Fund Payments contract": tuilib.payments_fund},
    {"Merge Payments contract funds": tuilib.payments_merge},
    {"Release Payments contract funds": tuilib.payments_release}
]
payments['author'] = 'Welcome to the Payments Module TUI!\nCLI version 0.2 by Thorn Mennet\n'

antara = {}
antara['name'] = 'Antara'
antara['header'] = "\
                 _                       _____                      _       _           _           __  __           _       _           \n\
     /\         | |                     / ____|                    | |     | |         (_)         |  \/  |         | |     | |          \n\
    /  \   _ __ | |_ __ _ _ __ __ _    | (___  _ __ ___   __ _ _ __| |_ ___| |__   __ _ _ _ __     | \  / | ___   __| |_   _| | ___  ___ \n\
   / /\ \ | '_ \| __/ _` | '__/ _` |    \___ \| '_ ` _ \ / _` | '__| __/ __| '_ \ / _` | | '_ \    | |\/| |/ _ \ / _` | | | | |/ _ \/ __| \n\
  / ____ \| | | | || (_| | | | (_| |    ____) | | | | | | (_| | |  | || (__| | | | (_| | | | | |   | |  | | (_) | (_| | |_| | |  __/\__ \ \n\
 /_/    \_\_| |_|\__\__,_|_|  \__,_|   |_____/|_| |_| |_|\__,_|_|   \__\___|_| |_|\__,_|_|_| |_|   |_|  |_|\___/ \__,_|\__,_|_|\___||___/ \n"

antara['menu'] = [
    {"Oracles": oracles},
    {"Gateways Creation": gw_create},
    {"Gateways Usage": gw_use},
    {"Pegs Creation": pegs_create},
    {"Pegs Usage": pegs_usage},
    {"Payments": payments},
]
antara['author'] = "Welcome to the Antara Modules TUI!\nCLI version 0.2 by Anton Lysakov & Thorn Mennet\n"

common_submenu_options = [
    {"Return to Antara modules menu": tuilib.exit_main},
    {"Exit TUI": tuilib.exit}
]

def get_rpc_status(menu, rpc_connection='', rpc_connection_kmd=''):
    add_to_menu = []
    if menu['name'] not in ['Pegs create']:
        try: 
            ac_name = rpc_connection.getinfo()['name']
            ac_rpc_status = tuilib.colorize("[Connected to "+ac_name+"]", 'green')
            add_to_menu.append({"Check connection to Smartchain": tuilib.getinfo_tui})
        except:
            ac_rpc_status = tuilib.colorize("[Not connected to Smartchain]", 'red')
            add_to_menu.append({"Connect to Smartchain": tuilib.rpc_connection_tui})
            pass 
    if menu['name'] not in ['Payments', 'Oracles']:
        try:
            ac_name = rpc_connection_kmd.getinfo()['name']
            kmd_rpc_status = tuilib.colorize("[Connected to KMD]", 'green')
            add_to_menu.append({"Check connection to KMD": tuilib.getinfo_tui})
        except Exception as e:
            kmd_rpc_status = tuilib.colorize("[Not connected to KMD]", 'red')
            add_to_menu.append({"Connect to KMD daemon": tuilib.kmd_rpc_connection_tui})
            pass
    if menu['name'] in ['Payments', 'Oracles']:
        status_str = ac_rpc_status
    elif menu['name'] in ['Pegs create']:
        status_str = kmd_rpc_status
    else:
        status_str = kmd_rpc_status+"   "+ac_rpc_status
    if status_str.find('Not') > 0:
        menuItems = add_to_menu+common_submenu_options
    else:
        menuItems = add_to_menu+menu['menu']+common_submenu_options
    return status_str, menuItems, rpc_connection_kmd, rpc_connection


main_menu_options = ["Oracles", "Gateways Creation", "Gateways Usage", "Pegs Creation", "Pegs Usage", "Payments"]
rpc_connect_options = ["Connect to KMD daemon", "Connect to Smartchain"]
ac_rpc_options = ["Check connection to Smartchain"]
kmd_rpc_options = ["Check connection to KMD", "Send KMD gateway deposit transaction"]
kmd_ac_rpc_options = ["Deposit KMD in Gateway and claim Tokens", "Execute gateways deposit"]
no_param_options = ["Exit TUI", "Create a Pegs assetchain",
                    "Migrate oracles and data from one chain to another", "Return to Antara modules menu"]
# TODO: add more readme docs
docs_options = ["Pegs Module Readme"]
readme_files = ['docs/pegs_module.md']
def submenu(menu, rpc_connection='', rpc_connection_kmd=''):
    while True:
        os.system('clear')
        print(tuilib.colorize(menu['header'], 'blue'))
        print(tuilib.colorize(menu['author'], 'green'))
        rpc_status = get_rpc_status(menu, rpc_connection, rpc_connection_kmd)
        print(rpc_status[0])
        menuItems = rpc_status[1]
        for item in menuItems:
            print(tuilib.colorize("[" + str(menuItems.index(item)) + "] ", 'blue') + list(item.keys())[0])
        choice = input(">> ")
        try:
            if int(choice) < 0:
                raise ValueError
            if list(menuItems[int(choice)].keys())[0] == "Return to Antara modules menu":
                submenu(antara,rpc_connection, rpc_connection_kmd)
            elif list(menuItems[int(choice)].keys())[0] in main_menu_options:
                submenu(list(menuItems[int(choice)].values())[0],rpc_connection, rpc_connection_kmd)
            elif list(menuItems[int(choice)].keys())[0] in no_param_options:
                list(menuItems[int(choice)].values())[0]()
            elif list(menuItems[int(choice)].keys())[0] in docs_options:
                index = docs_options.index(list(menuItems[int(choice)].keys())[0])
                list(menuItems[int(choice)].values())[0](readme_files[index])
            elif list(menuItems[int(choice)].keys())[0] == "Connect to KMD daemon":
                rpc_connection_kmd = list(menuItems[int(choice)].values())[0]()
            elif list(menuItems[int(choice)].keys())[0] == "Connect to Smartchain":
                rpc_connection = list(menuItems[int(choice)].values())[0]()                
            elif list(menuItems[int(choice)].keys())[0] in kmd_rpc_options:
                while True:
                    try:
                        #print(list(menuItems[int(choice)].values())[0])
                        #print(rpc_connection_kmd)
                        list(menuItems[int(choice)].values())[0](rpc_connection_kmd)
                        break
                    except Exception as e:
                        print("Something went wrong with "+str(list(menuItems[int(choice)].values())[0]))
                        input(e)
                        input("Press [Enter] to continue...")
                        break
            elif list(menuItems[int(choice)].keys())[0] in kmd_ac_rpc_options:
                while True:
                    try:
                        list(menuItems[int(choice)].values())[0](rpc_connection, rpc_connection_kmd)
                        break
                    except Exception as e:
                        print("Something went wrong with "+str(list(menuItems[int(choice)].values())[0]))
                        print(e)
                        input("Press [Enter] to continue...")
                        break
            else:
                list(menuItems[int(choice)].values())[0](rpc_connection)
        except (ValueError, IndexError):
            pass

def main():
    menuItems = antara['menu']
    while True:
        os.system('clear')
        print(tuilib.colorize(antara['header'], 'blue'))
        print(tuilib.colorize(antara['author'], 'green'))
        for item in menuItems:
            print(tuilib.colorize("[" + str(menuItems.index(item)) + "] ", 'blue') + list(item.keys())[0])
        choice = input(">> ")
        try:
            if int(choice) < 0:
                raise ValueError
            # Call the matching function
            if list(menuItems[int(choice)].keys())[0] == "Exit TUI":
                list(menuItems[int(choice)].values())[0]()
            else:
                submenu(list(menuItems[int(choice)].values())[0])
        except (ValueError, IndexError):
            pass


if __name__ == "__main__":
    while True:
        with (open("lib/logo.txt", "r")) as logo:
            for line in logo:
                parts = line.split(' ')
                row = ''
                for part in parts:
                    if part.find('.') == -1:
                        row += tuilib.colorize(part, 'blue')
                    else:
                        row += tuilib.colorize(part, 'black')
                print(row, end='')
                #print(line, end='')
                time.sleep(0.04)
            time.sleep(0.4)
        print("\n")
        break
    main()


