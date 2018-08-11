#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  5 16:01:51 2018

@author: raleigh
"""

import re
import json
import socket
import datetime
import pdb
import subprocess
import influxdb


def run_status_cmd(timeout=None):
    """
    Runs the status command and returns the output as a string.
    """
    command = subprocess.run(args=["sudo", "pwrstat", "-status"], timeout=timeout, check=True, stdout=subprocess.PIPE)
    
    return command.stdout

def extract_values_from_output(cmd_output_as_string):
    """
    Given the raw text output of the UPS info command, this function parses it into a dictionary.
    """
    
    #regex_to_match = r"['.']{2,}"
    
    # filter out newlines, tabs, and split on more than 2 periods at a time
    regex_to_match = r"['.'|\n|\t]{2,}|"
    
    separated_text = re.split(regex_to_match, cmd_output_as_string)
    
    # the entry at index 10 just says "current  ups status"
    del separated_text[10]
    # the first 2 entries dont contain any useful data
    return separated_text[2:]
    
    
def convert_values_to_dict(data_as_list):
    # Would have used enumerate() here if it let you specify a step size
    data_dictionary = {}
    for index in range(0, len(data_as_list), 2):
        # the data list has the form: ['key/name', 'value', 'key/name', 'value']
        if data_as_list[index] == '':
            break
        
        current_key, current_value = data_as_list[index], data_as_list[index+1]
        
        # grafana cant properly graph non-numeric values, so strip non-numeric characters
        data_dictionary[current_key] = current_value.strip()
        
    return data_dictionary
        

def parse_data_dict_for_influx(data_dictionary):
    """
    This takes a dictionary of keys/values of data measurements and converts it to a JSON array
    appropriate for sending to Influx.
    """
    
    measurements_array = []
    for key, value in data_dictionary.items():
        measurement_dict = {}
        measurement_dict['measurement'] = key
        measurement_dict['tags'] = {
                "host": socket.gethostname()
                }
        measurement_dict['time'] = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        measurement_dict['fields'] = {
                    "value": value
                }
        
        measurements_array.append(measurement_dict)
        
    return measurements_array
    
def initialize_influx():
    """
    Initializes InfluxDB to receive UPS data measurements.
    """
    influx_client = influxdb.InfluxDBClient(host='localhost', port=8086)
    
    database_list = influx_client.get_list_database()
    if all([database['name'] != 'ups' for database in database_list]):
        print("UPS database does not yet exist -- creating one now.")
        influx_client.create_database('ups')
    else:
        print("UPS database already exists.")
        
    influx_client.switch_database('ups')
    
    return influx_client


def send_data_to_influx(influx_client, json_data_array):
    
    response = influx_client.write_points(json_data_array)
    
    while response:
        response = influx_client.write_points(json_data_array)
        
    print("Stopped writing data to Influx.")
    
    
    
example_input = """The UPS information shows as following:

	Properties:
		Model Name................... CP1500AVRLCDa
		Firmware Number.............. CTHFU2010324
		Rating Voltage............... 120 V
		Rating Power................. 900 Watt(1500 VA)

	Current UPS status:
		State........................ Normal
		Power Supply by.............. Utility Power
		Utility Voltage.............. 117 V
		Output Voltage............... 117 V
		Battery Capacity............. 100 %
		Remaining Runtime............ 18 min.
		Load......................... 324 Watt(36 %)
		Line Interaction............. None
		Test Result.................. Unknown
		Last Power Event............. Blackout at 2018/07/06 07:44:11 for 24 sec.
"""

command_output = run_status_cmd()

splitted_values = extract_values_from_output(command_output)

data_dict = convert_values_to_dict(splitted_values)

influx_ready_array = parse_data_dict_for_influx(data_dict)