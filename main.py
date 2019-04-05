import logging
from pandas import read_csv
import onuscalc
import tl1functions

# START of logging configuration
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s -  %(name)s -  %(funcName)s - %(levelname)s: %(message)s')
file_handler = logging.FileHandler('logs/main_exec.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
# END of logging configuration

# Configuration Variables
olt_ip = '192.168.0.1'
tl1_user = 'user'
tl1_password = 'password'


# Importing files from UNM and ISP Software
serial_username_mac_from_database = read_csv('onus_from_database.csv', sep=';', header=None)
slot_pon_serial_from_unm = read_csv('onus_from_unm2000.csv', sep=';', header=None)

# Variable that contain the serial,model,position,username,vlan of the client
client_attributes = []
# Variable with the total matchs of serials between UNM2000 and ISPSoftware
total_matches = 0
# Position of client in the list
client_number = 0


for serial_database in serial_username_mac_from_database[0]:
    array_control = 0
    for serial_unm in slot_pon_serial_from_unm[2]:
        if str(serial_unm).upper() == str(serial_database).upper():
            client_attributes.append([serial_database, slot_pon_serial_from_unm[0][array_control], slot_pon_serial_from_unm[1][array_control],
                                      serial_username_mac_from_database[1][client_number], slot_pon_serial_from_unm[3][array_control],
                                      serial_username_mac_from_database[2][client_number]])
            total_matches += 1
            array_control = 0
        array_control += 1
    client_number += 1

print("Total clients match UNM/Database: " + str(total_matches))

report = "user;slot;pon;serial;mode\n"
result_file = open('logs/result_log.csv', 'w+')
onus_calc_missing = onuscalc.onus_in_a_not_in_b(serial_username_mac_from_database[0], slot_pon_serial_from_unm[2])
configured_clients_counter = 0
mac_sum = 0
counter = 1
counter_bridge = 0
counter_router = 0
counter_error = 0
errors_ids = []
commands_to_send = [''] * 2
for line in client_attributes:
    print("Start configuration of client: " + str(counter) + " Username: " + line[3])
    commands_to_send[0] = tl1functions.tl1_add_onu_whitelist(olt_ip=olt_ip, slot=line[1], pon=line[2], onu_serial=line[0],
                                                             onu_model=line[4], name=line[3])
    report += str(line[3]) + ";" + str(line[1]) + ";" + str(line[2]) + ";" + str(line[0])
    # Configure as ROUTER if the mac present on RADIUS its Fiberhome
    if onuscalc.check_mac_of_connection(client_attributes[mac_sum][5]) == 1:
        commands_to_send[1] = tl1functions.tl1_pppoe_command(olt_ip=olt_ip, slot=str(line[1]), pon=str(line[2]), onu_serial=str(line[0]),
                                                             pppoe_user=line[3], pppoe_password='online')
        counter_router += 1
        report += ";" + "PPPoE\n"
    # No configure and report as error if the value of the return its 2 ( error ) on mac calculation
    elif onuscalc.check_mac_of_connection(client_attributes[mac_sum][5]) == 2:
        report += ";" + "ERROR\n"
        errors_ids.append(counter)
        counter_error += 1
    # Anything else, configure as router with PPPoE WAN
    else:
        commands_to_send[1] = tl1functions.tl1_bridge_command(olt_ip=olt_ip, slot=str(line[1]), pon=str(line[2]), onu_serial=str(line[0]))
        report += ";" + "Bridge\n"
        counter_bridge += 1
    # SENDS COMMANDS TO UNM200 CAUTION - DO NOT ENABLE - ONLY IF YOU WILL REALLY USE
    # tl1exec.tl1_connect_and_send_commands(olt_ip, tl1_user, tl1_password, commands_to_send)
    for commands in commands_to_send:
        print(commands)
    # Create reports and incrementing variables
    result_file.write(report)
    report = ""
    mac_sum += 1
    counter += 1
    configured_clients_counter += 1


print("Amount of ONUs on Database: " + str(len(set(serial_username_mac_from_database[2]))))
print("Amount of ONUS on UNM2000: " + str(len(set(slot_pon_serial_from_unm[2]))))
print("Amount of ONUs on Database and not present on UNM: " + str(len(onus_calc_missing[0])))
print("Amount of ONUs on UNM and not present on Database: " + str(len(onus_calc_missing[1])))
print("Amount of ONUs configured: " + str(configured_clients_counter))
print("Amount of ONUs configure in bridge mode: " + str(counter_bridge))
print("Amount of ONUs configure in router mode: " + str(counter_router))
print("Amount of ONUs configure not configured because of MAC error: " + str(counter_error))
for line in errors_ids:
    print("Error with the client id: " + str(line))
