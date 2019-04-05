import telnetlib
import re
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s -  %(name)s -  %(funcName)s - %(levelname)s: %(message)s')
file_handler = logging.FileHandler('logs/tl1exec.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

# TODO: Create exceptions


def tl1_connect_and_send_commands(unm2000_ip: str, tl1_user: str, tl1_password: str, command: list) -> str:
    telnet_client = telnetlib.Telnet(host=unm2000_ip, port=3337)
    telnet_client.write(("LOGIN:::CTAG::UN=" + tl1_user + ",PWD=" + tl1_password + ";").encode('ascii'))
    login_result: str = (re.findall('(?<=ENDESC=).*(?=\\r)', telnet_client.read_until(b";").decode('UTF-8')))
    commands_counter = 0
    if login_result[0] == 'No error':
        logger.info("***** Successful Login *****")
    else:
        logger.error("***** Error on Login *****")
        logger.error(login_result)
    for line in command:
        telnet_client.write(str(line).encode('ascii'))
        commands_counter += 1
        command_result: str = (re.findall('(?<=ENDESC=).*(?=\\r)', telnet_client.read_until(b";").decode('UTF-8')))
        if command_result[0] == 'No error':
            logger.info("Successful executed command: " + str(line))
        else:
            logger.error("Error executing the command: " + str(line))
            logger.error(login_result)
        if commands_counter > 9:
            logger.info("More than 10 commands on the list, aborting")
            return "More than 10 commands on the list, aborting"
    telnet_client.write(str('LOGOUT:::CTAG::;').encode('ascii'))
    return 'Commands sends successful'




