import subprocess
import socket
import re
import datetime

import influx_handler

def run_status_command(timeout=None):
    args = ["apcaccess"]
    command = subprocess.run(args = args, timeout = timeout,check=True,stdout= subprocess.PIPE)
    return (command.stdout).decode('utf-8')

def extract_values_to_dict(cmd_output_as_string):
    raw_data_as_keys_values_list = cmd_output_as_string.split("\n")
    raw_data_as_dictionary = {}
    for datum in raw_data_as_keys_values_list:
        key, value = datum.split(" : ")
        raw_data_as_dictionary[key] = value

        
    return raw_data_as_dictionary

def parse_data_for_influx(data_dictionary):
    measurements_array_event = []

    for key, value in data_dictionary.items():
        measurement_dict = {}

        measurement_dict['tags'] = {"host" : socket.gethostname() }

        measurement_dict['measurement'] = key

        # confusingly, this is the time the measurement is received, not when its taken
        measurement_dict['time'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

        numeric_only_keys = ['LINEV', 'LOADPCT', 'BCHARGE', 'TIMELEFT', 'MBATTCHG', 'MINTIMEL', 'OUTPUTV', 'LOTRANS', 'HITRANS', 'CUMONBATT', 'NOMPOWER']

        if key in numeric_only_keys:
            numeric_only_value = re.sub('[^0-9]', 'pip', value)
            measurement_dict['fields'] = {'value' : int(numeric_only_value)}

        else:
            measurement_dict['fields'] = {"value" : value}

        measurements_array_event.append(measurement_dict)


    return measurements_array_event


if __name__ == '__main__':
    while True:
        command_output = run_status_command()
        data_dictionary = extract_values_to_dict(command_output)

        influx_ready_array = parse_data_for_influx(data_dictionary)

        influx_client = influx_handler.initialize_influx()

        response = influx_handler.send_data_to_influx(influx_client, influx_ready_array)
