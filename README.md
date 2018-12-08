# About

**A short script to push the status information from a compatible\* UPS into [InfluxDB](https://www.influxdata.com/).**

# Setup/Compatiblity

## Hardware

This currently works on any UPS that is one of the following:

| Brand      | Model Name   | Capacity (Watts) |
|------------|--------------|------------------|
| CyberPower | CP850AVRLCD  | 510              |
| CyberPower | CP1000AVRLCD | 600              |
| CyberPower | CP1350AVRLCD | 815              |
| CyberPower | CP1500AVRLCD | 900              |

[Amazon link](http://a.co/aq341qo)

The UPS must be connected (via USB Type B) to a host machine.

## Software

There's currently two supported ways of interfacing with your UPS through this software (more may be added in the future):

* Using CyberPower's [PowerPanel Personal - Linux](https://www.cyberpowersystems.com/product/software/powerpanel-for-linux/) software. 

* Using [APC UPS Daemon](http://www.apcupsd.org/) (apcupsd)


Before running this script, you must also have InfluxDB already installed -- downloads are available at: https://portal.influxdata.com/downloads

# Usage

First install the Python-InfluxDB client.

```bash
pip install influxdb
```

Then, depending on which strategy you're using to interface with your UPS, you will either do:

```bash
python3 apcupsd.py
```

or 

```bash
python3 cyberpower.py
```

##  Note about admin access
Depending on how you installed the Cyberpower UPS software, you might need sudo access to actually run it. If you need sudo access to run the Cyberpower tool then you will also need to run the python script with sudo access (simply prepend 'sudo' to the command).

# Grafana integration

For instructions on how to add your new InfluxDB source into Grafana, see here: http://docs.grafana.org/features/datasources/influxdb/



# TODO 

- [ ] Refactor
- [ ] Serial connection support
- [ ] Windows support 