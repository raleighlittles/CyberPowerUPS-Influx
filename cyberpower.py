#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  5 16:01:51 2018

"""

import datetime
import re
import socket
import subprocess
import time

import influx_handler


def run_status_cmd(timeout=None):
    """
    Runs the command to retrieve UPS status information and returns the output as a string.
    """
    args = ["sudo", "pwrstat", "-status"]

    command = subprocess.run(
        args=args,
        timeout=timeout,
        check=True,
        stdout=subprocess.PIPE)

    return (command.stdout).decode('utf-8')


def extract_values_from_output(cmd_output_as_string):
    """
    Given the raw text output of the UPS info command, this function parses it into a dictionary.
    """

    # filter out newlines, tabs, and split on more than 2 periods at a time
    regex_to_match = r"['.'|\n|\t]{2,}|"

    separated_text = re.split(regex_to_match, cmd_output_as_string)

    # the entry at index 10 just says "current  ups status"
    del separated_text[10]
    # the first 2 entries don't contain any useful data
    return separated_text[2:]


def convert_values_to_dict(data_as_list):
    # Would have used enumerate() here if it let you specify a step size
    data_dictionary = {}
    for index in range(0, len(data_as_list), 2):
        # the data list has the form: ['key/name', 'value', 'key/name', 'value']
        if data_as_list[index] == '':
            break

        current_key, current_value = data_as_list[index], data_as_list[index +
                                                                       1]

        # grafana cant properly graph non-numeric values, so strip non-numeric characters
        data_dictionary[current_key] = current_value.strip()

    return data_dictionary


def parse_cyberpower_load_readings(load_string):
    """
    Load string has the form: "<X> Watt (Y%)" which needs to be converted to a list [X, Y]
    where X is the absolute/raw Load value and Y is the percentage value, relative to the maximum of your UPS outputs.
    """

    parsed_load_readings = list(
        filter(None,
               [re.sub(r"\D", "", string) for string in load_string.split()]))

    if len(parsed_load_readings) == 2:
        return parsed_load_readings

    else:
        raise ValueError(
            "Unable to parse load reading string: {0}".format(load_string))


def parse_data_dict_for_influx(data_dictionary):
    """
    This takes a dictionary of keys/values of data measurements and converts it to a JSON array
    appropriate for sending to Influx.
    """

    measurements_array = []
    for key, value in data_dictionary.items():
        measurement_dict = {}

        measurement_dict['tags'] = {"host": socket.gethostname()}

        measurement_dict['measurement'] = key

        measurement_dict['time'] = datetime.datetime.utcnow().strftime(
            '%Y-%m-%dT%H:%M:%SZ')

        # grafana will only let you use the "graph panel" charts with numeric types, not strings
        numeric_only_keys = [
            'Utility Voltage', 'Output Voltage', 'Battery Capacity',
            'Remaining Runtime'
        ]

        if key in numeric_only_keys:
            value = re.sub('[^0-9]', '', value)
            measurement_dict['fields'] = {'value': int(value)}

        elif key == 'Load':
            load_raw, load_pct = tuple(parse_cyberpower_load_readings(value))
            measurement_dict['fields'] = {
                'value_raw': int(load_raw),
                'value_pct': int(load_pct)
            }

        else:
            measurement_dict['fields'] = {"value": value}

        measurements_array.append(measurement_dict)

    return measurements_array


if __name__ == '__main__':
    while True:
        command_output = run_status_cmd()

        splitted_values = extract_values_from_output(command_output)

        data_dict = convert_values_to_dict(splitted_values)

        influx_ready_array = parse_data_dict_for_influx(data_dict)

        influx_client = influx_handler.initialize_influx()

        resp = influx_handler.send_data_to_influx(influx_client, influx_ready_array)
        time.sleep(1)
