# About

**A short script to push the status information from a compatible\* [UPS](https://en.wikipedia.org/wiki/Uninterruptible_power_supply) into [InfluxDB](https://www.influxdata.com/).**

# Setup

![flowchart](./docs/mermaid-diagram-20220202103940.svg)

Depending on what UPS you have and how you plan on communicating with it, you'll need to install ONE of the following:

* CyberPower's [PowerPanel Personal - Linux](https://www.cyberpowersystems.com/product/software/powerpanel-for-linux/) software

*  [APC UPS Daemon](http://www.apcupsd.org/) ('apcupsd')

Regardless of which UPS management tool you install, you'll also need to install InfluxDB: https://portal.influxdata.com/downloads

# Usage

First install the Python-InfluxDB client.

```bash
$ pip install influxdb
```

Then, depending on which strategy you're using to interface with your UPS, you will either do:

```bash
$ python3 apcupsd.py
```

or 

```bash
$ python3 cyberpower.py
```

##  Sudo/Root permissions
Depending on how you installed the CyberPower UPS software, you might need sudo access to actually run it. If you need sudo access to run the CyberPower tool then you will also need to run the python script with sudo access (simply prepend 'sudo' to the command).

# Grafana integration

For instructions on how to add your new InfluxDB source into Grafana, see here: http://docs.grafana.org/features/datasources/influxdb/