# About

**A short script to push the status information from a compatible\* UPS into [InfluxDB](https://www.influxdata.com/).**

# Setup/Compatiblity

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

If all of the requirements above are met, run the command in the `example/input.txt` file and check that your system's output is similar to the output stored in the `output.txt` file.


# Usage
To run the script, do:

```bash
python3 script.py
```

For now, this script has to be saved and ran on the machine that is connected to the UPS. 

## Admin access
If you require `sudo` access to run the UPS status command, then you need to run `script.py` with administrator access as well.


# Grafana integration

You can add this into Grafana like you would with any other new datasource. 