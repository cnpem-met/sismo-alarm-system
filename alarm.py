from typing import Tuple
import numpy as np
import pandas as pd
from datetime import datetime
import os
import time

from email_sender import send_email
from ioc import IOC
from utils import Severity, log
from config import LIMITS_ALERT, LIMITS_DANGER, MINIMUM_TIME_BETWEEN_ALARMS, REF_MAP, ALERT_ALARM_ENABLED, PV_NAME


def read_txt(filepath: str) -> pd.DataFrame:
    time.sleep(1)
    try:
        data = pd.read_csv(filepath, sep='\t', decimal=',')
        # checking if type is correct, and if not changuing the decimal delimiter
        if data.dtypes[0] != np.float64:
            data = pd.read_csv(filepath, sep='\t')
    except (PermissionError, FileNotFoundError):
        # conflict between write and read operations, ignore this file
        log(f'Failed to verify file {os.path.basename(filepath)}.')
        data = pd.DataFrame()
    return data

def check_max_values(data: pd.DataFrame) -> dict:
    out_text = {'danger': '', 'alert': ''}

    max_values = data.max().values
    print(max_values)
    for i, value in enumerate(max_values):
        # checking values within the list defined by the "danger" limits
        for limit in LIMITS_DANGER:
            if value > limit:
                out_text['danger'] += f'{data.columns[i]} passou o limite de {limit} g.\n'
        # checking values within the list defined by the "alert" limits
        for limit in LIMITS_ALERT:
            # only considering data from a particular channel
            if value > limit and i == 2:
                out_text['alert'] = 'Passagem do rolo compressor detectada.\n'
    return out_text

def run_alarm_checking(path: str, last_alarm: datetime) -> Tuple[bool, list]:
    data = read_txt(path)
    out_txt = check_max_values(data)
    time_since_last_alarm = (datetime.now() - last_alarm).total_seconds()
    
    is_alarm_triggered = False
    log_msgs = []
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    
    if out_txt['danger'] and time_since_last_alarm > MINIMUM_TIME_BETWEEN_ALARMS:
        # reference expects a filename such as 'CAR-01.txt' or 'CAT-01.txt'
        reference = os.path.basename(path).split('-')[0]
        reference = REF_MAP[reference]

        body_txt = f'Alarme disparado na {reference}\n\n' + out_txt['danger']
        log_msgs.append('Alarm triggered (DANGER), sending email...')
        send_email(body_txt, severity=Severity.DANGER)
        
        is_alarm_triggered = True
    
    if ALERT_ALARM_ENABLED:
        pv_value = 0
        if out_txt['alert']:
            log_msgs.append('Alarm triggered (ALERT), updating PV...')
            pv_value = 1
            is_alarm_triggered = True
        IOC.driver.write(PV_NAME, pv_value)

    _ = [print(f'[{now}] {log_msg}') for log_msg in log_msgs]

    return is_alarm_triggered, log_msgs

