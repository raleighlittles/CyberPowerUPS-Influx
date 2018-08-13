# About

**A short script to push the status information from a compatible\* UPS into [InfluxDB](https://www.influxdata.com/).**

# Setup

This currently works on any UPS that is one of the following:

| Brand      | Model Name   | Capacity (Watts) |
|------------|--------------|------------------|
| CyberPower | CP850AVRLCD  | 510              |
| CyberPower | CP1000AVRLCD | 600              |
| CyberPower | CP1350AVRLCD | 815              |
| CyberPower | CP1500AVRLCD | 900              |

[Amazon link](http://a.co/aq341qo)

It also requires:

* The UPS connected (via USB Type B) to a host machine

* The host machine running CyberPower's [PowerPanel Personal - Linux](https://www.cyberpowersystems.com/product/software/powerpanel-for-linux/) software. *Windows support will be added at a future time.*

Finally, *the script must be run on the aforementioned host machine,with sudo privileges.*

```bash
sudo python3 script.py
```

# Grafana integration

You can add this into Grafana like you would with any other new datasource. 