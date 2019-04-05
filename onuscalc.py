import logging
import loggingfunctions
import urllib.request as urllib2
import json
import codecs


# START of logging configuration
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s -  %(name)s -  %(funcName)s - %(levelname)s: %(message)s')
file_handler = logging.FileHandler('logs/onus_calculation.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
# END of logging configuration


def onus_in_a_not_in_b(onus_a: list, onus_b: list) -> list:
    # Send log event of starting
    logger.info(loggingfunctions.generate_string_for_log_tipe_1("EXECUTION OF onus_in_a_not_in_b STARTED"))

    # Calc the 2 variables of ONUs
    result = list(set([str(line).upper() for line in onus_a]))
    onus_b_upper = list(set([str(line).upper() for line in onus_b]))

    # List of ONTs that wasn't deleted
    onts_dif = []

    # Start of removing the 'NAN' string from lists
    for line in result:
        if line == 'NAN':
            result.remove('NAN')
    for line in onus_b_upper:
        if line == 'NAN':
            onus_b_upper.remove('NAN')
    # END of the removing 'NAN' string from lists

    # START of calc of different ONUs
    for line in onus_b_upper:
        try:
            logger.debug("Trying to calc the following serial: " + line)
            result.remove(line)
        except:
            onts_dif.append(line)
            logger.debug("The following serial can`t be deleted: " + line)
        logger.debug("Serial calculated with success:  " + line)
    # END of calc of different ONUs

    # Send log of finishes
    logger.info(loggingfunctions.generate_string_for_log_tipe_1("EXECUTION OF onus_in_a_not_in_b FINISHED"))

    # Return the list of ONUs that wasn't removed and the ONUs that was.

    return result, onts_dif


# This function return 1 if the MAC if fiberhome and 0 if its not
def check_mac_of_connection(mac_address):
    logger.info(loggingfunctions.generate_string_for_log_tipe_1("Starting the calc of MACS"))
    if mac_address == '00:00:00:00:00:00':
        logger.info(loggingfunctions.generate_string_for_log_tipe_1("Ended the calc of MACS"))
        return 2
    if mac_address == '99:99:99:99:99:99':
        logger.info(loggingfunctions.generate_string_for_log_tipe_1("Ended the calc of MACS"))
        return 2
    try:
        request = urllib2.Request('http://macvendors.co/api/' + mac_address, headers={'User-Agent': "API Browser"})
        response = urllib2.urlopen(request)
        # Fix: json object must be str, not 'bytes'
    except:
        logger.exception("Something went wrong with the mac-address request api")
        return 2
    reader = codecs.getreader("utf-8")
    try:
        obj = json.load(reader(response))
    except:
        logger.exception("Something wen wrong with the json returned by api")
    try:
        if (obj['result']['company']) == 'Fiberhome Telecommunication Technologies Co.,LTD':
            logger.info("The following mac-address was checked: " + mac_address)
            logger.info("The mac its FIBERHOME")
            result = 1
        else:
            logger.info("The following mac-address was checked: " + mac_address)
            logger.info("The mac its from: " + obj['result']['company'])
            result = 0
    except:
        logger.error("The mac address was not found: " + mac_address)
        result = 2
    logger.info(loggingfunctions.generate_string_for_log_tipe_1("Ended the calc of MACS"))
    return result
