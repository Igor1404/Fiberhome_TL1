import logging


logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s -  %(name)s -  %(funcName)s - %(levelname)s: %(message)s')

logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('logs/tl1functions.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


# TODO: function to verify the config sintax.

def calc_vlanid(slot, pon):
    if slot == 1:
        if pon == 1 or pon == 2 or pon == 3:
            logger.info('sector: 1, pon:1/2/3, vlanid:3000')
            return 3000
        elif pon == 4 or pon == 5 or pon == 6:
            logger.info("sector: 1, pon:4/5/6, vlanid:3001")
            return 3001
        elif pon == 7 or pon == 8:
            logger.info("sector: 1, pon:7/8, vlanid:3004")
            return 3004
        else:
            logger.critical("sector: invalid, pon:invalid, vlanid:invalid - " + str(slot) + "/" + str(pon))
            return 0
    elif slot == 2:
        if pon == 1 or pon == 2:
            logger.info("sector: 2, pon:1/2, vlanid:3003")
            return 3003
        elif pon == 5 or pon == 6 or pon == 7:
            logger.info("sector: 2, pon:5/6/7, vlanid:3002")
            return 3002
        elif pon == 8:
            logger.info("sector: 2, pon:8, vlanid:3004")
            return 3004
        else:
            logger.critical("sector: invalid, pon:invalid, vlanid:invalid - " + str(slot) + "/" + str(pon))
            return 0
    elif slot == 3:
        if pon == 1:
            logger.info("sector: 3, pon:1, vlanid:3006")
            return 3006
        elif pon == 2 or pon == 3:
            logger.info("sector: 3, pon:2/3, vlanid:3007")
            return 3007
        elif pon == 4:
            logger.info("sector: 3, pon:4, vlanid:3005")
            return 3005
        elif pon == 5:
            logger.info("sector: 3, pon:5, vlanid:3009")
            return 3009
        elif pon == 6 or pon == 7 or pon == 8:
            logger.info("sector: 3, pon:6/7/8, vlanid:3010")
            return 3010
        elif pon == 9 or pon == 10:
            logger.info("sector: 3, pon:9/10, vlanid:3012")
            return 3012
        elif pon == 11 or pon == 12:
            logger.info("sector: 3, pon:11/12, vlanid:3008")
            return 3008
        elif pon == 13:
            logger.info("sector: 3, pon:13, vlanid:3011")
            return 3011
        else:
            logger.critical("sector: invalid, pon:invalid, vlanid:invalid - " + str(slot) + "/" + str(pon))
            return 0


def tl1_bridge_command(olt_ip, slot, pon, onu_serial):
    configure_cmd = "CFG-LANPORTVLAN::OLTID=" + olt_ip + ",PONID=NA-NA-" + str(slot) + "-" + str(pon) + ",ONUIDTYPE=MAC,ONUID=" + \
                    str(onu_serial).upper() +",ONUPORT=NA-NA-NA-1:CTAG::CVLAN=" + str(calc_vlanid(slot, pon)) + " ,CCOS=0;"
    logger.info(configure_cmd)
    return configure_cmd


def tl1_pppoe_command(olt_ip, slot, pon, onu_serial, pppoe_user, pppoe_password):
    configure_cmd = "SET-WANSERVICE::OLTID=" + olt_ip + ",PONID=NA-NA-" + str(slot) + "-" + str(pon) + ",ONUIDTYPE=MAC,ONUID=" + onu_serial.upper() +\
                    ":CTAG::STATUS=1,MODE=2,CONNTYPE=2,VLAN=" + str(calc_vlanid(int(slot), int(pon))) + ",COS=7,QOS=1,NAT=1,IPMODE=3,PPPOEPROXY=2,PPPOEUSER="\
                    + pppoe_user + ",PPPOEPASSWD=" + pppoe_password + ",PPPOENAME=pppoe,PPPOEMODE=1,UPORT=;"
    logger.info(configure_cmd)
    return configure_cmd


def tl1_add_onu_whitelist(olt_ip, slot, pon, onu_serial, onu_model, name):
    configure_cmd = "ADD-ONU::OLTID=" + olt_ip + ",PONID=NA-NA-" + str(slot) + "-" + str(pon) + ":CTAG::ONUID=" + str(onu_serial).upper() +\
                    ",ONUIDTYPE=MAC,ONUTYPE=" + str(onu_model) + ",NAME=" + str(name) +";"
    return configure_cmd


