# iot-central-client-python3
Azure IOT Central simple client for raspberry pi 3B

# Install dependencies

You need python3 installed on your system. Then:

`pip3 install -r requirements.txt`

# Setup the daemon

Edit config.ini

```
; config.ini
[REMOTE]
HostName = xxxxx
DeviceId = yyyyy
SharedAccessKey = zzzzz

[SAMPLE]
CpuDelaySample = 2
GlobalDelaySample = 5
```

# Run the daemon

`python3 iot-hub-client-daemon.py`

Should start the daemon in background

# Notes

* psutil-demo.py contain the code to get your system telemetry
* iot-hub-client.py contain the minimal code to send your systems telemetry

`/!\ This code is running on my raspi but neither the requirements.txt nore the deployment has been tested on a fresh install. Proceed carefully and open a PR if you encounter or fix any issue. Thanks /!\`
