import influxdb

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
        pass

    return influx_client


def send_data_to_influx(influx_client, json_data_array):
    """
    Uses the InfluxDB Python API to send data.
    """
    influx_client.switch_database('ups')
    bool_response = influx_client.write_points(json_data_array)

    return bool_response