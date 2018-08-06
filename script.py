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

splitted_values = extract_values_from_output(example_input)

data_dict = convert_values_to_dict(splitted_values)

influx_ready_array = parse_data_dict_for_influx(data_dict)